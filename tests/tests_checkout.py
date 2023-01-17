import unittest
from unittest.mock import patch

import os, shutil

from helpers.app_helpers import get_working_directory, testinput
from helpers.test_helpers import CaptureOutput

from functions.checkout import _get_commit_hash, checkout
from functions.users import set_author
from functions.init import init
from functions.commit import commit

class TestCheckout(unittest.TestCase):
    
    @patch('builtins.input', side_effect=[
        "John Doe", "johndoe@gmail.com",
        "commit message 1: added file_1.txt with 1 line",
        "commit message 2: added a third line to file_1.txt",
    ])
    def setUp(self, mock_input):
        os.environ['DEBUG'] = '0'
        os.environ['TEST'] = '1'

        with CaptureOutput() as _:
            init()
            set_author()
        
        first_lines = ["1. This is line 1", "2. This is line 2"]
        second_lines = ["1. This is line 1", "2. This is line 2", "3. This is line 3"]

        TestCheckout._create_file(os.path.join(get_working_directory(), "file_1.txt"), first_lines)
        with CaptureOutput() as _:
            commit()

        TestCheckout._create_file(os.path.join(get_working_directory(), "file_1.txt"), second_lines)
        with CaptureOutput() as _:
            commit()

    def tearDown(self):
        shutil.rmtree(get_working_directory())

    @staticmethod
    def _create_file(file_path, lines):
        with open(file_path, 'w+', encoding="utf-8") as file:
            file.writelines(lines)

    @patch('builtins.input', side_effect=['', '123', '12345678902', '1234567890'])
    def test__get_commit_hash(self, mock_input):
        
        with CaptureOutput() as output:
            input_hash = _get_commit_hash()

        self.assertEqual(len(output), 3)
        self.assertEqual(output[0], output[1], output[2])
        self.assertEqual(input_hash, '1234567890')

    def test_checkout(self, mock_input):
        pass

        

