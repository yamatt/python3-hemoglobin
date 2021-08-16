import unittest
from unittest.mock import Mock

from hemoglobin.grammarbot import (
    GrammarBotException,
    HemoglobinGrammarBot as GrammarBotClient,
    HemoglobinGrammarBotApiResponse as GrammarBotApiResponse,
    HemoglobinGrammarBotMatch as GrammarBotMatch,
    Language as Languages,
)


class TestGrammarBotMatch(unittest.TestCase):
    def test_sentence(self):
        TEST_SENTENCE_VALUE = "test sentence"
        mock_grammarbotmatch = GrammarBotMatch({"sentence": TEST_SENTENCE_VALUE})
        self.assertEqual(mock_grammarbotmatch.sentence, TEST_SENTENCE_VALUE)


class TestGrammarBotApiResponse(unittest.TestCase):
    def test_matches(self):
        mock_match = Mock()

        class OverrideHemoglobinGrammarBotApiResponse(GrammarBotApiResponse):
            MATCH = mock_match

        test_match_response = {"test_response": "test match value"}
        mock_grammarbotapiresponse = OverrideHemoglobinGrammarBotApiResponse(
            {"matches": [test_match_response]}
        )

        mock_grammarbotapiresponse.matches

        mock_match.assert_called()


class TestGrammarBotClient(unittest.TestCase):
    def setUp(self):
        self.test_text = "test text"
        self.test_apikey = "test api_key"
        self.test_language = Languages.EN_US

        self.test_hemoglobingrammarbot = GrammarBotClient(
            api_key=self.test_apikey, language=self.test_language
        )

    def test_create_params(self):

        result = self.test_hemoglobingrammarbot._create_params(self.test_text)

        self.assertEqual(
            {
                "language": self.test_language.value,
                "text": self.test_text,
                "api_key": self.test_apikey,
            },
            result,
        )

    def test_parse_response_correct_content_type_with_encoding_part(self):
        class MockResponse:
            headers = {"Content-Type": "application/json; charset=UTF-8"}

        result = self.test_hemoglobingrammarbot.check_response(MockResponse)

    def test_check_response_correct_content_type_without_encoding_part(self):
        class MockResponse:
            headers = {"Content-Type": "binary/text"}

        with self.assertRaises(GrammarBotException):
            self.test_hemoglobingrammarbot.check_response(MockResponse)

    def test_under_max_chars(self):
        test_short_text = """Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n\nPhasellus augue odio, consectetur ut justo nec, sollicitudin convallis libero."""

        self.test_hemoglobingrammarbot.MAX_CHARS = 200  # line above is 136 chars

        self.test_hemoglobingrammarbot.check_under_max_chars = Mock()
        self.test_hemoglobingrammarbot.check_over_max_chars = Mock()

        self.test_hemoglobingrammarbot.check(test_short_text)

        self.test_hemoglobingrammarbot.check_under_max_chars.assert_called()
        self.test_hemoglobingrammarbot.check_over_max_chars.assert_not_called()

    def test_over_max_chars(self):
        test_short_text = """Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n\nPhasellus augue odio, consectetur ut justo nec, sollicitudin convallis libero."""

        self.test_hemoglobingrammarbot.MAX_CHARS = 100  # line above is 136 chars

        self.test_hemoglobingrammarbot.check_under_max_chars = Mock()
        self.test_hemoglobingrammarbot.check_over_max_chars = Mock()

        self.test_hemoglobingrammarbot.check(test_short_text)

        self.test_hemoglobingrammarbot.check_under_max_chars.assert_not_called()
        self.test_hemoglobingrammarbot.check_over_max_chars.assert_called()

    def test_check_over_max_chars(self):
        test_short_text = """Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n\nPhasellus augue odio, consectetur ut justo nec, sollicitudin convallis libero."""

        self.test_hemoglobingrammarbot.get_response = Mock()
        self.test_hemoglobingrammarbot.check_response = Mock()
