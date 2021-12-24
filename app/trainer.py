import os, gzip, time
import numpy as np
import utils

import argparse
 

# Initialize parser
description = 'Fashion MNIST trainer and exporter'
parser = argparse.ArgumentParser(description=description)
parser.add_argument("-i", "--images", required=True, help="path containing train images. (idx3-ubyte.gz format)")
parser.add_argument("-l", "--labels", required=True, help="path containing train labels. (idx1-ubyte.gz format)")
parser.add_argument("-e", "--export", required=True, help="path to export the trained model")
args = parser.parse_args()

print(f'\nCmd Args Received: {vars(args)}\n')

utils.isfile_check_and_exit(args.images, 'Not a valid images path')
utils.isfile_check_and_exit(args.labels, 'Not a valid labels path')
utils.isdir_check_and_exit(args.export, 'Not a valid export path')

import tensorflow as tf
from tensorflow import keras

with gzip.open(args.labels, 'rb') as lbpath:
    train_labels = np.frombuffer(lbpath.read(), np.uint8, offset=8)

with gzip.open(args.images, 'rb') as imgpath:
    train_images = np.frombuffer(imgpath.read(), np.uint8, offset=16).reshape(len(train_labels), 28, 28, 1)

print(f'\ntrain images shape: {train_images.shape}\n')
# print(train_images[0] / 255.0)

model = keras.Sequential([
  keras.layers.Conv2D(input_shape=(28,28,1), filters=8, kernel_size=3, 
                      strides=2, activation='relu', name='Conv1'),
  keras.layers.Flatten(),
  keras.layers.Dense(10, name='Dense')
])

epochs = 5

model.compile(optimizer='adam', 
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=[keras.metrics.SparseCategoricalAccuracy()])
model.fit(train_images, train_labels, epochs=epochs)

test_loss, test_acc = model.evaluate(train_images, train_labels)
print('\nTrain accuracy: {}\n'.format(test_acc))

export_answer = input('Do you want to export and serve the model? (y/n): ')
if export_answer in ['y', 'Y', 'yes', 'Yes']:
    MODEL_DIR = args.export
    version = round(time.time() * 1000)
    export_path = os.path.join(MODEL_DIR, str(version))
    print('\nexport_path = {}\n'.format(export_path))

    tf.keras.models.save_model(
        model,
        export_path,
        overwrite=True,
        include_optimizer=True,
        save_format=None,
        signatures=None,
        options=None
    )

    print('\nSaved model successfully\n')

