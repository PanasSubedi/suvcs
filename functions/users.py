import os, pickle
from helpers.app_helpers import get_working_directory, check_init

@check_init
def get_author(display=False):
    author_file_path = os.path.join(get_working_directory(), '.suv', 'users', 'author.suvd')
    if os.path.exists(author_file_path):
        with open(author_file_path, 'rb') as file:
            author = pickle.load(file)
        if len(author) == 2:
            if display:
                print("Name: {}\nEmail: {}".format(author[0], author[1]))
                return
            return author
        else:
            return None
    else:
        return None

@check_init
def set_author():
    author = get_author()
    if author is not None:
        choice = _get_overwrite_choice(author)
    else:
        choice = True

    if choice:
        name_and_email = _get_name_and_email()
        author_file_path = os.path.join(get_working_directory(), '.suv', 'users', 'author.suvd')
        with open(author_file_path, 'wb+') as file:
            pickle.dump(name_and_email, file, protocol=pickle.HIGHEST_PROTOCOL)
        print("Author updated.")

    else:
        print("Author unchanged.")

def _get_overwrite_choice(author):
    valid_choice = False
    while not valid_choice:
        choice = input("Author already set as:\nName: {}\nEmail: {}\n\nOverwrite? (Y/N) ".format(author[0], author[1]))

        if choice[0].lower() in ('y', 'n'):
            valid_choice = True

    return choice == 'y'

def _get_name_and_email():
    import re
    def check_name_validity(name):
        name_regex = re.compile(r'[a-zA-Z ]+')
        return re.fullmatch(name_regex, name)

    def check_email_validity(email):
        email_regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        return re.fullmatch(email_regex, email)

    valid_inputs = False
    while not valid_inputs:
        name = input("Enter name of the author: ")
        email = input("Enter email address of the author: ")

        if check_name_validity(name.strip()) and check_email_validity(email.strip()):
            valid_inputs = True
        else:
            print("Invalid input. Please try again.")

    return name, email
