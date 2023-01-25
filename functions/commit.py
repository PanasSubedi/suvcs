from functions.diff import diff
from functions.users import get_author

from helpers.app_helpers import check_init, get_working_directory
from helpers.commit_helpers import update_head_at_commit, store_commit, add_commit_to_tree, set_current_commit
from helpers.branch_helpers import get_branch_data, store_branch_data

import json

from hashlib import sha256
from datetime import datetime

def _hash_commit(commit_data):
    commit_string = json.dumps(commit_data, sort_keys=True)
    return sha256(commit_string.encode('utf-8')).hexdigest()

@check_init
def commit():

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
        print("No changes to commit.")
    else:
        commit_data = {
            'author': author,
            'changes': changes,
            'message': message,
        }
        commit_hash = _hash_commit(commit_data)

        commit_data['hash'] = commit_hash
        commit_data['timestamp'] = int(datetime.utcnow().timestamp())

        branch_data = get_branch_data()
        branch_data[branch_data['current_branch']]['commits'].append(commit_hash)
        
        store_branch_data(branch_data)
        store_commit(commit_data)
        add_commit_to_tree(commit_hash)
        set_current_commit(commit_hash)
        update_head_at_commit(changes)