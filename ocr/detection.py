from __future__ import annotations
from ocr.character import Character


class Detection:
    """
    Represents a single detection of a character in an image.
    Contains the position and a match certainty.
    """

    def __init__(
        self, character: Character, position: tuple[int, int], match: float
    ) -> None:
        self.character = character
        self.position = position
        self.match = match

    @staticmethod
    def compare_position(det1: Detection, det2: Detection) -> int:
        """
        Compare function for sorting detections by their position. The order is
        from top to bottom and from left to right (like reading).
        """

        if abs(det1.position[0] - det2.position[0]) > max(
            det1.character.size[1], det2.character.size[1]
        ):
            return det1.position[0] - det2.position[0]
        return det1.position[1] - det2.position[1]

    def is_overlapping(self, other: Detection) -> bool:
        """
        Returns True if the detection is overlapping with the other detection.
        """

        y1, x1 = self.position
        y2, x2 = other.position
        w1, h1 = self.character.size
        w2, h2 = other.character.size

        # Coordinates of the intersecting rectangle
        left = max(x1, x2)
        top = max(y1, y2)
        right = min(x1 + w1, x2 + w2)
        bottom = min(y1 + h1, y2 + h2)

        intersection_area = max(0, right - left) * max(0, bottom - top)

        return intersection_area > 0

    def __repr__(self):
        return f"{self.character.char}: ({self.position[0]}, {self.position[1]}) {self.match: .3f}"

    def __str__(self):
        return f"{self.character.char}: ({self.position[0]}, {self.position[1]}) {self.match: .3f}"
