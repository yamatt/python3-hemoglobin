import unittest
from unittest.mock import Mock

from hemoglobin.grammarbot import (
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

    def test_parse_response_correct_content_type_with_mime_parts(self):
        class MockResponse:
            headers = "application/json; charset=UTF-8"

        class MockApiResponse:
            def __init__(self, json):
                self.json = json

        self.test_hemoglobingrammarbot.API_RESPONSE = MockApiResponse

        result = self.test_hemoglobingrammarbot.parse_response(MockResponse)

        self.assertIsInstance(result, MockApiResponse)

    def test_parse_response_correct_content_type_without_mime_parts(self):
        class MockResponse:
            headers = "application/json"

        class MockApiResponse:
            def __init__(self, json):
                self.json = json

        self.test_hemoglobingrammarbot.API_RESPONSE = MockApiResponse

        result = self.test_hemoglobingrammarbot.parse_response(MockResponse)

        self.assertIsInstance(result, MockApiResponse)
