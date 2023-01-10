import unittest
import os, shutil

from helpers.test_helpers import CaptureOutput
from functions.diff import diff
from functions.init import init

from helpers.app_helpers import get_working_directory

class TestDiff(unittest.TestCase):
    def setUp(self):
        os.environ['DEBUG'] = '0'
        os.environ['TEST'] = '1'

    def tearDown(self):
        shutil.rmtree(get_working_directory())

    def test_diff_overall(self):
        with CaptureOutput() as _:
            init()

        lines_1 = ["Hello world", "something else"]
        lines_2 = ["Hello world 2"]

        # in working directory
        TestDiff._create_file(os.path.join(get_working_directory(), "created.txt"), lines_1)
        TestDiff._create_file(os.path.join(get_working_directory(), "modified.txt"), lines_1)
        TestDiff._create_file(os.path.join(get_working_directory(), "unchanged.txt"), lines_1)

        # in head
        TestDiff._create_file(os.path.join(get_working_directory(), '.suv', 'head', "modified.txt"), lines_2)
        TestDiff._create_file(os.path.join(get_working_directory(), '.suv', 'head', 'removed.txt'), lines_2)
        TestDiff._create_file(os.path.join(get_working_directory(), '.suv', 'head', 'unchanged.txt'), lines_1)

        with CaptureOutput() as output:
            diff()

        self.assertEqual(len(output), 11)
        self.assertEqual(output[1], "Added:")
        self.assertTrue("created.txt" in output[2])
        self.assertEqual(output[4], "Removed:")
        self.assertTrue("removed.txt" in output[5])
        self.assertEqual(output[7], "Modified:")
        self.assertTrue("modified.txt" in output[8])
        self.assertTrue("Hello world" in output[9])
        self.assertTrue("Hello world 2" in output[10])

    def test_diff_file_changed(self):
        with CaptureOutput() as _:
            init()

        lines_1 = ["Hello world", "something else"]
        lines_2 = ["Hello world 2"]

        # in working directory
        TestDiff._create_file(os.path.join(get_working_directory(), "file_1.txt"), lines_1)

        # in head
        TestDiff._create_file(os.path.join(get_working_directory(), '.suv', 'head', "file_1.txt"), lines_2)

        with CaptureOutput() as output:
            diff()

        self.assertEqual(len(output), 5)
        self.assertEqual(output[1], "Modified:")
        self.assertEqual(output[2], "file_1.txt")
        self.assertTrue("-Hello world" in output[3])
        self.assertTrue("+Hello world 2" in output[4])


    def test_diff_file_added(self):
        with CaptureOutput() as _:
            init()

        lines_1 = ["Hello world", "something else"]

        # in working directory
        TestDiff._create_file(os.path.join(get_working_directory(), "file_1.txt"), lines_1)
        TestDiff._create_file(os.path.join(get_working_directory(), "file_2.txt"), lines_1)

        with CaptureOutput() as output:
            diff()

        self.assertEqual(len(output), 4)
        self.assertEqual(output[1], "Added:")
        self.assertTrue("file_1.txt" in output[2] or "file_1.txt" in output[3])
        self.assertTrue("file_2.txt" in output[2] or "file_2.txt" in output[3])

    def test_diff_file_removed(self):
        with CaptureOutput() as _:
            init()

        lines_1 = ["Hello world", "something else"]
        lines_2 = ["Hello world 2"]

        # in working directory
        TestDiff._create_file(os.path.join(get_working_directory(), "file_1.txt"), lines_1)

        # in head
        TestDiff._create_file(os.path.join(get_working_directory(), '.suv', 'head', "file_1.txt"), lines_1)
        TestDiff._create_file(os.path.join(get_working_directory(), '.suv', 'head', 'file_2.txt'), lines_2)

        with CaptureOutput() as output:
            diff()

        self.assertEqual(len(output), 3)
        self.assertEqual(output[1], "Removed:")
        self.assertTrue("file_2.txt" in output[2])

    def test_diff_no_changes(self):

        with CaptureOutput() as _:
            init()

        lines = ["Hello", "world"]
        TestDiff._create_file(os.path.join(get_working_directory(), "file_1.txt"), lines)
        TestDiff._create_file(os.path.join(get_working_directory(), '.suv', 'head', "file_1.txt"), lines)

        with CaptureOutput() as output:
            diff()

        self.assertEqual(len(output), 1)
        self.assertEqual(output[0], "No changes")

    @staticmethod
    def _create_file(file_path, lines):
        with open(file_path, 'w+', encoding="utf-8") as file:
            file.writelines(lines)
        