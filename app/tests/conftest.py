import hashlib
import json
import os

import pytest

from app.ClassifiedText import ClassifiedText, DataPoint
from app.HashDatabase import HashDatabase
from app.TextClassification import TextClassifier
from app.TextExtraction import TextExtractor


@pytest.fixture(scope="function")
def expected_output():
    output = "Once upon a time there were three bears, who lived together in a house of their own in a wood. One of them was a little, small wee bear; one was a middle-sized bear, and the other was a great, huge bear.One day, after they had made porridge for their breakfast, they walked out into the wood while the porridge was cooling. And while they were walking, a little girl came into the house. This little girl had golden curls that tumbled down her back to her waist, and everyone called her by Goldilocks.Goldilocks went inside. First she tasted the porridge of the great, huge bear, and that was far too hot for her. And then she tasted the porridge of the middle bear, and that was too cold for her. And then she went to the porridge of the little, small wee bear, and tasted that. And that was neither too hot nor too cold, but just right; and she liked it so well, that she ate it all up.Then Goldilocks went upstairs into the bed chamber and first she lay down upon the bed of the great, huge bear, and then she lay down upon the bed of the middle bear and finally she lay down upon the bed of the little, small wee bear, and that was just right. So she covered herself up comfortably, and lay there until she fell fast asleep.By this time, the three bears thought their porridge would be cool enough, so they came home to breakfast.“SOMEBODY HAS BEEN AT MY PORRIDGE!” said the great huge bear, in his great huge voice.“Somebody has been at my porridge!” said the middle bear, in his middle voice.Then the little, small wee bear looked at his, and there was the spoon in the porridge pot, but the porridge was all gone.“Somebody has been at my porridge, and has eaten it all up!” said the little, small wee bear, in his little, small wee voice.Then the three bears went upstairs into their bedroom.“SOMEBODY HAS BEEN LYING IN MY BED!” said the great, huge bear, in his great, rough, gruff voice.“Somebody has been lying in my bed!” said the middle bear, in his middle voice.And when the little, small, wee bear came to look at his bed, upon the pillow there was a pool of golden curls, and the angelic face of a little girl snoring away, fast asleep.“Somebody has been lying in my bed, and here she is!” Said the little, small wee bear, in his little, small wee voice.Goldilocks jumped off the bed and ran downstairs, out of the door and down the garden path. She ran and she ran until she reached the house of her grandmama. When she told her grandmama about the house of the three bears who lived in the wood, her granny said: “My my, what a wild imagination you have, child!”"  # noqa: E501

    return output


@pytest.fixture(scope="function")
def new_text_extractor():
    return TextExtractor()


@pytest.fixture()
def app_directory():
    current_dir = os.getcwd()

    if current_dir.split("/")[2] == "runner":
        return os.environ.get("APP_DIR")
    elif current_dir.split("/")[-1] == ("DOMEXPipeline" or "ORNLDOMEXPipeline"):
        return current_dir + "/app"
    else:
        return os.getcwd()


@pytest.fixture()
def create_hash():
    def _create_hash(output_text):
        return hashlib.sha256(output_text.encode()).digest().hex()

    return _create_hash


@pytest.fixture(scope="function")
def test_database():
    new_db = HashDatabase(postgres=False, db_path=":memory:")
    yield new_db
    cursor = new_db._return_new_cursor()
    cursor.execute("drop table text_classification_results")
    cursor.close()


@pytest.fixture(scope="function")
def test_populated_database():
    data = [
        (
            "S. Truett Cathy Invented Chicken",
            '{"parent_hash": null, "points": [{"noun": "Cathy", "category": "Person", "subcategory": null, "confidence_score": 0.5, "length": 20, "offset": 45}], "categories": ["Person"]}',
        ),  # noqa: E501
        (
            "Thomas Edison Copied Electricity",
            '{"parent_hash": null, "points": [{"noun": "Thomas", "category": "Person", "subcategory": null, "confidence_score": 0.45, "length": 20, "offset": 45}], "categories": ["Person"]}',
        ),  # noqa: E501
    ]
    new_db = HashDatabase(postgres=False, db_path=":memory:")
    cursor = new_db._return_new_cursor()
    for data_point in data:
        tmp_hash = hashlib.sha256(data_point[0].encode()).digest().hex()
        cursor.execute(
            "INSERT INTO text_classification_results VALUES (?,?);",
            (
                tmp_hash,
                data_point[1],
            ),
        )
    cursor.close()
    yield new_db
    cursor = new_db._return_new_cursor()
    cursor.execute("drop table text_classification_results")
    cursor.close()


