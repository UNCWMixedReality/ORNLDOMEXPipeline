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

    def __init__(self):
        self.points = []
        self.categories = []

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
