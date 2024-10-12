# Configs.py
import os

import yaml

class Config:
    _config = None

    @classmethod
    def load(cls, configFile):
        if cls._config is None:
            # 获取当前文件的绝对路径
            current_dir = os.path.dirname(__file__)
            # 构建相对路径
            file_path = os.path.join(current_dir, configFile)
            print(file_path)
            with open(file_path, 'r', encoding='utf-8') as f:
                cls._config = yaml.safe_load(f)
        return cls._config

    @classmethod
    def get(cls, key):
        if cls._config is None:
            raise ValueError("Config not loaded. Call load() first.")
        return cls._config.get(key)
