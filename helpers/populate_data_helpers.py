import os, sys

from helpers.app_helpers import get_working_directory

def _create_file(path, lines):
    with open(path, 'w+') as file:
        file.writelines(lines)

def commit_1():
    file = os.path.join(get_working_directory(), 'ideas.txt')
    lines = ["1. Characters\n", "2. Plot\n", "3. Setting\n"]

    _create_file(file, lines)

def commit_2():
    file = os.path.join(get_working_directory(), 'ideas.txt')
    lines = ["1. Characters\n", "2. Plot\n", "3. Setting\n", "4. Dialogue\n"]

    _create_file(file, lines)