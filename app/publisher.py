import utils

import argparse 

# Initialize parser
description = 'Publisher: publishes images in input directory to broker\'s topic and move that file to published directory'
parser = argparse.ArgumentParser(description=description)
parser.add_argument("-i", "--input", required=True, help="path containing input images. (.png format)")
parser.add_argument("-p", "--published", required=True, help="path for moving input images once published.")
args = parser.parse_args()

print(f'\nCmd Args Received: {vars(args)}\n')

utils.isdir_check_and_exit(args.input, 'Not a valid input path')
utils.isdir_check_and_exit(args.published, 'Not a valid publish path')

input_files_path = args.input
published_files_path = args.published

import os, shutil, json
from PIL import Image
from numpy import asarray

# os.environ[] won't change dynamically in runtime for Python.
# Hence, it always returns the value of program start
# So, kept outside the infinite loop
broker = utils.get_broker()

print('\nPublisher started...')

while True:
    files = [f for f in os.listdir(input_files_path)]

    for f in files:
        image = Image.open(os.path.join(input_files_path, f))
        data = {'filename': f, 'img_data': asarray(image).tolist()}

        broker.publish(utils.input_topic_name, json.dumps(data))
        
        shutil.move(os.path.join(input_files_path, f), os.path.join(published_files_path, f))