import os, gzip
import numpy as np
import utils
from PIL import Image

import argparse 

# Initialize parser
description = 'Unzip idx3-ubyte.gz to actual files'
parser = argparse.ArgumentParser(description=description)
parser.add_argument("-i", "--images", required=True, help="path containing test images. (idx3-ubyte.gz format)")
parser.add_argument("-l", "--labels", required=True, help="path containing test labels. (idx1-ubyte.gz format)")
parser.add_argument("-o", "--output", required=True, help="path to output folder")
parser.add_argument("-s", "--start", required=True, help="start index of the image to unzip in ubyte file", type=int)
parser.add_argument("-e", "--end", required=True, help="end index of the image to unzip in ubyte file", type=int)
args = parser.parse_args()

print(f'\nCmd Args Received: {vars(args)}\n')

utils.isfile_check_and_exit(args.images, 'Not a valid images path')
utils.isfile_check_and_exit(args.labels, 'Not a valid labels path')
utils.isdir_check_and_exit(args.output, 'Not a valid output path')


with gzip.open(args.labels, 'rb') as lbpath:
    train_labels = np.frombuffer(lbpath.read(), np.uint8, offset=8)

with gzip.open(args.images, 'rb') as imgpath:
    train_images = np.frombuffer(
        imgpath.read(), np.uint8, offset=16).reshape(len(train_labels), 28, 28, 1)

for i in range(args.start, args.end + 1):
    image = Image.fromarray(train_images[i].reshape(28,28))
    output_file_name = os.path.join(args.output, str(i) + '.png')
    image.save(output_file_name)
    print(f'\nSaved: {output_file_name}')