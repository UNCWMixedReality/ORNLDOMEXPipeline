# NOTE: Ensure you're using logging where it would be useful. The Log level is
# declared in __main__, but stick to [info] for high level things "Extracted x amount of files"
# and [debug] for things that will be helpful when stuff breaks, like all FileNotFound errors
import os
import sqlite3

from azure.ai.textanalytics import DocumentError, TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

from app.ClassifiedText import ClassifiedText, DataPoint


class TextClassifier(object):
    def __init__(self, db_path: str = "internal_db.db", azure=False):
        self.azure_channel = None
        self.aws_channel = None
        self.con = sqlite3.connect(db_path)
        self.cache_table_name = "record_db"

        if azure:
            self._instantiate_azure_connection()

    # Public methods
    def classify_single_text_element(
        self, text: str, service: str = "azure"
    ) -> ClassifiedText:
        """
        Given: A string of text
        Return: A completed ClassifiedText object
        """

        working_classified_text = ClassifiedText()

        try:
            document = [text]
            result = self.azure_channel.recognize_entities(documents=document)[0]

            for entity in result.entities:
                new_datapoint = DataPoint(
                    noun=entity.text,
                    category=entity.category,
                    subcategory=entity.subcategory,
                    confidence_score=entity.confidence_score,
                    length=entity.length,
                    offset=entity.offset,
                )

            working_classified_text.add_point(new_datapoint)

        except Exception as err:
            print(
                f"Encountered exception while classifying the document beginning in {text[:100]}.\
                The error is as follows: {err}"
            )
            return None

        return working_classified_text

    # Top level private methods
    def _classify_with_azure(self, text: str) -> ClassifiedText:
        self._instantiate_azure_connection()
        return None

    def _classify_with_aws(self, text: str) -> ClassifiedText:
        return None

    # Utility private methods

    def _record_number_of_text_records(self, text: str):
        if type(text) != str:
            raise ValueError("Input must be a string")

        current_length = len(text)
        return current_length

    def _add_new_responses_to_classified_text(
        self, current_text: ClassifiedText, new_nouns: dict
    ):
        return None

    def _instantiate_azure_connection(self):
        key = os.environ.get("AZURE_KEY")
        endpoint = os.environ.get("AZURE_ENDPOINT")

        # Authenticate the client using your key and endpoint
        ta_credential = AzureKeyCredential(key)
        self.azure_channel = TextAnalyticsClient(
            endpoint=endpoint, credential=ta_credential
        )


if __name__ == "__main__":
    test = TextClassifier(azure=True)
    test.classify_single_text_element(
        "My name is Seth. I really like Apple. I'd like to work for them one day."
    )
