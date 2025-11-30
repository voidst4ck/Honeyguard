import yaml
from pathlib import Path
from typing import Optional, Dict


class UserManager:
    """Gère la whitelist des utilisateurs autorisés"""
    
    def __init__(self, users_file='config/users.yml'):
        self.users_file = Path(users_file)
        self.users = {}
        self.default_config = {}
        
        if self.users_file.exists():
            self.load()
    
    def load(self):
        """Charge la whitelist"""
        with open(self.users_file, 'r') as f:
            data = yaml.safe_load(f) or {}
        
        # Indexe par username pour lookup rapide
        self.users = {
            user['username']: user 
            for user in data.get('users', [])
        }
        
        self.default_config = data.get('default', {
            'allow_shell': False,
            'max_attempts': 3
        })
    
    def check_credentials(self, username: str, password: str) -> Optional[Dict]:
        """
        Vérifie si credentials sont dans la whitelist
        
        Returns:
            Dict avec config user si match, None sinon
        """
        user = self.users.get(username)
        
        if user and user.get('password') == password:
            return {
                'username': username,
                'shell': user.get('shell', False),
                'level': user.get('level', 'low_interaction')
            }
        
        return None
    
    def is_whitelisted(self, username: str) -> bool:
        """Vérifie si username existe dans whitelist"""
        return username in self.users
    
    def get_default_config(self) -> Dict:
        """Retourne la config par défaut"""
        return self.default_config


# Instance globale
user_manager = UserManager()