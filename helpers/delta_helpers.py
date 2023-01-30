import difflib

def get_delta_from_filename(file_path1:str, file_path2:str) -> list:
    '''Get difference between files.'''

    with open(file_path1, 'r') as file1, open(file_path2, 'r') as file2:
        return get_delta_from_list(file1.readlines(), file2.readlines())

def get_delta_from_list(old:list, new:list) -> list:
    '''Get differences between files as a list of strings.'''

    return [line for line in difflib.unified_diff(old, new)]

def apply_delta(file_content:list, delta:list, revert:bool=False) -> list:
    '''Return the provided list by updating it based on the given delta.'''

    diff_metadata_index = 2 if revert else 1
    insert_flag = '-' if revert else '+'
    remove_flag = '+' if revert else '-'

    net_change = 0
    for line in delta:
        if line.startswith('---') or line.startswith('+++'):
            # unnecessary for file update.
            continue

        elif line.startswith('@@'):
            # track the start index (in file) of a chunk of changes
            chunk_start_index = int(line.split()[diff_metadata_index].split(',')[0][1:])-1+net_change
            chunk_cursor = 0

            # make sure that the last index -1 of the list is not overwritten in case of empty original file
            if chunk_start_index < 0:
                chunk_start_index = 0

        elif line.startswith(insert_flag):
            file_content.insert(chunk_start_index+chunk_cursor, line[1:])
            net_change += 1

            # chunk cursor increases by 1 on insert.
            chunk_cursor += 1

        elif line.startswith(remove_flag):
            file_content.pop(chunk_start_index+chunk_cursor)
            net_change -= 1

            # chunk cursor does not change on remove.

        else:

            # chunk cursor changes on unchanged rows.
            chunk_cursor += 1

    return file_content
