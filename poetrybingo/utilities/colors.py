import sys, os

sys.path.insert(0, "poetrybingo/data")

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
    return f"{bcolors.HEADER}{string}" + "{bcolors.ENDC}"

def BLUE(string):
    return f"{bcolors.OKBLUE}{string}" + "{bcolors.ENDC}"

def CYAN(string):
    return f"{bcolors.OKCYAN}{string}" + "{bcolors.ENDC}"

def GREEN(string):
    return f"{bcolors.OKGREEN}{string}" + "{bcolors.ENDC}"

def WARNING(string):
    return f"{bcolors.WARNING}{string}" + "{bcolors.ENDC}"

def FAIL(string):
    return f"{bcolors.FAIL}{string}" + "{bcolors.ENDC}"

def BOLD(string):
    return f"{bcolors.BOLD}{string}" + "{bcolors.ENDC}"

def UNDERLINE(string):
    return f"{bcolors.UNDERLINE}{string}" + "{bcolors.ENDC}"