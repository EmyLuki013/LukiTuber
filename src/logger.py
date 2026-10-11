from loguru import logger
from datetime import datetime
import os
import sys

class Logger:
    def __init__(self, name: str):
        self.name = name
        self.log_dir = "logs"
        self.session_id = None
        self._configure()
    
    def _configure(self):
        logger.remove()
        
        logger.add(
            sys.stdout,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            level="INFO"
        )
        
        os.makedirs(self.log_dir, exist_ok=True)
    
    def start_session(self):
        """Inicia uma nova sessão de log"""
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        logger.add(
            os.path.join(self.log_dir, f"{self.name}_{self.session_id}_debug.log"),
            format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} | {message}",
            level="DEBUG",
            encoding="utf-8"
        )
        
        logger.add(
            os.path.join(self.log_dir, f"{self.name}_{self.session_id}_error.log"),
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}",
            level="ERROR",
            encoding="utf-8",
            rotation="100 MB"
        )
        
        return self.session_id
    
    def get_logger(self):
        return logger

log = Logger("Lukituber")
session_id = log.start_session()
log = log.get_logger()
