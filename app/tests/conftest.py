import pytest
from app.TextExtraction import TextExtractor
import os


@pytest.fixture(scope="function")
def expected_output():
    output = "Once upon a time there were three bears, who lived together in a house of their own in a wood. One of them was a little, small wee bear; one was a middle-sized bear, and the other was a great, huge bear.One day, after they had made porridge for their breakfast, they walked out into the wood while the porridge was cooling. And while they were walking, a little girl came into the house. This little girl had golden curls that tumbled down her back to her waist, and everyone called her by Goldilocks.Goldilocks went inside. First she tasted the porridge of the great, huge bear, and that was far too hot for her. And then she tasted the porridge of the middle bear, and that was too cold for her. And then she went to the porridge of the little, small wee bear, and tasted that. And that was neither too hot nor too cold, but just right; and she liked it so well, that she ate it all up.Then Goldilocks went upstairs into the bed chamber and first she lay down upon the bed of the great, huge bear, and then she lay down upon the bed of the middle bear and finally she lay down upon the bed of the little, small wee bear, and that was just right. So she covered herself up comfortably, and lay there until she fell fast asleep.By this time, the three bears thought their porridge would be cool enough, so they came home to breakfast.“SOMEBODY HAS BEEN AT MY PORRIDGE!” said the great huge bear, in his great huge voice.“Somebody has been at my porridge!” said the middle bear, in his middle voice.Then the little, small wee bear looked at his, and there was the spoon in the porridge pot, but the porridge was all gone“Somebody has been at my porridge, and has eaten it all up!” said the little, small wee bear, in his little, small wee voiceThen the three bears went upstairs into their bedroom.“SOMEBODY HAS BEEN LYING IN MY BED!” said the great, huge bear, in his great, rough, gruff voice.“Somebody has been lying in my bed!” said the middle bear, in his middle voice.And when the little, small, wee bear came to look at his bed, upon the pillow there was a pool of golden curls, and the angelic face of a little girl snoring away, fast asleep.“Somebody has been lying in my bed, and here she is!” Said the little, small wee bear, in his little, small wee voice.Goldilocks jumped off the bed and ran downstairs, out of the door and down the garden path. She ran and she ran until she reached the house of her grandmama. When she told her grandmama about the house of the three bears who lived in the wood, her granny said: “My my, what a wild imagination you have, child!”"  # noqa: E501

    return output


@pytest.fixture(scope="function")
def new_text_extractor():
    return TextExtractor()


@pytest.fixture()
def app_directory():
    current_dir = os.getcwd()

    if current_dir.split("/")[-1] == ("DOMEXPipeline" or "ORNLDOMEXPipeline"):
        return current_dir + "/app"
    else:
        return os.getcwd()
