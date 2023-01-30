import os, sys

from helpers.app_helpers import get_working_directory

def _create_file(path, lines):
    '''Create/overwrite a file with provided content in the provided path.'''
    with open(path, 'w+') as file:
        file.writelines(lines)

def commit_1():
    '''Add content for the first commit.'''
    file = os.path.join(get_working_directory(), 'ideas.txt')
    lines = ["1. Characters\n", "2. Plot\n", "3. Setting\n"]

    _create_file(file, lines)

def commit_2():
    '''Add content for the second commit.'''
    file = os.path.join(get_working_directory(), 'ideas.txt')
    lines = ["1. Characters\n", "2. Plot\n", "3. Setting\n", "4. Dialogue\n"]

    _create_file(file, lines)