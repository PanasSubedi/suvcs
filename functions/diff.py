import os

from helpers.app_helpers import get_working_directory, check_init, get_file_set, print_in_color
from helpers.delta_helpers import get_delta_from_filename

@check_init
def diff():
    working_directory = get_working_directory()
    head_directory = os.path.join(working_directory, '.suv', 'head')

    files_in_working_directory = get_file_set(working_directory)
    files_in_head = get_file_set(head_directory)

    new_files = files_in_working_directory - files_in_head
    removed_files = files_in_head - files_in_working_directory
    common_files = files_in_working_directory.intersection(files_in_head)

    unchanged_files = []
    change_files = []

    for file in common_files:
        print(file)
        delta = get_delta_from_filename(os.path.join(working_directory, file), os.path.join(head_directory, file))

        if len(delta) == 0:
            unchanged_files.append(file)
        else:
            change_files.append(file)
            

    '''print("Status: ")
    print("Currently on branch main")
    print()
    print("Added: ")

    for file in new_files:
        print_in_color("+ {}".format(file), "OKGREEN")

    print()
    print("Removed: ")
    for file in removed_files:
        print_in_color("- {}".format(file), "FAIL")'''

    
