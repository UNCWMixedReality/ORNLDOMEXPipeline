import os

import nltk
from textblob import TextBlob

from DocumentIngestion import extract_all_data_from_a_directory

# nltk.download('brown')
# nltk.download('punkt')


def generate_nouns_from_a_collection_of_data(directory: str, depth: int):
    data = extract_all_data_from_a_directory(directory, depth)

    for each_document in data.keys():
        new_blob = TextBlob(data[each_document]["text"])
        data[each_document]["nouns"] = new_blob.noun_phrases

    return data


results = generate_nouns_from_a_collection_of_data(os.getcwd() + "/speeches/", 1)

for i in results:
    print(i)
    print(
        f'First 10 noun phrases extracted from {i}.txt: {", ".join(results[i]["nouns"][:10])}'
    )
