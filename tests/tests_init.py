import unittest

from helpers.test_helpers import CaptureOutput
from functions.init import init

import shutil, os

class TestInit(unittest.TestCase):

    def setUp(self):
        os.environ['DEBUG'] = '0'
        os.environ['TEST'] = '1'

    def tearDown(self):
        shutil.rmtree(os.path.join(os.getcwd(), 'test_working_directory'))

    def test_init(self):
        with CaptureOutput() as output:
            init()

        self.assertTrue(output[0].startswith("Initialized repo at"))
        self.assertTrue(os.path.exists(os.path.join(os.getcwd(), 'test_working_directory')))
        self.assertTrue(os.path.exists(os.path.join(os.getcwd(), 'test_working_directory', '.suv')))
        self.assertTrue(os.path.exists(os.path.join(os.getcwd(), 'test_working_directory', '.suv', 'deltas')))
        self.assertTrue(os.path.exists(os.path.join(os.getcwd(), 'test_working_directory', '.suv', 'head')))
        self.assertTrue(os.path.exists(os.path.join(os.getcwd(), 'test_working_directory', '.suv', 'users')))
        self.assertTrue(os.path.exists(os.path.join(os.getcwd(), 'test_working_directory', '.suv', 'commits')))

    def test_two_init_calls(self):
        with CaptureOutput() as output:
            init()
            init()

        self.assertEqual(len(output), 2)
        self.assertTrue(output[0].startswith("Initialized repo at"))
        self.assertEqual(output[1], "SUV already initialized.")