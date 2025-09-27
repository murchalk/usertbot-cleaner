import configparser
from pathlib import Path


class Config:
    def __init__(self):
        self.parser = configparser.ConfigParser()
        self._load_config()
        self._setup_paths()
        self._setup_properties()

    def _load_config(self) -> None:
        config_file = Path('config.ini')
        config_file.exists() or print("Configuration file 'config.ini' not found!")
        self.parser.read(config_file, encoding='utf-8')

    def _setup_paths(self) -> None:
        base_dir = Path(__file__).parent
        self.SESSION = str(base_dir.parent / "data/account")

    def _setup_properties(self) -> None:
        self.API_ID = self.parser.getint('Telegram', 'API_ID', fallback=0)
        self.API_HASH = self.parser.get('Telegram', 'API_HASH', fallback='')
        self.PHONE_NUMBER = self.parser.get('Telegram', 'PHONE_NUMBER', fallback='')

        self.INTERVAL_CHAT = self.parser.getfloat('Bot', 'INTERVAL_CHAT', fallback=1.0)
        self.INTERVAL_MESSAGE = self.parser.getfloat('Bot', 'INTERVAL_MESSAGE', fallback=0.5)
        self.LIMIT_HOURS = self.parser.getfloat('Bot', 'LIMIT_HOURS', fallback=48.0)
        self.COUNT_MESSAGES = self.parser.getint('Bot', 'COUNT_MESSAGES', fallback=0)
        self.CHATS_ID = self.parser.get('Bot', 'CHATS_ID', fallback=0).split(',')
        self.TEXT_REPLACE = self.parser.get('Bot', 'TEXT_REPLACE', fallback='')

config = Config()
