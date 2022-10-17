from expertai.nlapi.cloud.client import ExpertAiClient
import os
from dotenv import load_dotenv

load_dotenv()

username = os.getenv("EAI_USERNAME")
password = os.getenv("EAI_PASSWORD")


class Model:
    def __init__(self) -> None:
        self.client = ExpertAiClient()

    def hate_speech(self, text) -> dict:
        """Classify input text as hate if detected.

        Args:
            text (string): input text or string.

        Returns:
            dict: {string: string}
        """
        detector = "hate-speech"
        language = "en"

        output = self.client.detection(
            body={"document": {"text": text}},
            params={"detector": detector, "language": language},
        )

        speech = {}

        for category in output.categories:
            speech_type = category.hierarchy
            speech["speech_type"] = speech_type[0]
            speech["category_id"] = category.id_
            speech["category_hierarchy"] = category.hierarchy

        i = 1
        for extraction in output.extractions:
            for field in extraction.fields:
                speech[field.name] = field.value
            i = i + 1

        return speech

    def sentiment_analysis(self, text):
        """Classify input text's sentiments.

        Args:
            text (string): input text or string.

        Returns:
            dict: {string : string}
        """
        language = "en"

        sentiment = {}

        output = self.client.specific_resource_analysis(
            body={"document": {"text": text}},
            params={"language": language, "resource": "sentiment"},
        )

        # Output overall sentiment
        sentiment["score"] = output.sentiment.overall

        return sentiment
