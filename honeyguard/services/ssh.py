import paramiko
import logging
import socket
import threading
from datetime import datetime

from honeyguard.core.config import config
from honeyguard.core.logger import log_event


class SSHHoneypot:
    """SSH Honeypot avec Paramiko"""
    
    def __init__(self):
        ssh_config = config.get('services.ssh', {})
        
        self.host = ssh_config.get('host', '0.0.0.0')
        self.port = ssh_config.get('port', 2222)
        self.banner = ssh_config.get('banner', 'SSH-2.0-OpenSSH_8.9p1')
        
        self.logger = logging.getLogger('honeyguard.ssh')
        self.host_key = paramiko.RSAKey.generate(2048)
        
        self.running = False
        self.sock = None
    
    def start(self):
        """Démarre le serveur SSH"""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.sock.listen(100)
        
        self.running = True
        self.logger.info(f"SSH Honeypot started on {self.host}:{self.port}")
        
        while self.running:
            try:
                client, addr = self.sock.accept()
                t = threading.Thread(target=self.handle_client, args=(client, addr))
                t.daemon = True
                t.start()
            except Exception as e:
                if self.running:
                    self.logger.error(f"Error accepting connection: {e}")
    
    def stop(self):
        """Arrête le serveur"""
        self.running = False
        if self.sock:
            self.sock.close()
        self.logger.info("SSH Honeypot stopped")
    
    def handle_client(self, client, addr):
        """Gère une connexion client"""
        session_id = datetime.now().strftime('%Y%m%d%H%M%S%f')
        
        # Récupère max_attempts depuis config
        max_attempts = config.get('services.ssh.max_auth_attempts', 3)
        
        # Log connexion
        log_event('ssh', 'connection', {
            'source_ip': addr[0],
            'source_port': addr[1],
            'session_id': session_id
        })
        
        try:
            transport = paramiko.Transport(client)
            transport.local_version = self.banner
            transport.add_server_key(self.host_key)
            
            # Passe max_attempts au serveur
            server = SSHServer(addr[0], session_id, max_attempts=max_attempts)
            transport.start_server(server=server)
            
            channel = transport.accept(20)
            if channel:
                channel.close()
        
        except Exception as e:
            self.logger.debug(f"[{session_id}] Error: {e}")
        
        finally:
            try:
                transport.close()
            except:
                pass


class SSHServer(paramiko.ServerInterface):
    """Interface serveur SSH"""
    
    def __init__(self, client_ip, session_id, max_attempts=3):
        self.client_ip = client_ip
        self.session_id = session_id
        self.logger = logging.getLogger('honeyguard.ssh')
        
        self.max_attempts = max_attempts
        self.attempt_count = 0
    
    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
    
    def check_auth_password(self, username, password):
        """Capture credentials"""
        
        # Incrémente compteur
        self.attempt_count += 1
        
        self.logger.warning(
            f"[{self.session_id}] 🔑 Attempt {self.attempt_count}/{self.max_attempts} - "
            f"{self.client_ip} - User: '{username}' | Pass: '{password}'"
        )
        
        # Log en JSON
        log_event('ssh', 'auth_attempt', {
            'source_ip': self.client_ip,
            'session_id': self.session_id,
            'username': username,
            'password': password,
            'auth_method': 'password',
            'attempt': self.attempt_count,
            'success': False
        })
        
        # Ferme après max_attempts
        if self.attempt_count >= self.max_attempts:
            self.logger.info(f"[{self.session_id}] Max attempts reached, closing connection")
        
        return paramiko.AUTH_FAILED
    
    def check_auth_publickey(self, username, key):
        self.logger.info(f"[{self.session_id}] Public key auth from {self.client_ip}")
        return paramiko.AUTH_FAILED
    
    def get_allowed_auths(self, username):
        # Si max atteint, ne propose plus rien
        if self.attempt_count >= self.max_attempts:
            return ''
        return 'password,publickey'