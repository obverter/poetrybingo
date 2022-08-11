import sys, os

sys.path.append(os.path.join(sys.path[0], "poetrybingo", "utilities"))
sys.path.append(os.path.join(sys.path[0], "poetrybingo", "data"))
sys.path.append(os.path.join(sys.path[0], "poetrybingo", "modules"))


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def HEADER(string):
    return f"{bcolors.HEADER}{string}"


def BLUE(string):
    return f"{bcolors.OKBLUE}{string}"


def CYAN(string):
    return f"{bcolors.OKCYAN}{string}"


def GREEN(string):
    return f"{bcolors.OKGREEN}{string}"


def WARNING(string):
    return f"{bcolors.WARNING}{string}"


def FAIL(string):
    return f"{bcolors.FAIL}{string}"


def BOLD(string):
    return f"{bcolors.BOLD}{string}"


def UNDERLINE(string):
    return f"{bcolors.UNDERLINE}{string}"


def ENDC():
    return f"{bcolors.ENDC}"
