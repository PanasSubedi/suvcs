import os
import pickle

from helpers.app_helpers import get_working_directory

def get_branch_data():
    branch_metadata_file = os.path.join(get_working_directory(), '.suv', 'branches', 'branch-metadata.suv')
    if os.path.exists(branch_metadata_file):
        with open(branch_metadata_file, 'rb') as file:
            return pickle.load(file)
    return {}

def store_branch_data(branch_data):
    with open(os.path.join(get_working_directory(), '.suv', 'branches', 'branch-metadata.suv'), 'wb+') as file:
        pickle.dump(branch_data, file, protocol=pickle.HIGHEST_PROTOCOL)