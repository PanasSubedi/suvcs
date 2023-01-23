marker = "$> "
valid_commands = [
    "exit", "init", "set author", "author", "diff",
    "status", "commit", "checkout", "branch", "set branch",
    "add branch"
]

from functions.init import init
from functions.users import set_author, get_author
from functions.diff import diff
from functions.commit import commit
from functions.checkout import checkout
from functions.branch import branch, set_branch, add_branch

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
            elif command == "checkout": checkout()
            elif command in ("diff", "status"): diff()
            elif command == "commit": commit()
            elif command == "branch": branch()
            elif command == "set branch": set_branch()
            elif command == "add branch": add_branch()

        else:
            print("Invalid command.")
