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

    changed_files = []

    for file in common_files:
        delta = get_delta_from_filename(os.path.join(working_directory, file), os.path.join(head_directory, file))
        if len(delta) != 0:
            changed_files.append((file, delta))

    printed = False
    if len(new_files) > 0:
        printed=True
        print("\nAdded:")
        for file in new_files:
            print_in_color("+ {}".format(file), "OKGREEN")

    if len(removed_files) > 0:
        printed=True
        print("\nRemoved:")
        for file in removed_files:
            print_in_color("- {}".format(file), "FAIL")

    if len(changed_files) > 0:
        printed=True
        print("\nModified:")
        for file_tuple in changed_files:
            print(file_tuple[0])
            for line in file_tuple[1][3:]:
                if line[0] == "+":
                    print_in_color(line, "OKGREEN")
                elif line[0] == "-":
                    print_in_color(line, "FAIL")
                else: print(line)

    if not printed:
        print("No changes")
            