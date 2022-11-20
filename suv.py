marker = "$> "
valid_commands = [
    "exit"
]

def exit():
    print("Exiting...")
    return True

if __name__ == '__main__':

    exit_flag = False
    while not exit_flag:
        command = input(marker)
        if command in valid_commands:
            if command == "exit": exit_flag = exit()

        else:
            print("Invalid command.")
