# Configs.py
import yaml

class Config:
    _config = None

    @classmethod
    def load(cls, file_path):
        if cls._config is None:
            # with open(file_path, 'r') as file:
            #     cls._config = yaml.safe_load(file)
            with open(file_path, 'r', encoding='utf-8') as f:
                cls._config = yaml.safe_load(f)
        return cls._config

    @classmethod
    def get(cls, key):
        if cls._config is None:
            raise ValueError("Config not loaded. Call load() first.")
        return cls._config.get(key)
