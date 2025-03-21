import os
import argparse
from PIL import Image, ImageOps
from ocr.font import Font
from ocr.ocr import OCR


def main():
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="OCR Application")
    parser.add_argument("image_path", help="Path to the image file", type=str)
    parser.add_argument(
        "-i", "--invert", help="Invert the colors of the image", action="store_true"
    )

    # Parse arguments
    args = parser.parse_args()

    # Load the font and instantiate the OCR
    font = Font(os.path.join("fonts", "arial"))
    ocr = OCR(font)

    # Open the image
    try:
        image = Image.open(args.image_path)
    except FileNotFoundError:
        print(f"Error: The file {args.image_path} was not found.")
        return
    except Exception as e:
        print(f"Error loading image: {e}")
        return

    # Invert the image colors if specified
    if args.invert:
        image = ImageOps.invert(image.convert("RGB"))

    # Process the image with OCR and print the results
    text = ocr.read(image)
    print(text)


if __name__ == "__main__":
    main()
