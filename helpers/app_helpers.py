import os

from suv_data import get_suv_directories

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
