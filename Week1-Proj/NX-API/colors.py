HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = "\033[1m"

def disable():
    HEADER = ''
    OKBLUE = ''
    OKGREEN = ''
    WARNING = ''
    FAIL = ''
    ENDC = ''

def infog( msg):
    return OKGREEN + msg + ENDC

def info( msg):
    return OKBLUE + msg + ENDC

def warn( msg):
    return WARNING + msg + ENDC

def err( msg):
    return FAIL + msg + ENDC