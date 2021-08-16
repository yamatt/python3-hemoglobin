from io import StringIO
from tempfile import NamedTemporaryFile
import unittest
from unittest.mock import Mock

from hemoglobin.files import HemoglobinFile


class TestHemoglobinFile(unittest.TestCase):
    def test_text(self):
        test_file_contents = "test file contents"
        with StringIO(test_file_contents) as test_file:
            test_hemoglobinfile = HemoglobinFile(test_file, None)

            self.assertIsNone(test_hemoglobinfile._text)
            test_text_result = test_hemoglobinfile.text
            self.assertEqual(test_hemoglobinfile.text, test_file_contents)
            self.assertEqual(id(test_hemoglobinfile.text), id(test_text_result))
            self.assertEqual(test_hemoglobinfile._text, test_file_contents)

    def test_to_dictionary(self):
        test_file_contents = "test file response"

        class MockHemoglobin:
            class grammarbot:
                class APIResponse:
                    raw_json = {"test": "value"}

                check = Mock(return_value=APIResponse)

        mock_file = Mock(return_value=test_file_contents)

        test_hemoglobinfile = HemoglobinFile(mock_file, MockHemoglobin)

        result = test_hemoglobinfile.to_dict()

        self.assertEqual(MockHemoglobin.grammarbot.APIResponse.raw_json, result)
        MockHemoglobin.grammarbot.check.assert_called()

    def test_from_path_cls(self):
        test_hemoglobin = Mock()
        with NamedTemporaryFile() as temp_file:
            test_hemoglobinfile = HemoglobinFile.from_path(
                temp_file.name, test_hemoglobin
            )
            self.assertIsNotNone(test_hemoglobinfile.f)
            self.assertEqual(test_hemoglobinfile.hemoglobin, test_hemoglobin)
