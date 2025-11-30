import logging
import signal
import sys
from threading import Event

from honeyguard.core.config import config
from honeyguard.core.logger import setup_logger


def load_services():
    """Charge dynamiquement les services activés"""
    services = []
    enabled = config.get_enabled_services()
    
    logger = logging.getLogger('honeyguard')
    
    if 'ssh' in enabled:
        from honeyguard.services.ssh import SSHHoneypot
        services.append(SSHHoneypot())
        logger.info("✓ SSH service loaded")
    
    # Futur : http, ftp, etc.
    # if 'http' in enabled:
    #     from honeyguard.services.http import HTTPHoneypot
    #     services.append(HTTPHoneypot())
    
    return services


def main():
    # Charge config
    config.load('config/default.yml')
    
    # Setup logger
    log_config = config.get('logging', {})
    logger = setup_logger(
        log_file=log_config.get('file', 'logs/honeyguard.log'),
        level=log_config.get('level', 'INFO'),
        format_type=log_config.get('format', 'json')
    )
    
    logger.info("=" * 60)
    logger.info(f"🍯 {config.get('app.name')} v{config.get('app.version')}")
    logger.info("=" * 60)
    
    # Charge services
    services = load_services()
    
    if not services:
        logger.error("No services enabled in config!")
        sys.exit(1)
    
    logger.info(f"Enabled services: {', '.join(config.get_enabled_services())}")
    logger.info("=" * 60)
    
    # Démarre tous les services
    stop_event = Event()
    
    def signal_handler(sig, frame):
        logger.info("\n🛑 Shutting down...")
        stop_event.set()
    
    signal.signal(signal.SIGINT, signal_handler)
    
    # Lance chaque service dans son thread (déjà géré par Paramiko)
    for service in services:
        import threading
        t = threading.Thread(target=service.start)
        t.daemon = True
        t.start()
    
    # Attend Ctrl+C
    stop_event.wait()
    
    # Arrête tous les services
    for service in services:
        service.stop()
    
    logger.info("👋 Goodbye!")


if __name__ == '__main__':
    main()