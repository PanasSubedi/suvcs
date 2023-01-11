import os, shutil
import pickle
from helpers.app_helpers import get_working_directory
from helpers.delta_helpers import apply_delta

from treelib import Tree

def display_commit_tree():
    commit_metadata_file = os.path.join(get_working_directory(), '.suv', 'commits', 'commit-metadata.suv')
    if os.path.exists(commit_metadata_file):
        with open(commit_metadata_file, 'rb') as file:
            commit_metadata = pickle.load(file)
            commit_metadata.get("tree").show()
    else:
        print("No commit tree.")

def store_commit_tree(commit_file, commit_tree):
    if os.path.exists(commit_file):
        with open(commit_file, 'rb') as file:
            commit_metadata = pickle.load(file)
    else:
        commit_metadata = {}

    commit_metadata["tree"] = commit_tree
    with open(commit_file, 'wb+') as file:
        pickle.dump(commit_metadata, file, protocol=pickle.HIGHEST_PROTOCOL)

def get_commit_tree(commit_file):
    if os.path.exists(commit_file):
        with open(commit_file, 'rb') as file:
            commit_metadata = pickle.load(file)
            return commit_metadata.get("tree"), commit_metadata.get("current_commit")
    else:
        return Tree(), None

def add_commit_to_tree(commit_hash):
    commit_metadata_file = os.path.join(get_working_directory(), '.suv', 'commits', 'commit-metadata.suv')
    
    commit_tree, parent_hash = get_commit_tree(commit_metadata_file)
    commit_tree.create_node(commit_hash, commit_hash, parent=parent_hash)
    store_commit_tree(commit_metadata_file, commit_tree)

def set_current_commit(commit_hash):
    commit_metadata_file = os.path.join(get_working_directory(), '.suv', 'commits', 'commit-metadata.suv')
    
    if os.path.exists(commit_metadata_file):
        with open(commit_metadata_file, 'rb') as file:
            commit_metadata = pickle.load(file)
    else:
        commit_metadata = {}

    commit_metadata["current_commit"] = commit_hash

    with open(commit_metadata_file, 'wb+') as file:
        pickle.dump(commit_metadata, file, protocol=pickle.HIGHEST_PROTOCOL)

def store_commit(commit_data):
    with open(os.path.join(get_working_directory(), '.suv', 'commits', commit_data.get('hash')), 'wb') as file:
        pickle.dump(commit_data, file, protocol=pickle.HIGHEST_PROTOCOL)

def update_head_at_commit(changes):
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
        
        for line in new_file_content:
            print(line)
        with open(os.path.join(get_working_directory(), '.suv', 'head', file_name), 'w', encoding='utf-8') as file:
            file.writelines(new_file_content)