@pytest.fixture(scope="function")
def sample_data():
    data = [
        (
            "S. Truett Cathy Invented Chicken",
            '{"parent_hash": null, "points": [{"noun": "Cathy", "category": "Person", "subcategory": null, "confidence_score": 0.5, "length": 20, "offset": 45}], "categories": ["Person"]}',
        ),  # noqa: E501
        (
            "Thomas Edison Copied Electricity",
            '{"parent_hash": null, "points": [{"noun": "Thomas", "category": "Person", "subcategory": null, "confidence_score": 0.45, "length": 20, "offset": 45}], "categories": ["Person"]}',
        ),  # noqa: E501
    ]

    return data


@pytest.fixture(scope="function")
def retrieve_classified_text():
    def _retrieve_classified_text(database, hash):
        db_cursor = database._return_new_cursor()
        db_cursor.execute(
            "SELECT classified_text FROM text_classification_results WHERE hash = ?",
            (hash,),
        )
        result = db_cursor.fetchone()[0]
        print(f"{result = }")
        return ClassifiedText(parent_hash=hash, json_str=json.loads(result))

    return _retrieve_classified_text


@pytest.fixture(scope="function")
def create_datapoint():
    def _create_datapoint(
        text, category, subcategory=None, confidence_score=0.00, length=0, offset=0
    ):
        return DataPoint(text, category, subcategory, confidence_score, length, offset)

    return _create_datapoint


@pytest.fixture(scope="function")
def new_classified_text():
    return ClassifiedText()


@pytest.fixture(scope="function")
def create_classified_text():
    def _create_classified_text(hash, json_str):
        return ClassifiedText(parent_hash=hash, json_str=json_str)

    return _create_classified_text


@pytest.fixture(scope="function")
def new_azure_classifier():
    return TextClassifier(azure=True)


@pytest.fixture()
def gatsby_text():
    text = "In my younger and more vulnerable years my father gave me some advicethat I’ve been turning over in my mind ever since.“Whenever you feel like criticizing anyone,” he told me, “justremember that all the people in this world haven’t had the advantagesthat you’ve had.”He didn’t say any more, but we’ve always been unusually communicativein a reserved way, and I understood that he meant a great deal morethan that. In consequence, I’m inclined to reserve all judgements, ahabit that has opened up many curious natures to me and also made methe victim of not a few veteran bores. The abnormal mind is quick todetect and attach itself to this quality when it appears in a normalperson, and so it came about that in college I was unjustly accused ofbeing a politician, because I was privy to the secret griefs of wild,unknown men. Most of the confidences were unsought—frequently I havefeigned sleep, preoccupation, or a hostile levity when I realized bysome unmistakable sign that an intimate revelation was quivering onthe horizon; for the intimate revelations of young men, or at leastthe terms in which they express them, are usually plagiaristic andmarred by obvious suppressions. Reserving judgements is a matter ofinfinite hope. I am still a little afraid of missing something if Iforget that, as my father snobbishly suggested, and I snobbishlyrepeat, a sense of the fundamental decencies is parcelled outunequally at birth.And, after boasting this way of my tolerance, I come to the admissionthat it has a limit. Conduct may be founded on the hard rock or thewet marshes, but after a certain point I don’t care what it’s foundedon. When I came back from the East last autumn I felt that I wantedthe world to be in uniform and at a sort of moral attention forever; Iwanted no more riotous excursions with privileged glimpses into thehuman heart. Only Gatsby, the man who gives his name to this book, wasexempt from my reaction—Gatsby, who represented everything for which Ihave an unaffected scorn. If personality is an unbroken series ofsuccessful gestures, then there was something gorgeous about him, someheightened sensitivity to the promises of life, as if he were relatedto one of those intricate machines that register earthquakes tenthousand miles away. This responsiveness had nothing to do with thatflabby impressionability which is dignified under the name of the“creative temperament”—it was an extraordinary gift for hope, aromantic readiness such as I have never found in any other person andwhich it is not likely I shall ever find again. No—Gatsby turned outall right at the end; it is what preyed on Gatsby, what foul dustfloated in the wake of his dreams that temporarily closed out myinterest in the abortive sorrows and short-winded elations of men."  # noqa: E501

    return text
