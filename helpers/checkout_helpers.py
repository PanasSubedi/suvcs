import os, shutil

from helpers.delta_helpers import apply_delta
from helpers.commit_helpers import get_commit

def update_directory_content(directory, commits):
    '''Update an empty directory based on a list of commit hashes.'''

    for commit_hash in commits:
        commit_data = get_commit(commit_hash)
        new_files, removed_files, changed_files = commit_data.get('changes')

        for file_tuple in new_files:
            file_path = os.path.join(directory, file_tuple[0])
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            new_file_content = apply_delta([], file_tuple[1])
            with open(file_path, 'w+', encoding='utf-8') as file:
                file.writelines(new_file_content)

        for file_tuple in removed_files:
            os.remove(os.path.join(directory, file_tuple[0]))

        for file_tuple in changed_files:
            file_path = os.path.join(directory, file_tuple[0])
            with open(file_path, 'r', encoding='utf-8') as file:
                file_content = file.readlines()

            new_file_content = apply_delta(file_content, file_tuple[1])
            with open(file_path, 'w', encoding='utf-8') as file:
                file.writelines(new_file_content)

def remove_directory_content(directory):
    '''Empty a directory.'''

    for file_dir in os.listdir(directory):
        file_path = os.path.join(directory, file_dir)
        if file_dir == '.suv':
            continue
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
        else:
            os.remove(file_path)

def get_commit_path(commit_hash_id, commit_tree):
    '''Get the path to a commit in a given commit tree. Works by always following the parent.'''

    path = []
    root_reached = False

    while not root_reached:
        path.insert(0, commit_hash_id)
        parent_commit = commit_tree.parent(commit_hash_id)

        if parent_commit:
            commit_hash_id = parent_commit.identifier
        else:
            root_reached = True

    return path