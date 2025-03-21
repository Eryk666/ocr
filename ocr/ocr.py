from functools import cmp_to_key

import numpy as np
from numpy.fft import fft2, ifft2

from PIL.Image import Image

from ocr.detection import Detection
from ocr.font import Font
from ocr.character import Character
from ocr.preprocess import correct_rotation


class OCR:
    """
    Optical Character Recognition class. It reads text from an image using a given font.
    """

    def __init__(self, font: Font, match_threshold: float = 0.9) -> None:
        self.font = font
        self.threshold = match_threshold

    def read(self, text_image: Image) -> str:
        """
        Returns the text read from the image.
        """

        text_image = correct_rotation(text_image)

        detections = self.__detect_all_characters(text_image)
        detections = self.__filter_overlapping_detections(detections)

        return self.__reconstruct_text(detections)

    def __detect_all_characters(self, text_image: Image) -> list[Detection]:
        detections = []

        for character in self.font.characters:
            detections.extend(self.__detect_character(text_image, character))

        return detections

    def __detect_character(
        self, text_image: Image, character: Character
    ) -> list[Detection]:
        text_array = np.array(text_image.convert("L"))
        char_array = np.array(character.image.convert("L"))

        # Use the character correlation with itself to normalize the correlation
        correlation_norm = np.max(
            np.real(ifft2(fft2(char_array) * fft2(np.rot90(char_array, 2))))
        )

        # Pad the character array with zeros to match the text array size
        char_array = np.pad(
            char_array,
            (
                (0, text_array.shape[0] - char_array.shape[0]),
                (0, text_array.shape[1] - char_array.shape[1]),
            ),
        )

        # Calculate the correlation of the text with the character, normalize it
        # and remove matches below the threshold
        correlation = np.real(ifft2(fft2(text_array) * fft2(np.rot90(char_array, 2))))
        correlation /= correlation_norm
        correlation[correlation <= self.threshold * np.max(correlation)] = 0

        positions = np.nonzero(correlation)

        return [
            Detection(character, (x, y), correlation[x, y] * character.match_weight)
            for x, y in zip(positions[0], positions[1])
        ]

    def __filter_overlapping_detections(
        self, detections: list[Detection]
    ) -> list[Detection]:
        detections.sort(key=lambda d: d.match, reverse=False)

        filtered_detections = []

        while detections:
            best_detection = detections.pop()
            filtered_detections.append(best_detection)

            # Filter out all overlapping detections
            detections = [
                detection
                for detection in detections
                if not best_detection.is_overlapping(detection)
            ]

        return filtered_detections

    def __reconstruct_text(self, detections: list[Detection]) -> str:
        if len(detections) < 1:
            return ""

        if len(detections) == 1:
            return str(detections[0].character)

        text = ""

        detections.sort(key=cmp_to_key(Detection.compare_position))

        for i in range(len(detections) - 1):
            curr_detection = detections[i]
            next_detection = detections[i + 1]

            text += str(curr_detection.character)

            if (
                next_detection.position[0] - curr_detection.position[0]
                > self.font.line_height
            ):
                text += "\n"
            elif (
                next_detection.position[1] - curr_detection.position[1]
                > curr_detection.character.size[0] + self.font.space_width
            ):
                text += " "

        return text
