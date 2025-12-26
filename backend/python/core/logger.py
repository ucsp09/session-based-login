import logging
import json

class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_record = {
            'time': self.formatTime(record, self.datefmt),
            'name': record.name,
            'module': record.module,
            'funcName': record.funcName,
            'lineno': record.lineno,
            'level': record.levelname,
            'message': record.getMessage(),
        }
        return json.dumps(log_record)

class Logger:
    @staticmethod
    def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
        logger = logging.getLogger(name)
        logger.setLevel(level)
        if not logger.hasHandlers():
            ch = logging.StreamHandler()
            ch.setLevel(level)
            formatter = JsonFormatter()
            ch.setFormatter(formatter)
            logger.addHandler(ch)
        return logger
