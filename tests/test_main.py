import unittest

from hemoglobin.__main__ import create_args
from hemoglobin.grammarbot import Language as Languages


class TestGetArgs(unittest.TestCase):
    def run_args(self, args):
        return create_args().parse_args(args.split(" "))

    def test_apikey_defined(self):
        TEST_APIKEY = "testapikey"
        TEST_ARG = f"{TEST_APIKEY} ."
        args = self.run_args(TEST_ARG)
        self.assertEqual(args.apikey, TEST_APIKEY)

    def test_use_json(self):
        args = create_args().parse_args(["--json", "testapikey", "."])
        self.assertTrue(args.use_json_output)
        args = create_args().parse_args(["-j", "testapikey", "."])
        self.assertTrue(args.use_json_output)

    def test_not_use_json(self):
        args = create_args().parse_args(["."])
        self.assertFalse(args.use_json_output)

    def test_paths(self):
        TEST_PATH = "./test_path"
        TEST_ARGS = f"testapikey {TEST_PATH}"
        args = self.run_args(TEST_ARGS)
        self.assertEqual(args.path, [TEST_PATH])

    def test_valid_language(self):
        TEST_LANGUAGE = "en-US"
        TEST_ARG = f"--language {TEST_LANGUAGE} testapikey ."
        args = self.run_args(TEST_ARG)
        self.assertEqual(args.language, Languages(TEST_LANGUAGE))

    def test_apikey_undefined(self):
        TEST_ARG = "."
        args = self.run_args(TEST_ARG)
        self.assertFalse(args.apikey)
