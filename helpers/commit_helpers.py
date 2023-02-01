import os, shutil
import pickle
from helpers.app_helpers import get_working_directory
from helpers.delta_helpers import apply_delta

from treelib import Tree

def display_commit_tree():
    '''Show the commit tree'''

    commit_metadata_file = os.path.join(get_working_directory(), '.suv', 'commits', 'commit-metadata.suv')
    if os.path.exists(commit_metadata_file):
        with open(commit_metadata_file, 'rb') as file:
            commit_metadata = pickle.load(file)
            commit_metadata.get("tree").show()
    else:
        print("No commit tree.")

def store_commit_tree(commit_file, commit_tree):
    '''Store the given commit tree to a given commit file.'''

    if os.path.exists(commit_file):
        with open(commit_file, 'rb') as file:
            commit_metadata = pickle.load(file)
    else:
        commit_metadata = {}

    commit_metadata["tree"] = commit_tree
    with open(commit_file, 'wb+') as file:
        pickle.dump(commit_metadata, file, protocol=pickle.HIGHEST_PROTOCOL)

def get_commit_tree(commit_file):
    '''Return the commit tree from a given commit metadata file.'''

    if os.path.exists(commit_file):
        with open(commit_file, 'rb') as file:
            commit_metadata = pickle.load(file)
            return commit_metadata.get("tree"), commit_metadata.get("current_commit")
    else:
        return Tree(), None

def add_commit_to_tree(commit_hash):
    '''Get commit tree, add a new commit hash to it, and store the tree back.'''

    commit_metadata_file = os.path.join(get_working_directory(), '.suv', 'commits', 'commit-metadata.suv')
    
    commit_tree, parent_hash = get_commit_tree(commit_metadata_file)

    # use the first ten characters as identifier and the whole commit hash as the tag.
    commit_tree.create_node(commit_hash, commit_hash[:10], parent=parent_hash[:10] if parent_hash else None)
    store_commit_tree(commit_metadata_file, commit_tree)

def get_current_commit():
    commit_metadata_file = os.path.join(get_working_directory(), '.suv', 'commits', 'commit-metadata.suv')
    
    if os.path.exists(commit_metadata_file):
        with open(commit_metadata_file, 'rb') as file:
            commit_metadata = pickle.load(file)
            return commit_metadata.get("current_commit")
    else:
        return None
        
def set_current_commit(commit_hash):
    '''Set current commit to ensure that future commits are a child of the current commit.'''

    commit_metadata_file = os.path.join(get_working_directory(), '.suv', 'commits', 'commit-metadata.suv')
    
    if os.path.exists(commit_metadata_file):
        with open(commit_metadata_file, 'rb') as file:
            commit_metadata = pickle.load(file)
    else:
        commit_metadata = {}

    commit_metadata["current_commit"] = commit_hash

    with open(commit_metadata_file, 'wb+') as file:
        pickle.dump(commit_metadata, file, protocol=pickle.HIGHEST_PROTOCOL)

def get_commit(commit_hash):
    '''Get all the commit data for a given hash.'''
    with open(os.path.join(get_working_directory(), '.suv', 'commits', commit_hash), 'rb') as file:
        commit_data = pickle.load(file)

    return commit_data

def store_commit(commit_data):
    '''Store all the commit data for a commit in a separate commit file named after the hash.'''
    with open(os.path.join(get_working_directory(), '.suv', 'commits', commit_data.get('hash')[:10]), 'wb') as file:
        pickle.dump(commit_data, file, protocol=pickle.HIGHEST_PROTOCOL)

def update_head_at_commit(changes):
    '''Update the head directory with content from the working directory on each commit.'''
    
    new_files, removed_files, changed_files = changes

    for file in new_files:
        file_name = file[0]

        source = os.path.join(get_working_directory(), file_name)
        destination = os.path.join(get_working_directory(), '.suv', 'head', file_name)

        os.makedirs(os.path.dirname(destination), exist_ok=True)
        shutil.copy2(
            os.path.join(source),
            os.path.join(destination)
        )

    for file in removed_files:
        file_name = file[0]
        os.remove(os.path.join(get_working_directory(), '.suv', 'head', file_name))

    for file in changed_files:
        file_name = file[0]
        delta = file[1]

        with open(os.path.join(get_working_directory(), '.suv', 'head', file_name), 'r', encoding='utf-8') as file:
            file_content = file.readlines()
        
        new_file_content = apply_delta(file_content, delta)
        
        with open(os.path.join(get_working_directory(), '.suv', 'head', file_name), 'w', encoding='utf-8') as file:
            file.writelines(new_file_content)