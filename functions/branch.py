from helpers.commit_helpers import get_current_commit
from helpers.branch_helpers import get_branch_data, store_branch_data

def branch():
    branch_data = get_branch_data()

    if len(branch_data.keys()) == 0:
        print("No branches.")
    else:
        for branch in branch_data:
            print(branch)

def set_branch():
    pass

def _get_branch_name(branch_name):
    while True:

        if len(branch_name) < 1 or len(branch_name) > 10 or " " in branch_name:
            print("Branch name must be between 1 and 10 characters and can have no spaces.")
            branch_name = input("Enter a branch name: ")
        else:
            return branch_name

def add_branch(branch_name=""):
    new_branch = _get_branch_name(branch_name)
    branch_data = get_branch_data()

    if new_branch in branch_data:
        print("Branch already exists.")
    else:
        branch_data[new_branch] = get_current_commit()
        store_branch_data(branch_data)
        print("Branch added.")