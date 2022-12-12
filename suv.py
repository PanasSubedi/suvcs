marker = "$> "
valid_commands = [
    "exit", "init", "set author", "author"
]

from functions.init import init
from functions.users import set_author, get_author

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

        else:
            print("Invalid command.")
