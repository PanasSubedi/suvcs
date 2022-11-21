import os

def create_directory(directory):
    if not os.path.exists(directory):
        os.mkdir(directory)
        return True
    return False

def create_directory_structure():
    working_directory = get_working_directory()
    directories = {
        'working': working_directory,
        'suv': os.path.join(working_directory, '.suv'),
        'head': os.path.join(working_directory, '.suv', 'head'),
        'deltas': os.path.join(working_directory, '.suv', 'deltas'),
        'users': os.path.join(working_directory, '.suv', 'users')
    }

    directories_created = False
    for directory in directories:
        directories_created = create_directory(directories.get(directory)) or directories_created

    if directories_created:
        return True, working_directory
    else:
        return False, None

def get_working_directory():

    from dotenv import load_dotenv
    load_dotenv()

    if int(os.getenv('DEBUG', 0)):
        return os.path.join(os.getcwd(), 'working_directory')
    elif int(os.getenv('TEST', 0)):
        return os.path.join(os.getcwd(), 'test_working_directory')
    else:
        return os.path.join(os.getcwd())

def init():
    directories_created, working_directory = create_directory_structure()

    if directories_created:
        print("Initialized repo at {}".format(working_directory))
    else:
        print("SUV already initialized.")
