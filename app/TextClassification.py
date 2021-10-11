# NOTE: Ensure you're using logging where it would be useful. The Log level is
# declared in __main__, but stick to [info] for high level things "Extracted x amount of files"
# and [debug] for things that will be helpful when stuff breaks, like all FileNotFound errors
from ClassifiedText import ClassifiedText


class TextClassifier(object):
    def __init__(self):
        pass

    # Public methods
    def classify_text(self, text: str) -> ClassifiedText:
        """
        Given: A string of text
        Return: A completed ClassifiedText object
        """
        return None

    # Private methods
    def _classify_with_azure(self, text: str) -> ClassifiedText:
        return None

    def _classify_with_aws(self, text: str) -> ClassifiedText:
        return None
