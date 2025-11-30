import logging
import json
from pathlib import Path
from datetime import datetime


class JSONFormatter(logging.Formatter):
    """Formatter qui output en JSON"""
    
    def format(self, record):
        log_data = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'level': record.levelname,
            'service': getattr(record, 'service', 'system'),
            'message': record.getMessage(),
        }
        
        # Ajoute les champs custom (username, password, etc.)
        if hasattr(record, 'extra_data'):
            log_data.update(record.extra_data)
        
        return json.dumps(log_data, ensure_ascii=False)


def setup_logger(log_file='logs/honeyguard.log', level='INFO', format_type='json'):
    """Configure le logger principal"""
    
    # Ajoute la date au nom du fichier
    log_path = Path(log_file)
    date_str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    
    # logs/honeyguard.log → logs/honeyguard_20250115.log
    log_file_with_date = log_path.parent / f"{log_path.stem}_{date_str}{log_path.suffix}"
    
    # Crée le dossier logs
    log_file_with_date.parent.mkdir(parents=True, exist_ok=True)
    
    # Logger principal
    logger = logging.getLogger('honeyguard')
    logger.setLevel(getattr(logging, level.upper()))
    
    # Handler fichier
    file_handler = logging.FileHandler(log_file_with_date, encoding='utf-8')
    
    if format_type == 'json':
        file_handler.setFormatter(JSONFormatter())
    else:
        file_handler.setFormatter(
            logging.Formatter('[%(asctime)s] %(levelname)-8s %(message)s')
        )
    
    logger.addHandler(file_handler)
    
    # Handler console (toujours en texte)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(
        logging.Formatter('[%(asctime)s] %(levelname)-8s %(message)s', datefmt='%H:%M:%S')
    )
    logger.addHandler(console_handler)
    
    # Log le nom du fichier utilisé
    logger.info(f"Logging to: {log_file_with_date}")
    
    return logger


def log_event(service, event_type, data):
    """
    Log un événement structuré
    
    Args:
        service: 'ssh', 'http', 'ftp', etc.
        event_type: 'connection', 'auth_attempt', etc.
        data: dict avec les données (ip, user, password, etc.)
    """
    logger = logging.getLogger('honeyguard')
    
    # Crée un LogRecord custom
    record = logger.makeRecord(
        logger.name, logging.WARNING, "", 0, event_type, (), None
    )
    record.service = service
    record.extra_data = data
    
    logger.handle(record)