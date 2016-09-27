from constants import LOG_DEBUG, LOG_INFO, LOG_TEST, LOG_SUCCESS, LOG_ERROR

COLOR_DEBUG = "\033[95m"
COLOR_INFO = "\033[92m"
COLOR_TEST = "\033[96m"
COLOR_SUCCESS = "\033[94m"
COLOR_ERROR = "\033[91m"
COLOR_ENDC = "\033[0m"

class Log:

    @staticmethod
    def d(string):
        if LOG_DEBUG:
            print COLOR_DEBUG + "[DEBUG] " + COLOR_ENDC + string

    @staticmethod
    def i(string):
        if LOG_INFO:
            print COLOR_INFO + "[INFO] " + COLOR_ENDC + string

    @staticmethod
    def t(string):
        if LOG_TEST:
            print COLOR_TEST + "[TEST] " + COLOR_ENDC + string

    @staticmethod
    def s(string):
        if LOG_SUCCESS:
            print COLOR_SUCCESS + "[SUCCESS] " + COLOR_ENDC + string

    @staticmethod
    def e(string):
        if LOG_ERROR:
            print COLOR_ERROR + "[ERROR] " + COLOR_ENDC + string
