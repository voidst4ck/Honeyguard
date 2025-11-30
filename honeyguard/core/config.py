import yaml
from pathlib import Path
from typing import Any


class ConfigManager:
    def __init__(self):
        self._config = None
    
    def load(self, config_file: str = 'config/default.yml'):
        config_path = Path(config_file)
        if not config_path.exists():
            raise FileNotFoundError(f"Config not found: {config_path}")
        
        with open(config_path, 'r') as f:
            self._config = yaml.safe_load(f)
    
    def get(self, key_path: str, default: Any = None) -> Any:
        keys = key_path.split('.')
        value = self._config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        return value
    
    def is_service_enabled(self, service_name: str) -> bool:
        """Vérifie si un service est activé"""
        return self.get(f'services.{service_name}.enabled', False)
    
    def get_enabled_services(self) -> list:
        """Retourne la liste des services activés"""
        services = self.get('services', {})
        return [name for name, cfg in services.items() if cfg.get('enabled', False)]


config = ConfigManager()