from functions.diff import diff
from functions.users import get_author
from helpers.app_helpers import check_init, get_working_directory
from helpers.commit_helpers import update_head_at_commit, store_commit, add_commit_to_tree, set_current_commit

import json

from hashlib import sha256
from datetime import datetime

def _hash_commit(commit_data):
    '''Provides a hash value for a given commit'''
    commit_string = json.dumps(commit_data, sort_keys=True)
    return sha256(commit_string.encode('utf-8')).hexdigest()

@check_init
def commit():
    '''Stores a new commit if the working directory has been updated'''

    author = get_author()
    if not author:
        print("Author not set.")
        return

    valid_input = False
    while not valid_input:
        message = input("Commit message: ")
        if len(message) > 0:
            valid_input = True

    changes = diff()
    if sum([len(change_list) for change_list in changes]) == 0:
        # changes has 'new', 'updated', and 'deleted' tuples
        # if the sum of their lengths is 0, there are no changes
        print("No changes to commit.")

    else:
        commit_data = {
            'author': author,
            'changes': changes,
            'message': message,
        }
        commit_hash = _hash_commit(commit_data)
        
        # timestamp added after hashing to make hash value
        # consistent and replicable
        commit_data['timestamp'] = int(datetime.utcnow().timestamp())
        commit_data['hash'] = commit_hash

        store_commit(commit_data)
        add_commit_to_tree(commit_hash)
        set_current_commit(commit_hash)
        update_head_at_commit(changes)