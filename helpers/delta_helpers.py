import difflib

def get_delta_from_filename(file_path1:str, file_path2:str) -> list:
    with open(file_path1, 'r') as file1, open(file_path2, 'r') as file2:
        return get_delta_as_list(file1.readlines(), file2.readlines())

def get_delta_as_list(old:list, new:list) -> list:
    return [line for line in difflib.unified_diff(old, new)]

def apply_delta(file_content:list, delta:list, revert:bool=False) -> list:
    diff_metadata_index = 2 if revert else 1
    insert_flag = '-' if revert else '+'
    remove_flag = '+' if revert else '-'

    net_change = 0
    for line in delta:
        if line.startswith('---') or line.startswith('+++'):
            continue

        elif line.startswith('@@'):
            chunk_start_index = int(line.split()[diff_metadata_index].split(',')[0][1:])-1+net_change
            chunk_cursor = 0

        elif line.startswith(insert_flag):
            file_content.insert(chunk_start_index+chunk_cursor, line[1:])
            net_change += 1
            chunk_cursor += 1

        elif line.startswith(remove_flag):
            file_content.pop(chunk_start_index+chunk_cursor)
            net_change -= 1

        else:
            chunk_cursor += 1

    return file_content
