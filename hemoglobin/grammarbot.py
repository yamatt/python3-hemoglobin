from enum import Enum
from typing import List

import mimeparse
import requests

from grammarbot import GrammarBotClient, GrammarBotApiResponse, GrammarBotMatch


class Language(Enum):
    EN_US = "en-US"
    EN_GB = "en-GB"


class GrammarBotException(Exception):
    pass


class HemoglobinGrammarBotMatch(GrammarBotMatch):
    @property
    def sentence(self) -> str:
        """
        Gives the rule category.
        """
        return self._match_json["sentence"]


class HemoglobinGrammarBotApiResponse(GrammarBotApiResponse):
    MATCH = HemoglobinGrammarBotMatch

    @property
    def matches(self) -> List[GrammarBotMatch]:
        """
        Different matches detected by the GrammarBot API.
        """
        return [self.MATCH(mjson) for mjson in self._json["matches"]]


class HemoglobinGrammarBot(GrammarBotClient):
    API_RESPONSE = HemoglobinGrammarBotApiResponse

    def __init__(
        self,
        base_uri: str = "http://api.grammarbot.io/",
        api_key: str = "python-default",
        language: Language = Language.EN_US,
    ):
        super(HemoglobinGrammarBot, self).__init__(base_uri=base_uri, api_key=api_key)
        self.language = language

    def _create_params(self, text):
        return {"language": self.language.value, "text": text, "api_key": self._api_key}

    def get_response(self, text: str):
        params = self._create_params(text)
        return requests.get(self._endpoint, params=params)

    def parse_response(self, response):
        main_mime_type, sub_mime_type, _ = mimeparse.parse_mime_type(
            response.headers["Content-Type"]
        )
        if main_mime_type == "application" and sub_mime_type == "json":
            json = response.json()
            return self.API_RESPONSE(json)
        raise GrammarBotException(response.text)

    def check(self, text: str):
        """
        Check a given piece of text for grammatical errors.
        :param text:
            Text to be checked using the API.
        """
        return self.parse_response(self.get_response(text))
