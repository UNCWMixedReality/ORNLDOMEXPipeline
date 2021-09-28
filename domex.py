import os
import logging
from operator import itemgetter

import nltk
from textblob import TextBlob

from DocumentIngestion import extract_all_data_from_a_directory

# Import models
nltk.download('brown')
nltk.download('punkt')

# Set logging
logging.basicConfig(filename='domex_pipeline.log', level=logging.INFO, filemode='w', format='%(name)s - %(levelname)s - %(message)s')

def generate_nouns_from_a_collection_of_data(directory: str, depth: int):
    data = extract_all_data_from_a_directory(directory, depth)

    for each_document in data.keys():
        new_blob = TextBlob(data[each_document]["text"])
        data[each_document]["nouns"] = new_blob.noun_phrases

    return data

def frequency_from_list(nouns: list) -> dict:
    freq_dict = {}

    for noun in nouns:
        if noun in freq_dict:
            freq_dict[noun] += 1
        else:
            freq_dict[noun] = 1
    
    return freq_dict

def get_ten_most_frequent_nouns(noun_freq: dict) -> list:
    # Prepare yourself for some truly inefficient code

    def _list_helper(new_item, current_list):
        current_list.append(new_item)
        return sorted(current_list, key=itemgetter(1), reverse=True)[:10]

    most_popular = []
    for i in noun_freq:
        most_popular = _list_helper((i, noun_freq[i]), most_popular)
    
    return most_popular


results = generate_nouns_from_a_collection_of_data(os.getcwd() + "/speeches/", 1)

for i in results:
    logging.info(f'output for {i}')
    logging.info(f'Total number of unique nouns found: {len(set(results[i]["nouns"]))}')
    most_popular_from_i = get_ten_most_frequent_nouns(frequency_from_list(results[i]["nouns"]))
    logging.info(f'Ten most frequently occuring nouns: {most_popular_from_i}')

