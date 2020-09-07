import unittest

from argparse import ArgumentError

from hemoglobin.__main__ import create_args
from hemoglobin.grammarbot import Language as Languages


class TestGetArgs(unittest.TestCase):
    def run_args(self, args):
        return create_args().parse_args(args.split(" "))

    def test_apikey_defined(self):
        TEST_APIKEY = "testapikey"
        TEST_ARG = "{apikey} .".format(apikey=TEST_APIKEY)
        args = self.run_args(TEST_ARG)
        self.assertEqual(args.apikey, TEST_APIKEY)

    def test_use_json(self):
        args = create_args().parse_args("--json testapikey .".split(" "))
        self.assertTrue(args.use_json_output)
        args = create_args().parse_args("-j testapikey .".split(" "))
        self.assertTrue(args.use_json_output)

    def test_not_use_json(self):
        args = create_args().parse_args(".".split(" "))
        self.assertFalse(args.use_json_output)

    def test_paths(self):
        TEST_PATH = "./test_path"
        TEST_ARGS = "testapikey {test_path}".format(test_path=TEST_PATH)
        args = self.run_args(TEST_ARGS)
        self.assertEqual(args.path, [TEST_PATH])

    def test_valid_language(self):
        TEST_LANGUAGE = "en-US"
        TEST_ARG = "--language {test_language} testapikey .".format(
            test_language=TEST_LANGUAGE
        )
        args = self.run_args(TEST_ARG)
        self.assertEqual(args.language, Languages(TEST_LANGUAGE))

    def test_apikey_undefined(self):
        TEST_ARG = "."
        args = self.run_args(TEST_ARG)
        self.assertFalse(args.apikey)
