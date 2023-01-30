# SuVCS - A simple version control system

SuVCS is a simple version control system made as a personal project to understand how version control systems work.

## Use

### Requirements

1. Python 3
2. future==0.18.3
3. python-dotenv==0.21.1
4. treelib==1.6.1

### Initialization

1. ```python3 suv.py```
2. ```init```

The ```init``` command creates a ```working directory``` folder in the current directory. SuVCS keeps a track of all the files within that directory.

### Available commands

Use ```python3 suv.py``` to start the version control system. After using ```init```, you can use the following commands at the moment:

#### exit

Exit the system.

#### set author

Set the current author of the project. You can set a **name** and an **email address**.

#### author

Displays the current author of the project. Shows nothing if no author is set.

#### diff

Displays changes in the working directory. Changes are grouped into **New**, **Removed**, and **Updated**. For new and removed files, SuVCS only lists them. For the updated files, it also displays the changed lines.

Displays **No changes** if there are no changes.

#### status

Same as **diff** at the moment.

#### commit

Asks for a commit message and stores all current changes as a commit.

- Displays **No changes to commit.** if there are no changes.
- Displays **Author not set.** if author is not set.

#### checkout

Asks for the first 10 characters of a commit hash and updates the working directory to contain the content present during the provided commit.

- Displays **Commit not found.** if the input commit hash is invalid.

## Testing

Use ```python3 test.py``` to perform unit tests. Each external function is covered by unit tests. Internal functions are not covered because they get called during the execution of external functions anyway.