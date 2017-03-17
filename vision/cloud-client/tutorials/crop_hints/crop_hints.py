"""
Crop Hints tutorial.
Run this script on an image to output a cropped image or an image highlighting
suggested crop regions on an image:
    python crop_hints.py <path-to-image> <crop | draw>

Examples:
    python crop_hints.py resources/cropme.jpg draw
    python crop_hints.py resources/cropme.jpg crop
"""
# [START full_tutorial]
# [START imports]
import argparse
import io

from google.cloud import vision
from PIL import Image, ImageDraw
# [END imports]


def getCropHint(path):
    # [START get_crop_hint]
    """Detect crop hints on a single image and return the first result."""
    vision_client = vision.Client()
    with io.open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision_client.image(content=content)

    # Return bounds for the first crop hint using an aspect ratio of 1.77.
    return image.detect_crop_hints({1.77})[0].bounds.vertices
    # [END get_crop_hint]


def drawHint(image_file, vects):
    """Draw a border around the image using the hints in the vector list."""
    # [START draw_hint]
    im = Image.open(image_file)
    draw = ImageDraw.Draw(im)

    draw.line([vects[0].x_coordinate, vects[0].y_coordinate,
              vects[1].x_coordinate, vects[1].y_coordinate],
              fill='red', width=3)
    draw.line([vects[1].x_coordinate, vects[1].y_coordinate,
              vects[2].x_coordinate, vects[2].y_coordinate],
              fill='red', width=3)
    draw.line([vects[2].x_coordinate, vects[2].y_coordinate,
              vects[3].x_coordinate, vects[3].y_coordinate],
              fill='red', width=3)
    draw.line([vects[3].x_coordinate, vects[3].y_coordinate,
              vects[0].x_coordinate, vects[0].y_coordinate],
              fill='red', width=3)
    del draw
    im.save('output-hint.jpg', 'JPEG')
    # [END draw_hint]


def cropToHint(image_file, vects):
    """Crop the image using the hints in the vector list."""
    # [START crop_to_hint]
    im = Image.open(image_file)
    im2 = im.crop((vects[0].x_coordinate, vects[0].y_coordinate,
                  vects[2].x_coordinate - 1, vects[2].y_coordinate - 1))
    im2.save('output-crop.jpg', 'JPEG')
    # [END crop_to_hint]


def main(image_file, mode):
    """ Retrieves the crop hint and crops to or draws the hint."""
    # [START main]
    vects = getCropHint(image_file)

    if mode == 'crop':
        cropToHint(image_file, vects)

    if mode == 'draw':
        drawHint(image_file, vects)
    # [END main]


if __name__ == '__main__':
    # [START parseargs]
    parser = argparse.ArgumentParser()
    parser.add_argument('image_file', help='The image you\'d like to crop.')
    parser.add_argument('mode', help='Set to "crop" or "draw".')
    args = parser.parse_args()
    main(args.image_file, args.mode)
    parser = argparse.ArgumentParser()
    # [END parseargs]
# [END full_tutorial]
