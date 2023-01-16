import os

from helpers.commit_helpers import get_commit_tree
from helpers.app_helpers import get_working_directory

def _get_commit_hash():
    while True:
        commit_hash = input("Provide the first 10 characters of the commit hash: ")
        if len(commit_hash) == 10:
            return commit_hash
        print("Invalid commit hash.")

def checkout():
    commit_hash = _get_commit_hash()
    print("Checking out commit: " + commit_hash)

    commit_file = os.path.join(get_working_directory(), '.suv', 'commits', 'commit-metadata.suv')
    commit_tree, _ = get_commit_tree(commit_file)

    path = []
    if commit_tree.contains(commit_hash):

        root_reached = False
        while not root_reached:
            path.append(commit_tree.get_node(commit_hash))
            parent_commit = commit_tree.parent(commit_hash.tag)

            if parent_commit:
                commit_hash = parent_commit.identifier
            else:
                root_reached = True

    else:
        print("Commit not found.")

    print(path)


