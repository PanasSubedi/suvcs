import unittest

from helpers.test_helpers import CaptureOutput
from helpers.commit_helpers import store_commit, add_commit_to_tree, display_commit_tree, set_current_commit, update_head_at_commit
from helpers.app_helpers import get_working_directory
from functions.diff import diff

from functions.init import init
from functions.commit import _hash_commit

import os, shutil
import pickle

from datetime import datetime

class TestCommit(unittest.TestCase):
    
    def setUp(self):
        os.environ['DEBUG'] = '0'
        os.environ['TEST'] = '1'

        with CaptureOutput() as _:
            init()

    def tearDown(self):
        shutil.rmtree(os.path.join(os.getcwd(), 'test_working_directory'))

    @staticmethod
    def _create_file(file_path, lines):
        with open(file_path, 'w+', encoding="utf-8") as file:
            file.writelines(lines)

    def test_update_head_at_commit(self):
        lines_1 = ["Hello world", "something else"]
        lines_2 = ["Hello world 2"]

        # in working directory
        TestCommit._create_file(os.path.join(get_working_directory(), "created.txt"), lines_1)
        TestCommit._create_file(os.path.join(get_working_directory(), "modified.txt"), lines_1)
        TestCommit._create_file(os.path.join(get_working_directory(), "unchanged.txt"), lines_1)

        # in head
        TestCommit._create_file(os.path.join(get_working_directory(), '.suv', 'head', "modified.txt"), lines_2)
        TestCommit._create_file(os.path.join(get_working_directory(), '.suv', 'head', 'removed.txt'), lines_2)
        TestCommit._create_file(os.path.join(get_working_directory(), '.suv', 'head', 'unchanged.txt'), lines_1)

        with CaptureOutput() as _:
            changes = diff()

        update_head_at_commit(changes)
        new, removed, modified = changes

        for file in new:
            self.assertEqual(file[0], 'created.txt')
            self.assertEqual(len(file[1]), 4)
            self.assertEqual(file[1][2], '@@ -0,0 +1 @@\n')

        for file in removed:
            self.assertEqual(file[0], 'removed.txt')
            self.assertEqual(len(file[1]), 4)
            self.assertEqual(file[1][2], '@@ -1 +0,0 @@\n')

        for file in modified:
            self.assertEqual(file[0], 'modified.txt')
            self.assertEqual(len(file[1]), 5)
            self.assertEqual(file[1][2], '@@ -1 +1 @@\n')


    def test_set_current_commit(self):
        random_hash_1 = _hash_commit("Hello world 1")
        random_hash_2 = _hash_commit("Hello world 2")

        add_commit_to_tree(random_hash_1)
        set_current_commit(random_hash_1)
        add_commit_to_tree(random_hash_2)

        with CaptureOutput() as output:
            display_commit_tree()

        self.assertEqual(len(output), 3)
        self.assertEqual(random_hash_1, output[0])
        self.assertEqual("└── {}".format(random_hash_2), output[1])

    def test_add_commit_to_tree_first_commit(self):
        random_hash_1 = _hash_commit("Hello world")
        add_commit_to_tree(random_hash_1)

        with CaptureOutput() as output:
            display_commit_tree()

        self.assertEqual(random_hash_1, output[0])


    def test_store_commit(self):
        commit_data = {
            'author': {'name': 'John Doe', 'email': 'john@doe.com'},
            'changes': [('file1.txt', []), ('file2.txt', []), ('file3.txt', [])],
            'message': 'Helpful commit message',
            'timestamp': int(datetime.utcnow().timestamp()),
        }
        commit_data['hash'] = _hash_commit(commit_data)

        store_commit(commit_data)

        commit_file = os.path.join(get_working_directory(), '.suv', 'commits', commit_data.get('hash')[:10])
        self.assertTrue(os.path.exists(commit_file))

        with open(commit_file, 'rb') as file:
            commit_data_loaded = pickle.load(file)

        self.assertEqual(commit_data, commit_data_loaded)


