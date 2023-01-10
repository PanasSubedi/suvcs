import os

from suv_data import get_suv_directories

def print_in_color(content_to_print, color, *args, **kwargs):
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

    print(f"{getattr(bcolors, color)}{content_to_print}{bcolors.ENDC}", *args, **kwargs)

def get_file_set(directory):

    file_paths = set()
    for root, directories, files in os.walk(directory):
        directories[:] = [dir for dir in directories if dir != '.suv']
        for file in files:
            file_paths.add(os.path.join(root, file)[len(directory)+1:])
    return file_paths

def check_init(func):
    def wrapper(*args, **kwargs):
        suv_directories = get_suv_directories(get_working_directory())
        for directory in suv_directories:
            if not os.path.exists(suv_directories.get(directory)):
                print("Not a valid SUV repo. Use init to initialize.")
                return
        return func(*args, **kwargs)

    return wrapper

def get_working_directory():
    from dotenv import load_dotenv
    load_dotenv()

    if int(os.getenv('DEBUG', 0)):
        return os.path.join(os.getcwd(), 'working_directory')
    elif int(os.getenv('TEST', 0)):
        return os.path.join(os.getcwd(), 'test_working_directory')
    else:
        return os.path.join(os.getcwd())
