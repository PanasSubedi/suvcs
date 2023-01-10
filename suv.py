marker = "$> "
valid_commands = [
    "exit", "init", "set author", "author", "diff",
    "status", "add", "commit"
]

from functions.init import init
from functions.users import set_author, get_author
from functions.diff import diff
from functions.commit import add, commit

def exit():
    print("Exiting...")
    return True

if __name__ == '__main__':
    exit_flag = False
    while not exit_flag:
        command = input(marker)
        if command in valid_commands:
            if command == "exit": exit_flag = exit()
            elif command == "init": init()
            elif command == "set author": set_author()
            elif command == "author": get_author(display=True)
            elif command in ("diff", "status"): diff()
            elif command == "add": add()
            elif command == "commit": commit()

        else:
            print("Invalid command.")
