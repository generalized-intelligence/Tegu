#encoding=utf-8
import logging
import sys

class MyLogger(): 
    mylogger_instance = None

    def __init__(self, path, parent=None):
        self.LOG_FILE = path
        self.logger = logging.getLogger('Tegu')
        self.logger.setLevel(level = logging.DEBUG)
        handler = logging.FileHandler(self.LOG_FILE)
        handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        console = logging.StreamHandler(sys.stdout)
        console.formatter = formatter
        console.setLevel(logging.DEBUG)

        self.logger.addHandler(handler)
        self.logger.addHandler(console)

    @classmethod
    def getMyLogger(cls, path="log.log"):
        if path=='log.log':
            if cls.mylogger_instance is None:
                return
            else:
                return cls.mylogger_instance
        else:
            if cls.mylogger_instance is None:
                cls.mylogger_instance = cls(path)
            return cls.mylogger_instance
        
    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warn(self, msg):
        self.logger.warn(msg)
    
    def error(self, msg):
        self.logger.error(msg)

    def log_params(self, **params):
        print(self.LOG_FILE)
        self.info(params)
            


