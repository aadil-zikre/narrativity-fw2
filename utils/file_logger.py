import logging
import sys
import __main__ as MAIN

class Logger:
    def __init__(self, logger_name=None, add_stream_handler = True, std_err = False, level = 'debug'):
        self.logger_name = logger_name if logger_name else __name__
        self.add_stream_handler = add_stream_handler
        self.std_err = std_err
        self.level = self.LEVELS.get(level, logging.INFO)
        self.logger = None
    
    LEVELS = {'debug': logging.DEBUG, 'info': logging.INFO, 'warning': logging.WARNING, 'error': logging.ERROR, 'critical': logging.CRITICAL}
    
    @staticmethod
    def remove_handlers(logger):
        while logger.handlers:
            handler = logger.handlers[0]
            handler.close()
            logger.removeHandler(handler)
        return logger
    
    def set_logger(self, dt_fmt_basic = True):
        logging.basicConfig(
            format="%(asctime)s :: [%(levelname)s] :: %(message)s", 
            datefmt='%d %B, %Y %I:%M:%S %p %z',
            level=logging.ERROR,
            stream = sys.stderr,
            force=True)
        logging.getLogger().removeHandler(logging.getLogger().handlers[0])
        self.logger = logging.getLogger(self.logger_name) ## IMP: __name__ is important for scope of logger
        self.logger.setLevel(logging.DEBUG)
        if dt_fmt_basic:
            formatter = logging.Formatter("%(asctime)s :: [%(levelname)s] :: %(message)s")
        else:
            formatter = logging.Formatter("%(asctime)s :: [%(levelname)s] :: %(message)s", datefmt='%d %B, %Y %I:%M:%S %p %z')
        if self.add_stream_handler:
            if not self.std_err:
                # self.logger = self.remove_handlers(self.logger)
                stream_handler = logging.StreamHandler(stream = sys.stdout)
            else:
                stream_handler = logging.StreamHandler(stream = sys.stderr)
            stream_handler.setFormatter(formatter)
            stream_handler.setLevel(self.level)
            self.logger.addHandler(stream_handler)
    
    def get_logger(self, dt_fmt_basic = True):
        if not self.logger:
            self.set_logger(dt_fmt_basic)
        return self.logger
    
    def add_file_handler(self, filepath, level = logging.INFO):
        file_handler = logging.FileHandler(filepath)
        file_handler.setLevel(level)
        formatter = logging.Formatter(
            '%(asctime)s :: %(name)s :: %(levelname)s :: %(message)s', datefmt='%d %B, %Y %I:%M:%S %p %z')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        return self.get_logger()
    
    def add_log_prefix(self, prefix):
        self.prefix = prefix
        for handler in self.logger.handlers:
            if self.prefix:
                formatter = logging.Formatter(handler.formatter._fmt.replace("%(message)s", "") + f"{prefix} :: %(message)s", datefmt='%d %B, %Y %I:%M:%S %p %z')
                handler.setFormatter(formatter)
        return self.get_logger()
    
    def remove_log_prefix(self):
        for handler in self.logger.handlers:
            if self.prefix:
                formatter = logging.Formatter(handler.formatter._fmt.replace(f"{self.prefix} :: %(message)s", "%(message)s"), datefmt='%d %B, %Y %I:%M:%S %p %z')
                handler.setFormatter(formatter)
        self.prefix = None
        return self.get_logger()
    
    def __str__(self):
        to_print("logger not initialized")
        if self.logger:
            to_print = ""
            to_print = "".join([to_print,f"Logger is set. Name :: {self.logger.name} with the following handlers :"])
            for num, i in enumerate(self.logger.handlers, start = 1):
                h_name, h_op, h_level = i.__str__().replace("<","").replace(">","").split(" ")
                to_print = "".join([to_print, "\n", f"{num} :: {h_name} :: {h_level}"])
        return to_print

if 'LOGGER_NAME' in dir(MAIN):
    logger_name = MAIN.LOGGER_NAME
else:
    logger_name = 'acf'

logger = Logger(logger_name)
log = logger.get_logger() # You can change the date format here

log_debug = log.debug
log_info = log.info
log_warning = log.warning
log_error = log.error
log_critical = log.critical

log_info("Logger initialized WITHOUT file handler")

def init_logger(filepath):
    global log
    log = logger.add_file_handler(filepath)
    log_info(f"File Handler added. Location set to {filepath!r}")

def add_log_prefix_global(prefix):
    global log
    log = logger.add_log_prefix(prefix)
    log_info(f"Log prefix added: {prefix}")

def remove_log_prefix_global():
    global log
    log = logger.remove_log_prefix()
    log_info("Log prefix removed")

if __name__ == '__main__':
    log_file_loc = '/home/azikre/aadil/github/narrativity-fw2/tmp.log'
    init_logger(log_file_loc)
    add_log_prefix_global("preprocessing_utils")
    remove_log_prefix_global()

    