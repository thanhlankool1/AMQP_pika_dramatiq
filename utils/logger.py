import logging

class Logger():
    def __init__(self):
        self.logger = None

    def logtoFile(self):
        console = True
        # create the logging instance for logging to file only
        self.logger = logging.getLogger('log')

        
        # make log file directory when not exist
        # directory = os.path.dirname("stop_service.log")
        # if not os.path.exists(directory):
        #     os.makedirs(directory)

        file_logger = logging.FileHandler('check_consumer.log',encoding='utf-8')
        #file_logger = logging.FileHandler('/root/lan/remove_gift/log_test_remove_service.log')
        NEW_FORMAT = '[%(asctime)s] - [%(levelname)s] - %(message)s'
        file_logger_format = logging.Formatter(NEW_FORMAT)

        # tell the handler to use the above format
        file_logger.setFormatter(file_logger_format)

        # finally, add the handler to the base logger
        if self.logger.hasHandlers():
            self.logger.handlers.clear()
        self.logger.addHandler(file_logger)

        # remember that by default, logging will start at 'warning' unless
        # we set it manually
        self.logger.setLevel(logging.DEBUG)

        if console:
            # define a Handler which writes INFO messages or higher to the sys.stderr
            console = logging.StreamHandler()
            console.setLevel(logging.INFO)
            # set a format which is simpler for console use
            formatter = logging.Formatter('[%(asctime)s] - [%(levelname)s] - %(message)s')
            # tell the handler to use this format
            console.setFormatter(formatter)
            # add the handler to the the current logger
            self.logger.addHandler(console)
        return self.logger

LOGGER = Logger().logtoFile()