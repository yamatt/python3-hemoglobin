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
    def test_create_params(self):
        test_text = "test text"
        test_apikey = "test api_key"
        test_language = Languages.EN_US

        test_hemoglobingrammarbot = GrammarBotClient(
            api_key=test_apikey, language=test_language
        )

        result = test_hemoglobingrammarbot._create_params(test_text)

        self.assertEqual(
            {
                "language": test_language.value,
                "text": test_text,
                "api_key": test_apikey,
            },
            result,
        )
