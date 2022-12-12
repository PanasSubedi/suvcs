import unittest
from unittest.mock import patch

from functions.users import set_author, get_author
from functions.init import init

from helpers.test_helpers import CaptureOutput

import os, shutil

class TestAuthors(unittest.TestCase):

    def setUp(self) -> None:
        os.environ['DEBUG'] = '0'
        os.environ['TEST'] = '1'

        with CaptureOutput() as _:
            init()

    def tearDown(self) -> None:
        for root, dirs, _ in os.walk(os.path.join(os.getcwd(), 'test_working_directory'), topdown=False):
            for directory_name in dirs:
                shutil.rmtree(os.path.join(root, directory_name), ignore_errors=False, onerror=None)
        os.rmdir(os.path.join(os.getcwd(), 'test_working_directory'))

    @patch('builtins.input', side_effect=['John', 'john@bar.com'])
    def test_set_author(self, mock_input) -> None:
        with CaptureOutput() as output:
            set_author()
            get_author(display=True)

        self.assertEqual(output[0], 'Author updated.')
        self.assertEqual(output[1], 'Name: John')
        self.assertEqual(output[2], 'Email: john@bar.com')

    @patch('builtins.input', side_effect=['John', 'john@bar.com', 'n'])
    def test_set_author_twice_overwrite_no(self, mock_input) -> None:
        with CaptureOutput() as output:
            set_author()
            get_author(display=True)
            set_author()
            get_author(display=True)

        self.assertEqual(output[0], 'Author updated.')
        self.assertEqual(output[1], 'Name: John')
        self.assertEqual(output[2], 'Email: john@bar.com')
        self.assertEqual(output[3], 'Author unchanged.')
        self.assertEqual(output[4], 'Name: John')
        self.assertEqual(output[5], 'Email: john@bar.com')

    @patch('builtins.input', side_effect=['John', 'john@bar.com', 'y', 'John Doe', 'johndoe@foobar.com'])
    def test_set_author_twice_overwrite_yes(self, mock_input) -> None:
        with CaptureOutput() as output:
            set_author()
            get_author(display=True)
            set_author()
            get_author(display=True)
        self.assertEqual(output[0], 'Author updated.')
        self.assertEqual(output[1], 'Name: John')
        self.assertEqual(output[2], 'Email: john@bar.com')
        self.assertEqual(output[3], 'Author updated.')
        self.assertEqual(output[4], 'Name: John Doe')
        self.assertEqual(output[5], 'Email: johndoe@foobar.com')