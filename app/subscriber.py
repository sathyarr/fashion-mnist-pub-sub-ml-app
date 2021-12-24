import utils

import argparse 

# Initialize parser
description = 'Subscriber: subscribes the topic, processes and saves the result in output directory'
parser = argparse.ArgumentParser(description=description)
parser.add_argument("-o", "--output", required=True, help="path to save output images. (.png format)")
parser.add_argument("-u", "--url", required=True, help="URL endpoint of the tf model server to predict images")
args = parser.parse_args()

print(f'\nCmd Args Received: {vars(args)}\n')

utils.isdir_check_and_exit(args.output, 'Not a valid output path')

predicted_files_path = args.output
tf_serving_api = args.url

import os, json
import numpy as np
from PIL import Image


# os.environ[] won't change dynamically in runtime for Python.
# Hence, it always returns the value of program start
# So, kept outside the infinite loop
broker = utils.get_broker()


print('\nSubscriber started...')

class_names = ['T-shirt-top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

while True:
    subscribed_data_raw = broker.subscribe(utils.input_topic_name)
    if subscribed_data_raw != None: # Google PubSub requires
        subscribed_data = json.loads(subscribed_data_raw)

        img_data_np_array = np.array(subscribed_data['img_data'], np.uint8).reshape(1, 28, 28, 1) # TODO: because of same shape in training

        data = json.dumps({"signature_name": "serving_default", "instances": img_data_np_array.tolist()})

        import requests
        headers = {"content-type": "application/json"}
        json_response = requests.post(tf_serving_api, data=data, headers=headers)
        predictions = json.loads(json_response.text)['predictions']
        predicted_class = np.argmax(predictions[0])

        def save():
            image = Image.fromarray(img_data_np_array.reshape(28,28))
            filename_split = subscribed_data['filename'].split('.')
            save_filename = filename_split[0] + '-' + class_names[predicted_class] + '.' + filename_split[1]
            image.save(os.path.join(predicted_files_path, save_filename))

        save()