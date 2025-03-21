from PIL.Image import Image


class Character:
    """
    Represents a single character with its image and match weight (between 0 and 1).
    """

    def __init__(self, char: str, image: Image, match_weight: float) -> None:
        self.char = char
        self.image = image
        self.size = self.image.size
        self.match_weight = match_weight

    def __repr__(self):
        return self.char

    def __str__(self):
        return self.char

    def __eq__(self, other):
        if isinstance(other, Character):
            return self.char == other.char
        return False

    def __hash__(self):
        return hash(self.char)
