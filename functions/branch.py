from helpers.commit_helpers import get_current_commit, set_current_commit
from helpers.branch_helpers import get_branch_data, store_branch_data
from helpers.app_helpers import print_in_color

from functions.checkout import checkout

def branch():
    branch_data = get_branch_data()

    if len(branch_data.keys()) == 0:
        print("No branches.")
    else:
        for branch in branch_data:
            if branch == "current_branch": continue

            if branch == branch_data.get("current_branch"):
                print_in_color("* {}".format(branch), "OKGREEN")
            else:
                print(branch)

def set_branch(branch_name=""):
    branch_data = get_branch_data()
    branch_name = _get_branch_name(branch_name)

    if len(branch_data.keys()) == 0:
        print("No branches.")
    else:
        if branch_name in branch_data:
            branch_data["current_branch"] = branch_name
            store_branch_data(branch_data)

            if len(branch_data[branch_name]['commits']) != 0:
                set_current_commit(branch_data[branch_name]['commits'][-1])
                checkout(branch_data[branch_name]['commits'][-1][:10])
            print("Branch set to {}.".format(branch_name))
        else:
            print("Branch does not exist.")

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
        current_commit = get_current_commit()
        if current_commit is None:
            commits = []
        else:
            commits = [current_commit, ]
            
        branch_data[new_branch] = {}
        branch_data[new_branch]['commits'] = commits
        store_branch_data(branch_data)
        print("Branch added.")