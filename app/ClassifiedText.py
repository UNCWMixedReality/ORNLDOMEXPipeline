import json
from copy import deepcopy
from dataclasses import dataclass
from typing import Optional


@dataclass
class DataPoint:
    """Class for tracking an identified noun and confidence interval among other attributes"""

    noun: str
    category: str
    subcategory: Optional[str]
    confidence_score: float
    length: int
    offset: int

    # Sort numerically by confidence score
    #   Use Case: Get a sorted list of most confident to least confident results
    def __eq__(self, other):
        if self.confidence_score is None:
            return False
        elif other.confidence_score is None:
            return False
        else:
            return self.confidence_score == other.confidence_score

    def __gt__(self, other):
        if self.confidence_score is None:
            return False
        elif other.confidence_score is None:
            return False
        else:
            return self.confidence_score > other.confidence_score


class ClassifiedText(object):
    """A container for Datapoint values which holds the results of our noun extraction requests to various cloud based providers (Azure, AWS)"""

    def __init__(self, parent_hash=None, json_str=None):
        self.parent_hash = parent_hash
        self.points = []
        self.categories = []

        if json_str is not None:
            if parent_hash is None:
                self._instantiate_from_json(json_str, full=True)
            else:
                self._instantiate_from_json(json_str, full=False)

    def __add__(self, other):
        if not isinstance(other, ClassifiedText):
            raise RuntimeError("ClassifiedText objects can only be added to each other")
        else:

            tmp_classified_text = ClassifiedText(parent_hash=self.parent_hash)
            all_points = deepcopy(self.points)
            all_points.extend(deepcopy(other.points))

            for point in all_points:
                tmp_classified_text.add_point(point)

            return tmp_classified_text

    def add_point(self, point: DataPoint):
        if point.category not in self.categories:
            self.categories.append(point.category)

        self.points.append(point)

    def get_all_points_by_category(
        self, category: str, subcategory: Optional[str] = None
    ):
        valid_points = [point for point in self.points if point.category == category]

        if subcategory is not None:
            valid_points = [
                point for point in valid_points if point.subcategory == subcategory
            ]

        return valid_points

    def _instantiate_from_json(self, json_str: str, full: bool = False):

        if full:
            self.parent_hash = json_str["parent_hash"]

        for point in json_str["points"]:
            tmp_point = DataPoint(
                noun=point["noun"],
                category=point["category"],
                subcategory=point["subcategory"],
                confidence_score=point["confidence_score"],
                length=point["length"],
                offset=point["offset"],
            )

            self.add_point(tmp_point)


class ClassifiedTextEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__
