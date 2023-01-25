import os

from helpers.commit_helpers import get_commit_tree, set_current_commit
from helpers.app_helpers import get_working_directory
from helpers.checkout_helpers import update_directory_content, remove_directory_content, get_commit_path

def _get_commit_hash():
    while True:
        commit_hash = input("Provide the first 10 characters of the commit hash: ")
        if len(commit_hash) == 10:
            return commit_hash
        print("Invalid commit hash.")

def checkout(commit_hash_id=""):
    commit_hash_id = _get_commit_hash() if commit_hash_id == "" else commit_hash_id
    print("Checking out commit: " + commit_hash_id)

    commit_file = os.path.join(get_working_directory(), '.suv', 'commits', 'commit-metadata.suv')
    commit_tree, _ = get_commit_tree(commit_file)

    if commit_tree.contains(commit_hash_id):
        commit_path = get_commit_path(commit_hash_id, commit_tree)
        remove_directory_content(get_working_directory())
        update_directory_content(get_working_directory(), commit_path)
        set_current_commit(commit_tree.get_node(commit_hash_id).tag)

    else:
        print("Commit not found.")


