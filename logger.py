LOG_LEVEL = 0

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def set_logger_config(OK_responses = False, WARNING_responses = False, FAIL_responses = False):
    global LOG_LEVEL
    LOG_LEVEL = 0
    if OK_responses:
        LOG_LEVEL = 100
    if WARNING_responses:
        LOG_LEVEL += 10
    if FAIL_responses:
        LOG_LEVEL += 1

def appropriate_level(color):
    global LOG_LEVEL
    if color == bcolors.OKBLUE or color == bcolors.OKCYAN or color == bcolors.OKGREEN:
        return LOG_LEVEL // 100 == 1
    if color == bcolors.WARNING:
        return LOG_LEVEL // 10 % 10 == 1
    if color == bcolors.FAIL:
        return LOG_LEVEL % 10 == 1
    return False

def logger(request_name, url, message, color = bcolors.WARNING):
    attr_color = bcolors.OKBLUE
    if appropriate_level(color):
        print(f"{color}{bcolors.UNDERLINE}{bcolors.BOLD}[{request_name}]{bcolors.ENDC}\n\t{attr_color}'url': {bcolors.ENDC}{url}\n\t{attr_color}'message': {bcolors.ENDC}{color}{message}{bcolors.ENDC}\n")