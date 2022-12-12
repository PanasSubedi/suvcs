import unittest

from helpers.test_helpers import CaptureOutput
from suv import exit

class TestSUVCLI(unittest.TestCase):

    def test_exit(self):
        with CaptureOutput() as output:
            exit_output = exit()

        self.assertEqual(len(output), 1)
        self.assertTrue(output[0].startswith('Exiting'))
        self.assertTrue(exit_output)