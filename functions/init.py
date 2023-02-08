import os

from helpers.app_helpers import get_working_directory
from functions.branch import add_branch, set_branch
from suv_data import get_suv_directories

def create_directory(directory):
    '''Create directory if it does not exist.'''

    if not os.path.exists(directory):
        os.mkdir(directory)
        return True
    return False

def create_directory_structure():
    '''Create the initial directory structure.'''

    working_directory = get_working_directory()
    directories = get_suv_directories(working_directory)
    directories_created = False

    for directory in directories:
        # check if at least one directory is created.
        directories_created = create_directory(directories.get(directory)) or directories_created

    if directories_created:
        return True, working_directory
    else:
        return False, None

def init(verbose=True):
    '''Creates the .suv directory and the default folders as a mark of suv initialization.'''
    
    directories_created, working_directory = create_directory_structure()

    if directories_created:
        print("Initialized repo at {}".format(working_directory))
        add_branch("main")
        set_branch("main")
    elif verbose:
        print("SUV already initialized.")
