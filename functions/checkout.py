import os

from helpers.commit_helpers import get_commit_tree, set_current_commit
from helpers.app_helpers import get_working_directory
from helpers.checkout_helpers import update_directory_content, remove_directory_content, get_commit_path

def _get_commit_hash_input():
    '''Get the first 10 characters of a commit hash as user input'''

    while True:
        commit_hash = input("Provide the first 10 characters of the commit hash: ")
        if len(commit_hash) == 10:
            return commit_hash
        print("Invalid commit hash.")

def checkout():
    '''Asks user for the first 10 characters of a commit hash
    and checks out the commit for valid hashes'''

    commit_hash_id = _get_commit_hash_input()
    print("Checking out commit: " + commit_hash_id)

    commit_file = os.path.join(get_working_directory(), '.suv', 'commits', 'commit-metadata.suv')
    commit_tree, _ = get_commit_tree(commit_file)

    if commit_tree.contains(commit_hash_id):
        # if commit tree contains input,
        # - find path from root to the input
        # - remove all content in the working directory
        # - update content in the working directory
        #   based on the path
        
        commit_path = get_commit_path(commit_hash_id, commit_tree)
        remove_directory_content(get_working_directory())
        update_directory_content(get_working_directory(), commit_path)

        # set current commit to the provided hash so
        # that future commits branch from this one
        set_current_commit(commit_hash_id)

    else:
        print("Commit not found.")


