import json
from copy import deepcopy

import pytest

from app.ClassifiedText import ClassifiedText
from app.HashDatabase import HashDatabase


def test_database_table_creation(test_database):
    db = test_database

    cursor = db._return_new_cursor()

    query = "SELECT count(*) FROM sqlite_master WHERE type='table' AND name='text_classification_results';"
    cursor.execute(query)

    result = cursor.fetchone()
    print(result)

    assert result[0] == 1


def test_populated_db(test_populated_database):
    db = test_populated_database

    cursor = db._return_new_cursor()

    query = "SELECT count(hash) FROM text_classification_results;"
    cursor.execute(query)

    result = cursor.fetchone()

    print(result)
    assert result[0] == 2


def test_search_database_for_int_hash(test_database):
    db = test_database

    with pytest.raises(ValueError):
        db.check_for_existing_hash(12345678)


def test_search_database_for_invalid_hash_length(test_database):
    db = test_database

    with pytest.raises(ValueError):
        db.check_for_existing_hash("thisistooshort")


def test_search_database_for_hash_that_doesnt_exist(
    test_database, sample_data, create_hash
):
    db = test_database
    hash_0 = create_hash(sample_data[0][0])
    hash_1 = create_hash(sample_data[1][0])

    assert db.check_for_existing_hash(hash_0) == False  # noqa: E712
    assert db.check_for_existing_hash(hash_1) == False  # noqa: E712


def test_search_database_for_hash_that_does_exist(
    test_populated_database, sample_data, create_hash
):
    db = test_populated_database
    hash_0 = create_hash(sample_data[0][0])
    hash_1 = create_hash(sample_data[1][0])

    assert db.check_for_existing_hash(hash_0)
    assert db.check_for_existing_hash(hash_1)


def test_get_data_that_exists_by_hash(
    test_populated_database, sample_data, create_hash, create_classified_text
):
    db = test_populated_database
    hash_0 = create_hash(sample_data[0][0])
    hash_1 = create_hash(sample_data[1][0])

    ct_0 = create_classified_text(hash_0, json.loads(sample_data[0][1]))
    ct_1 = create_classified_text(hash_1, json.loads(sample_data[1][1]))

    assert db.get_classified_text_from_hash(hash_0).parent_hash == ct_0.parent_hash
    assert db.get_classified_text_from_hash(hash_1).parent_hash == ct_1.parent_hash
    assert db.get_classified_text_from_hash(hash_0).points == ct_0.points
    assert db.get_classified_text_from_hash(hash_1).points == ct_1.points


def test_insert_data(
    test_database,
    sample_data,
    create_hash,
    retrieve_classified_text,
    create_classified_text,
):
    db = test_database

    hash_0 = create_hash(sample_data[0][0])
    hash_1 = create_hash(sample_data[1][0])

    ct_0 = ClassifiedText(hash_0, json.loads(sample_data[0][1]))
    p_ct_0 = deepcopy(ct_0)
    ct_1 = ClassifiedText(hash_1, json.loads(sample_data[1][1]))
    p_ct_1 = deepcopy(ct_1)

    print(f" Before Storage: {ct_0.parent_hash = }")

    db.add_new_results_to_database(ct_0)
    db.add_new_results_to_database(ct_1)

    print(f" After Storage: {ct_0.parent_hash = }")

    assert retrieve_classified_text(db, hash_0).parent_hash == p_ct_0.parent_hash
    assert retrieve_classified_text(db, hash_1).parent_hash == p_ct_1.parent_hash
    assert retrieve_classified_text(db, hash_0).points == p_ct_0.points
    assert retrieve_classified_text(db, hash_1).points == p_ct_1.points
