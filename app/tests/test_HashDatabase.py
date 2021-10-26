import pytest


def test_databse_table_creation(test_database):
    db = test_database

    cursor = db._return_new_cursor()

    query = "SELECT count(*) FROM sqlite_master WHERE type='table' AND name='cache_db';"
    cursor.execute(query)

    result = cursor.fetchone()
    print(result)

    assert result[0] == 1


def test_populated_db(test_populated_database):
    db = test_populated_database

    cursor = db._return_new_cursor()

    query = "SELECT count(hash) FROM cache_db;"
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

    assert not db.check_for_existing_hash(hash_0)
    assert not db.check_for_existing_hash(hash_1)


def test_search_database_for_hash_that_does_exist(
    test_populated_database, sample_data, create_hash
):
    db = test_populated_database
    hash_0 = create_hash(sample_data[0][0])
    hash_1 = create_hash(sample_data[1][0])

    assert db.check_for_existing_hash(hash_0)
    assert db.check_for_existing_hash(hash_1)


def test_get_data_that_exists_by_hash(
    test_populated_database, sample_data, create_hash
):
    db = test_populated_database
    hash_0 = create_hash(sample_data[0][0])
    hash_1 = create_hash(sample_data[1][0])

    assert db.get_nouns_from_hash(hash_0) == sample_data[0][1]
    assert db.get_nouns_from_hash(hash_1) == sample_data[1][1]


def test_insert_data(test_db, sample_data, create_hash, retrieve_nouns):
    db = test_db

    hash_0 = create_hash(sample_data[0][0])
    hash_1 = create_hash(sample_data[1][0])

    db.add_new_results_to_hash(hash_0, sample_data[0][1])
    db.add_new_results_to_hash(hash_1, sample_data[1][1])

    assert retrieve_nouns(db, hash_0) == sample_data[0][1]
    assert retrieve_nouns(db, hash_1) == sample_data[1][1]
