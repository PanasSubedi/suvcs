import os

import unittest

from delta import get_delta_as_list

class TestDelta(unittest.TestCase):

    @staticmethod
    def _get_delta(filename1:str, filename2:str) -> list:
        with open(os.path.join(os.getcwd(), 'test_delta_dummy_files', filename1), 'r') as file:
            file1 = file.readlines()
        with open(os.path.join(os.getcwd(), 'test_delta_dummy_files', filename2), 'r') as file:
            file2 = file.readlines()
        return get_delta_as_list(file1, file2)

    def test_get_delta_as_list_1(self):
        delta = TestDelta._get_delta('1.txt', '2.txt')

        self.assertEqual(len(delta), 4)
        self.assertEqual(delta[2].strip(), '@@ -0,0 +1 @@')
        self.assertTrue(delta[3].strip().startswith('+'))

    def test_get_delta_as_list_2(self):
        delta = TestDelta._get_delta('2.txt', '3.txt')

        self.assertEqual(len(delta), 5)
        self.assertEqual(delta[2].strip(), '@@ -1 +1 @@')
        self.assertTrue(delta[3].startswith('-'))
        self.assertTrue(delta[4].startswith('+'))
        self.assertEqual(delta[3].strip(), '-Hello world')
        self.assertEqual(delta[4].strip(), '+Hello world is better than Lorem Ipsum')

    def test_get_delta_as_list_3(self):
        delta = TestDelta._get_delta('3.txt', '4.txt')

        self.assertEqual(len(delta), 6)
        self.assertTrue(delta[4].startswith('+'))
        self.assertTrue(delta[5].startswith('+'))

    def test_get_delta_as_list_4(self):
        delta = TestDelta._get_delta('4.txt', '5.txt')

        for line in delta:
            print(line, end='')

        self.assertEqual(len(delta), 6)
        self.assertTrue(delta[3].startswith('-'))
        self.assertTrue(delta[4].startswith('-'))




if __name__ == '__main__':
    unittest.main()
