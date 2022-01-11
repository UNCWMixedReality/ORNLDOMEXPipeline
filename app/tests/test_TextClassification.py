import pytest

from app.TextClassification import TextClassifier


# Noun Extraction
def test_azure_connection_works(new_azure_classifier, gatsby_text):
    classifier = new_azure_classifier

    output = classifier.classify_single_text_element(gatsby_text)

    assert output is not None


def test_analysis_on_gatsby_returns_gatsby_as_noun_with_high_confidence(
    new_azure_classifier, gatsby_text
):
    classifier = new_azure_classifier

    output = classifier.classify_single_text_element(gatsby_text)

    results = output.get_all_points_by_category("Person")

    gatsby_hits = [val for val in results if val.noun in ("Gatsby", "gatsby")]

    assert sorted(gatsby_hits, reverse=True)[0].confidence_score > 0.75
