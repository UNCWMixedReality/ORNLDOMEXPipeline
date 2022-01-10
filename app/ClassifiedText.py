from typing import Optional
from dataclasses import dataclass


@dataclass
class DataPoint:
    """Class for tracking an identified noun and confidence interval among other attributes"""

    noun: str
    category: str
    subcategory: Optional[str]
    confidence_score: float
    length: int
    offset: int


class ClassifiedText(object):
    """A container for Datapoint values which holds the results of our noun extraction requests to various cloud based providers (Azure, AWS)"""

    def __init__(self):
        self.points = []
        self.categories = []

    def add_point(self, point: DataPoint):
        if point.category not in self.categories:
            self.categories.append(point.category)

        self.points.append(point)

    def grab_all_points_by_category(
        self, category: str, subcategory: Optional[str] = None
    ):
        valid_points = [point for point in self.points if point.category == category]

        if subcategory is not None:
            valid_points = [
                point for point in valid_points if point.subcategory == subcategory
            ]

        return valid_points
