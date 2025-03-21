import numpy as np
import numpy.typing as npt
from numpy.fft import fft2, fftshift

from PIL import Image


def correct_rotation(text_image: Image.Image) -> Image.Image:
    """
    Return the image rotated so that the text is straight.
    """

    angle = get_rotation_angle(text_image)
    return text_image.rotate(90 - angle, resample=Image.BICUBIC)


def get_rotation_angle(text_image: Image.Image) -> float:
    """
    Calculate the rotation angle of the text in the image using DFT. The angle
    is measured perpendicular to the text so the straight text will have an
    angle of 90 degrees.

    This function uses the fact that there is a bright line in the magnitude
    spectrum that is perpendicular to the text. It finds a point on this line
    and calculates the angle with basic trigonometry.
    """

    text_array = pad_to_square(np.array(text_image.convert("L")))

    magnitude = fftshift(np.abs(fft2(text_array)))

    rows, cols = magnitude.shape
    mid_row, mid_col = rows // 2, cols // 2

    # Exclude the center
    magnitude[mid_row-5:mid_row+5, mid_col-5:mid_col+5] = 0

    # Find the brightest pixel which should be on the line
    max_row, max_col = np.unravel_index(np.argmax(magnitude), magnitude.shape)

    delta_row = max_row - mid_row
    delta_col = mid_col - max_col

    angle = np.rad2deg(np.arctan2(delta_row, delta_col))

    # The line is symmetrical and we might have picked the wrong side
    if angle < 0:
        angle += 180

    return angle


def pad_to_square(array: npt.NDArray) -> npt.NDArray:
    """
    Pad the array so that it is square and the content is in the center.
    """

    height, width = array.shape[:2]

    new_size = max(height, width)

    pad_height = (new_size - height) // 2
    pad_width = (new_size - width) // 2

    padding = (
        (pad_height, pad_height), 
        (pad_width, pad_width),
    )

    return np.pad(array, padding)