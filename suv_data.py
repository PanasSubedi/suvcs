import os

suv_directories = {
    'suv': os.path.join('.suv'),
    'head': os.path.join('.suv', 'head'),
    'deltas': os.path.join('.suv', 'deltas'),
    'users': os.path.join('.suv', 'users'),
    'stage': os.path.join('.suv', 'stage'),
}

def get_suv_directories(working_directory):
    directories = {}
    directories['working'] = working_directory
    for directory in suv_directories:
        directories[directory] = os.path.join(working_directory, suv_directories.get(directory))

    return directories