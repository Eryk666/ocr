# OCR

An Optical Character Recognition (OCR) tool that utilizes Discrete Fourier Transform (DFT) to extract text from images. Made for the Computational Methods in Science and Technology course at AGH UST.

## Installation

You'll need Python 3.10 or higher and Poetry to manage dependencies. Then simply install the required packages:

```bash
poetry install
```

## Usage

Run the script to extract text from an image:

```bash
python main.py <image-path> [-i | --invert]
```

- Replace `<image-path>` with the path to the image you want to process.
- The `-i` or `--invert` flag should be used if your image has black text on a white background.

To try it with the sample image, use:

```bash
python main.py examples/lorem_ipsum_arial.png -i
```

## Customization

You can add new fonts by placing them in the fonts directory. Each font should include character images and a corresponding JSON metadata file. The JSON file must follow this structure:

```json
{
    "font_name": "arial",
    "line_height": 48,
    "space_width": 10,
    "characters": [
        {
            "char": "a",
            "image": "a.png",
            "match_weight": 1
        },
        ...
    ]
}
```

- `font_name`: The name of the font.
- `line_height`: The height of a text line in pixels.
- `space_width`: The width of a space character.
- `characters`: A list of character definitions, where each entry includes:
  - `char`: The character itself.
  - `image`: The filename of the corresponding character image.
  - `match_weight`: A weight value used for matching accuracy. A lower value decreases the likelihood of detecting the character. This can help prevent misinterpretations, such as an "r" being mistakenly recognized within an "n" or "m".
