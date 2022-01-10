import pytest


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
    assert len(results.grab_all_points_by_category("Vegetable")) == 2


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
    assert len(results.grab_all_points_by_category("Fruit")) == 0


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
    assert len(results.grab_all_points_by_category("Vegetable")) == 3
    assert len(results.grab_all_points_by_category("Vegetable", "Determinate")) == 1


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
    assert len(results.grab_all_points_by_category("Vegetable")) == 3
    assert len(results.grab_all_points_by_category("Fruit")) == 0
    assert len(results.grab_all_points_by_category("Vegetable", "Determinate")) == 1
    assert len(results.grab_all_points_by_category("Vegetable", "Hydra")) == 0
