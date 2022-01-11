import json

import pytest

from app.ClassifiedText import ClassifiedText, ClassifiedTextEncoder


# Data Point Tests
def test_data_point_equality_on_datapoint_with_no_confidence_score(create_datapoint):
    tomato = create_datapoint("Tomato", "Vegetable", confidence_score=None)
    spinach = create_datapoint("Spinach", "Vegetable")

    assert tomato != spinach


def test_data_point_equality_on_datapoint_with_valid_confidence_scores(
    create_datapoint,
):
    tomato = create_datapoint("Tomato", "Vegetable", confidence_score=0.5)
    spinach = create_datapoint("Spinach", "Vegetable", confidence_score=0.5)

    assert tomato == spinach


def test_data_point_sorting_potential(create_datapoint):
    tomato = create_datapoint("Tomato", "Vegetable", confidence_score=0.75)
    spinach = create_datapoint("Spinach", "Vegetable", confidence_score=0.5)
    squash = create_datapoint("Squash", "Vegetable", confidence_score=0.25)

    garden = [spinach, squash, tomato]

    assert sorted(garden, reverse=True)[0] == tomato
    assert sorted(garden, reverse=True)[2] == squash


def test_addition_of_a_new_point(new_classified_text, create_datapoint):
    results = new_classified_text
    assert len(results.points) == 0

    tmp_datapoint = create_datapoint("Tomato", "Vegetable", "Indeterminate")

    results.add_point(tmp_datapoint)

    assert len(results.points) == 1
    assert tmp_datapoint in results.points


def test_category_update_after_points_addition(new_classified_text, create_datapoint):
    results = new_classified_text
    assert len(results.categories) == 0

    tmp_datapoint = create_datapoint("Tomato", "Vegetable", "Indeterminate")

    results.add_point(tmp_datapoint)

    assert len(results.categories) == 1
    assert tmp_datapoint.category in results.categories


def test_retrieval_of_datapoints_by_existing_categories(
    new_classified_text, create_datapoint
):
    results = new_classified_text
    assert len(results.categories) == 0
    assert len(results.points) == 0

    tomato = create_datapoint("Tomato", "Vegetable", "Indeterminate")
    cucumber = create_datapoint("Cucumber", "Vegetable", "Indeterminate")
    basil = create_datapoint("Basil", "Herb", "Italian")

    results.add_point(tomato)
    results.add_point(cucumber)
    results.add_point(basil)

    assert len(results.categories) == 2
    assert len(results.points) == 3
    assert len(results.get_all_points_by_category("Vegetable")) == 2


def test_retrieval_of_datapoints_by_nonexistent_categories(
    new_classified_text, create_datapoint
):
    results = new_classified_text
    assert len(results.categories) == 0

    tomato = create_datapoint("Tomato", "Vegetable", "Indeterminate")
    cucumber = create_datapoint("Cucumber", "Vegetable", "Indeterminate")
    basil = create_datapoint("Basil", "Herb", "Italian")

    results.add_point(tomato)
    results.add_point(cucumber)
    results.add_point(basil)

    assert len(results.categories) == 2
    assert len(results.get_all_points_by_category("Fruit")) == 0


def test_retrieval_of_datapoints_by_existing_subcategories(
    new_classified_text, create_datapoint
):
    results = new_classified_text
    assert len(results.categories) == 0

    tomato = create_datapoint("Tomato", "Vegetable", "Indeterminate")
    cucumber = create_datapoint("Cucumber", "Vegetable", "Indeterminate")
    cherry_tomato = create_datapoint("Cherry Tomatoes", "Vegetable", "Determinate")
    basil = create_datapoint("Basil", "Herb", "Italian")

    results.add_point(tomato)
    results.add_point(cucumber)
    results.add_point(cherry_tomato)
    results.add_point(basil)

    assert len(results.categories) == 2
    assert len(results.get_all_points_by_category("Vegetable")) == 3
    assert len(results.get_all_points_by_category("Vegetable", "Determinate")) == 1


def test_retrieval_of_datapoints_by_nonexistent_subcategories(
    new_classified_text, create_datapoint
):
    results = new_classified_text
    assert len(results.categories) == 0

    tomato = create_datapoint("Tomato", "Vegetable", "Indeterminate")
    cucumber = create_datapoint("Cucumber", "Vegetable", "Indeterminate")
    cherry_tomato = create_datapoint("Cherry Tomatoes", "Vegetable", "Determinate")
    basil = create_datapoint("Basil", "Herb", "Italian")

    results.add_point(tomato)
    results.add_point(cucumber)
    results.add_point(cherry_tomato)
    results.add_point(basil)

    assert len(results.categories) == 2
    assert len(results.get_all_points_by_category("Vegetable")) == 3
    assert len(results.get_all_points_by_category("Fruit")) == 0
    assert len(results.get_all_points_by_category("Vegetable", "Determinate")) == 1
    assert len(results.get_all_points_by_category("Vegetable", "Hydra")) == 0


# Test ClassifiedText __add__
def test_invalid_instance_of_classified_text_addition(new_classified_text):
    results = new_classified_text

    with pytest.raises(RuntimeError):
        results + 1


def test_valid_instance_of_classified_text_addition(create_datapoint):
    tomato = create_datapoint("Tomato", "Vegetable", "Indeterminate")
    cucumber = create_datapoint("Cucumber", "Vegetable", "Indeterminate")
    cherry_tomato = create_datapoint("Cherry Tomatoes", "Vegetable", "Determinate")
    basil = create_datapoint("Basil", "Herb", "Italian")

    t_hash = f'{"1"*64}'
    nt_hash = f'{"2"*64}'

    ct_1 = ClassifiedText(parent_hash=t_hash)
    ct_2 = ClassifiedText(parent_hash=nt_hash)

    ct_1.add_point(tomato)
    ct_2.add_point(cucumber)
    ct_1.add_point(cherry_tomato)
    ct_2.add_point(basil)

    assert len(ct_1.points) == 2
    assert len(ct_2.points) == 2

    combined_ct = ct_1 + ct_2

    assert combined_ct.parent_hash == t_hash
    assert len(combined_ct.points) == 4
    assert len(combined_ct.categories) == len(ct_1.categories) + len(ct_2.categories)


# Test JSON
def test_that_object_remains_the_same_through_json_serialization(create_datapoint):
    tomato = create_datapoint("Tomato", "Vegetable", "Indeterminate")
    cucumber = create_datapoint("Cucumber", "Vegetable", "Indeterminate")
    cherry_tomato = create_datapoint("Cherry Tomatoes", "Vegetable", "Determinate")
    basil = create_datapoint("Basil", "Herb", "Italian")

    t_hash = f'{"1"*64}'

    ct_1 = ClassifiedText(parent_hash=t_hash)

    ct_1.add_point(tomato)
    ct_1.add_point(cucumber)
    ct_1.add_point(cherry_tomato)
    ct_1.add_point(basil)

    assert len(ct_1.points) == 4
    assert len(ct_1.categories) == 2

    temp_json = json.dumps(ct_1, cls=ClassifiedTextEncoder)
    rebuilt_ct = ClassifiedText(json_str=temp_json)

    assert isinstance(rebuilt_ct, ClassifiedText)
    assert len(rebuilt_ct.points) == 4
    assert len(rebuilt_ct.categories) == 2
    assert rebuilt_ct.parent_hash == ct_1.parent_hash
    assert rebuilt_ct.points[0].noun == ct_1.points[0].noun
