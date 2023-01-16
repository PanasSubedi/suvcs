import sys

from helpers.populate_data_helpers import commit_1, commit_2

if __name__ == "__main__":
    inputs = sys.argv[1:]
    if len(inputs) == 0:
        print("Please provide a commit number.")
    else:
        commit_number = inputs[0]
        if commit_number == "1":
            commit_1()
        elif commit_number == "2":
            commit_2()
        else:
            print("Invalid commit number.")