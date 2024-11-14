# USAGE:
# python scan.py (--images <IMG_DIR> | --image <IMG_PATH>) [-i]
# For example, to scan a single image with interactive mode:
# python scan.py --image sample_images/desk.JPG -i
# To scan all images in a directory automatically:
# python scan.py --images sample_images

# Scanned images will be output to directory named 'output'

import argparse
import itertools
import math
import os

import cv2

from .scan import DocScanner


def main(args):

    im_dir = args["images"]
    im_file_path = args["image"]
    interactive_mode = args["i"]

    scanner = DocScanner(interactive_mode)

    valid_formats = [".jpg", ".jpeg", ".jp2", ".png", ".bmp", ".tiff", ".tif"]

    get_ext = lambda f: os.path.splitext(f)[1].lower()

    images = []
    # Scan single image specified by command line argument --image <IMAGE_PATH>
    if im_file_path:
        images.append((os.path.basename(im_file_path), scanner.scan(cv2.imread(im_file_path))))

    # Scan all valid images in directory specified by command line argument --images <IMAGE_DIR>
    if im_dir:
        images.extend([(os.path.basename(f), scanner.scan(cv2.imread('/'.join((im_dir, im)))))
                       for f in os.listdir(im_dir) if get_ext(f) in valid_formats])

    output_dir = '/'.join((os.getcwd(), 'output'))
    os.makedirs(output_dir, exist_ok=True)
    for name, image in images:
        print(name)
        cv2.imwrite('/'.join((output_dir, 'scanned_' + name)), image)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--images", help="Directory of images to be scanned")
    group.add_argument("--image", help="Path to single image to be scanned")
    parser.add_argument("-i", action='store_true',
        help = "Flag for manually verifying and/or setting document corners")

    args = vars(parser.parse_args())
    main(args)
