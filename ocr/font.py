import os, json
from PIL import Image, ImageOps
from ocr.character import Character


class Font:
    """
    A class representing a font that contains a set of characters.
    """

    def __init__(self, font_path: str) -> None:
        """
        Font path should point to a directory containing character images and
        .JSON file with font metadata.
        """

        self.font_name = ""
        self.line_height = 0
        self.space_width = 0
        self.characters = set()

        self.__load_font(font_path)

    def __load_font(self, font_path: str) -> None:
        with open(
            os.path.join(font_path, os.path.basename(font_path) + ".json"), "r"
        ) as font_json:
            font_data = json.load(font_json)

            self.font_name = font_data["font_name"]
            self.line_height = font_data["line_height"]
            self.space_width = font_data["space_width"]

            for character in font_data["characters"]:
                char = character["char"]

                image_path = os.path.join(font_path, character["image"])
                image = Image.open(image_path)
                image = ImageOps.invert(image)

                match_weight = float(character["match_weight"])

                self.characters.add(Character(char, image, match_weight))
