import os

import unittest

from helpers.delta_helpers import get_delta_as_list, apply_delta

class TestApplyDelta(unittest.TestCase):

    @staticmethod
    def _get_delta(filename1:str, filename2:str) -> list:
        with open(os.path.join(os.getcwd(), 'test_delta_dummy_files', filename1), 'r') as file:
            file1 = file.readlines()
        with open(os.path.join(os.getcwd(), 'test_delta_dummy_files', filename2), 'r') as file:
            file2 = file.readlines()
        return get_delta_as_list(file1, file2)

    def test_apply_delta(self):
        delta = TestApplyDelta._get_delta('3.txt', '4.txt')
        with open(os.path.join(os.getcwd(), 'test_delta_dummy_files', '3.txt'), 'r') as file:
            file_content = file.readlines()

        self.assertEqual(len(file_content), 1)
        self.assertTrue(file_content[0].startswith("Hello world"))
        apply_delta(file_content, delta)
        self.assertEqual(len(file_content), 3)
        self.assertTrue(file_content[-1].startswith("Sometimes"))

    def test_apply_delta_revert(self):
        delta = TestApplyDelta._get_delta('3.txt', '4.txt')
        with open(os.path.join(os.getcwd(), 'test_delta_dummy_files', '4.txt'), 'r') as file:
            file_content = file.readlines()

        self.assertEqual(len(file_content), 3)
        self.assertTrue(file_content[-1].startswith("Sometimes"))
        apply_delta(file_content, delta, revert=True)
        self.assertEqual(len(file_content), 1)
        self.assertTrue(file_content[0].startswith("Hello world"))


class TestGetDeltaAsList(unittest.TestCase):

    @staticmethod
    def _get_delta(filename1:str, filename2:str) -> list:
        with open(os.path.join(os.getcwd(), 'test_delta_dummy_files', filename1), 'r') as file:
            file1 = file.readlines()
        with open(os.path.join(os.getcwd(), 'test_delta_dummy_files', filename2), 'r') as file:
            file2 = file.readlines()
        return get_delta_as_list(file1, file2)

    def test_get_delta_as_list_1(self):
        delta = TestGetDeltaAsList._get_delta('1.txt', '2.txt')

        self.assertEqual(len(delta), 4)
        self.assertEqual(delta[2].strip(), '@@ -0,0 +1 @@')
        self.assertTrue(delta[3].strip().startswith('+'))

    def test_get_delta_as_list_2(self):
        delta = TestGetDeltaAsList._get_delta('2.txt', '3.txt')

        self.assertEqual(len(delta), 5)
        self.assertEqual(delta[2].strip(), '@@ -1 +1 @@')
        self.assertTrue(delta[3].startswith('-'))
        self.assertTrue(delta[4].startswith('+'))
        self.assertEqual(delta[3].strip(), '-Hello world')
        self.assertEqual(delta[4].strip(), '+Hello world is better than Lorem Ipsum')

    def test_get_delta_as_list_3(self):
        delta = TestGetDeltaAsList._get_delta('3.txt', '4.txt')

        self.assertEqual(len(delta), 6)
        self.assertTrue(delta[4].startswith('+'))
        self.assertTrue(delta[5].startswith('+'))

    def test_get_delta_as_list_4(self):
        delta = TestGetDeltaAsList._get_delta('4.txt', '5.txt')

        self.assertEqual(len(delta), 6)
        self.assertTrue(delta[3].startswith('-'))
        self.assertTrue(delta[4].startswith('-'))