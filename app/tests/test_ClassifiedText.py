import pytest


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
