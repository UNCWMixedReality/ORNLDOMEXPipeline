from app.TextClassification import TextClassifier
import pytest


# Noun Extraction
def test_azure_connection_works(new_azure_classifier, gatsby_text):
    classifier = new_azure_classifier

    output = classifier.classify_single_text_element(gatsby_text)

    assert output is not None
