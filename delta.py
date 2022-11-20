import difflib

def get_delta_as_list(old:list, new:list) -> None:
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

if __name__ == '__main__':
    import os

    with open(os.path.join(os.getcwd(), 'test_delta_dummy_files', '1_old.txt'), 'r') as file:
        old_1 = file.readlines()

    with open(os.path.join(os.getcwd(), 'test_delta_dummy_files', '1_new.txt'), 'r') as file:
        new_1 = file.readlines()

    for line in get_delta_as_list(old_1, new_1):
        print(line, end='')
