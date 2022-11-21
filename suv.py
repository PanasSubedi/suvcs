marker = "$> "
valid_commands = [
    "exit", "init"
]

from functions.init import init

def exit():
    print("Exiting...")
    return True

if __name__ == '__main__':
    exit_flag = True
    while not exit_flag:
        command = input(marker)
        if command in valid_commands:
            if command == "exit": exit_flag = exit()
            elif command == "init": init()

        else:
            print("Invalid command.")
