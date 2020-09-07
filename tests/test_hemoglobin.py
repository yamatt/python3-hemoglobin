import os
import unittest
from unittest.mock import Mock
import tempfile

from hemoglobin.hemoglobin import Config, Hemoglobin


class TestHemoglobin(unittest.TestCase):
    def test_grammarbot_singleton(self):
        test_hemoglobin = Hemoglobin(None, None)
        self.assertIsNone(test_hemoglobin._grammarbot)
        result = test_hemoglobin.grammarbot
        self.assertIsNotNone(test_hemoglobin._grammarbot)
        self.assertEqual(id(result), id(test_hemoglobin.grammarbot))
        self.assertIsInstance(result, Hemoglobin.GRAMMARBOT_CLIENT)

    def test_from_config_cls(self):
        class MockConfig:
            apikey = "test apikey"
            paths = ["test path"]
            language = "test language"

        test_hemoglobin = Hemoglobin.from_config(MockConfig)
        self.assertEqual(test_hemoglobin.paths, MockConfig.paths)
        self.assertEqual(test_hemoglobin.language, MockConfig.language)
        self.assertEqual(test_hemoglobin.apikey, MockConfig.apikey)

    def test_file_walk_single_file(self):
        single_file_path = "samples/example.txt"
        test_hemoglobin = Hemoglobin(None, [single_file_path])
        self.assertEqual(test_hemoglobin.files[0].f.name, single_file_path)

    def test_extension_check(self):
        test_hemoglobin = Hemoglobin(None, None)
        self.assertTrue(test_hemoglobin._extension_ok("file.md"))
        self.assertTrue(test_hemoglobin._extension_ok("/long/path/to/file.md"))
        self.assertFalse(test_hemoglobin._extension_ok("file"))
        self.assertFalse(test_hemoglobin._extension_ok("/long/path/to/file"))
        self.assertFalse(test_hemoglobin._extension_ok("file.odt"))
        self.assertFalse(test_hemoglobin._extension_ok("/long/path/to/file.odt"))

    def test_add_files(self):
        test_hemoglobin = Hemoglobin(None, None)
        self.assertTrue(len(test_hemoglobin._files) == 0)
        with tempfile.NamedTemporaryFile() as temp_file:
            test_hemoglobin._add_file(temp_file.name)
            self.assertTrue(len(test_hemoglobin._files) == 1)
            self.assertIsInstance(
                test_hemoglobin._files[0], test_hemoglobin.HEMOGLOBIN_FILE
            )
            self.assertEqual(test_hemoglobin._files[0].f.name, temp_file.name)

    def test_to_dictionary(self):
        class MockFile:
            MOCK_FILE_DICT = {"foo": "bar"}

            class f:
                # mock file object
                name = "test name"

            @staticmethod
            def to_dict():
                return MockFile.MOCK_FILE_DICT

        test_hemoglobin = Hemoglobin(None, None)
        test_hemoglobin._files = [MockFile]

        self.assertEqual(
            test_hemoglobin.to_dict(), {MockFile.f.name: MockFile.MOCK_FILE_DICT}
        )


class TestHemoglobinWalk(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.mock_claim_file = Mock()

        self.test_hemoglobin = Hemoglobin(None, [self.temp_dir.name])
        self.test_hemoglobin._claim_file = self.mock_claim_file

    def create_file(self, path):
        file_path = os.path.join(self.temp_dir.name, path)
        f = open(file_path, "w")
        f.close()
        return file_path

    def test_no_files(self):
        self.test_hemoglobin._paths_walk()
        self.mock_claim_file.assert_not_called()

    def test_single_file(self):
        file_path = self.create_file("file.txt")
        self.test_hemoglobin._paths_walk()
        self.mock_claim_file.assert_called()
        self.assertTrue(self.mock_claim_file.call_count == 1)

    def test_acceptable_file(self):
        self.create_file("file.txt")
        self.test_hemoglobin._paths_walk()
        self.mock_claim_file.assert_called()
        self.assertTrue(self.mock_claim_file.call_count == 1)

    def test_sub_directory(self):
        temp_sub_dir_name = "subdir"
        temp_sub_dir_path = os.path.join(self.temp_dir.name, temp_sub_dir_name)
        temp_sub_file_path = os.path.join(temp_sub_dir_path, "file.txt")

        os.mkdir(temp_sub_dir_path)

        f = open(temp_sub_file_path, "w")
        f.close()

        self.test_hemoglobin._paths_walk()
        self.mock_claim_file.assert_called()
        self.assertTrue(self.mock_claim_file.call_count == 1)

    def test_mutliple_files(self):
        self.create_file("file1.txt")
        self.create_file("file2.txt")

        self.test_hemoglobin._paths_walk()
        self.mock_claim_file.assert_called()
        self.assertTrue(self.mock_claim_file.call_count == 2)
