import unittest
from unittest.mock import patch

import os, shutil

from functions.init import init
from functions.users import set_author
from functions.branch import branch, add_branch, set_branch

from helpers.test_helpers import CaptureOutput
from helpers.app_helpers import get_working_directory

class TestBranch(unittest.TestCase):
    
    @patch('builtins.input', side_effect=[
        "John Doe", "johndoe@gmail.com",
    ])
    def setUp(self, mock_input):
        os.environ['DEBUG'] = '0'
        os.environ['TEST'] = '1'

        with CaptureOutput() as _:
            init()
            set_author()

    def tearDown(self):
        shutil.rmtree(get_working_directory())

    def test_branch_initially_set_to_main(self):
        with CaptureOutput() as output:
            branch()

        self.assertEqual(len(output), 1)
        self.assertTrue('main' in output[0])

    def test_add_new_branch_from_param(self):
        with CaptureOutput() as output:
            add_branch("main2")

        self.assertEqual(output[0], "Branch added.")

    def test_add_new_duplicate_branch_from_param(self):
        with CaptureOutput() as output:
            add_branch("main2")
            add_branch("main2")

        self.assertEqual(len(output), 2)
        self.assertEqual(output[1], "Branch already exists.")

    @patch('builtins.input', side_effect=[
        "main2", "main2"
    ])
    def test_add_new_duplicate_branch_from_cli(self, mock_input):
        with CaptureOutput() as output:
            add_branch()
            add_branch()

        # output[0] and output[2] contain line
        # 'Branch name must be between 1 and 10 characters and can have no spaces.'
        # preceding input
        self.assertEqual(len(output), 4)
        self.assertEqual(output[1], "Branch added.")
        self.assertEqual(output[3], "Branch already exists.")

    def test_set_branch_from_param(self):
        with CaptureOutput() as output:
            add_branch("main2")
            set_branch("main2")

        self.assertEqual(output[1], "Branch set to main2.")

    @patch('builtins.input', side_effect=["main2"])
    def test_set_added_branch_from_cli(self, mock_input):
        with CaptureOutput() as output:
            add_branch("main2")
            set_branch()

        # output[1] contains line
        # 'Branch name must be between 1 and 10 characters and can have no spaces.'
        # preceding input
        self.assertEqual(output[2], "Branch set to main2.")

    def test_branch_display_on_init(self):
        with CaptureOutput() as output:
            branch()

        # output should start with the code for green color
        self.assertFalse(output[0].startswith("main"))
        self.assertTrue("main" in output[0])

    def test_branch_display_color(self):
        with CaptureOutput() as output:
            add_branch("main2")
            set_branch("main2")
            branch()

        self.assertEqual(output[2], 'main')
        self.assertFalse(output[3].startswith('main2'))
        self.assertTrue('main2' in output[3])
