# 1. Install Dependencies - DONE
# 2. Import Dependencies - DONE
import cv2
import os
import uuid
import random

import keras
import numpy as np
from matplotlib import pyplot as plt

# 3. Import tensorflow dependencies (Functional API) - DONE
from keras.models import Model
from keras.layers import Layer, Conv2D, Dense, MaxPooling2D, Input, Flatten
import tensorflow as tf
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# 4. Setting GPU Memory Consumption Growth (Prevent tensorflow from consuming too much GPU)
gpus = tf.config.experimental.list_physical_devices('GPU')
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)

for gpu in gpus:
    print(gpu)

# 5. Creating Folder structures
# Set up the folders to use
# All 3 folders are under 'data' folder
positivePath = os.path.join("Users", "ADMIN", "Desktop", "Programming", 'Python', 'FaceRecogn (App)', 'data', 'negative')  # positive verifies True for recognition
negativePath = os.path.join("Users", "ADMIN", "Desktop", "Programming", 'Python', 'FaceRecogn (App)', 'data', 'negative')  # negative verifies False for recognition
anchor = os.path.join("Users", "ADMIN", "Desktop", "Programming", 'Python', 'FaceRecogn (App)', 'data', 'negative')  # anchor is the actual image to be verified

# Make the directories
'''os.makedirs(positivePath)
os.makedirs(negativePath)
os.makedirs(anchor)'''


# 6. Untar(Uncompress) labelled Faces in the wild Dataset
# link: http://vis-www.cs.umass.edu/lfw/#download
# Uncompress file to current project file

# 7. Move lfw Images to data/negative
'''for directory in os.listdir('lfw'):
    for file in os.listdir(os.path.join('lfw', directory)):
        exPath = os.path.join('lfw', directory, file)  # current path
        newPath = os.path.join(negativePath, file)  # new path
        os.replace(exPath, newPath)'''

# 8. Collect positive and anchor classes
# Webcam set up
'''cap = cv2.VideoCapture(0)
while cap.isOpened():
    ret, frame = cap.read()

    # cut down pixel count to 250px X 250px
    frame = frame[120:120 + 250, 120:120 + 250, :]
    # print(frame.shape)

    # Collect anchors
    if cv2.waitKey(1) & 0XFF == ord('a'):
        # unique file path
        imgName = os.path.join(anchor, '{}.jpg'.format(uuid.uuid1()))
        cv2.imwrite(imgName, frame)
    # Collect Positives
    if cv2.waitKey(1) & 0XFF == ord('p'):
        # unique file path
        imgName = os.path.join(positivePath, '{}.jpg'.format(uuid.uuid1()))
        cv2.imwrite(imgName, frame)
    cv2.imshow('Image Collection', frame)

    if cv2.waitKey(1) & 0XFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()'''

# 9. Load and preprocess images
# Get directories
anchor = tf.data.Dataset.list_files(anchor+'/*.jpg').take(100)
positivePath = tf.data.Dataset.list_files(positivePath+'/*.jpg').take(100)
negativePath = tf.data.Dataset.list_files(negativePath+'/*.jpg').take(100)


# Preprocessing (scaling and resize)
def preprocess(file_path):
    byte_img = tf.io.read_file(file_path)
    img = tf.io.decode_jpeg(byte_img)
    img = tf.image.resize(img, (100, 100))
    img = img / 255.0
    return img


# 10. Create label dataset
# (anchor, positive) = ones
# (anchor, negative) = zeros

print(tf.ones(len(anchor)))
positives = tf.data.Dataset.zip((anchor, positivePath, tf.data.Dataset.from_tensor_slices(tf.ones(len(anchor)))))
negatives = tf.data.Dataset.zip((anchor, negativePath, tf.data.Dataset.from_tensor_slices(tf.ones(len(anchor)))))
data = positives.concatenate(negatives)

# Build train and test partition


def preprocess_twin(input_img, validation_img, label):
    return preprocess(input_img), preprocess(validation_img), label


# Dataloader pipeline
data = data.map(preprocess_twin)
data = data.cache()
data = data.shuffle(buffer_size=1024)

# Training partition
train = data.take(round(len(data)*.7))
train = train.batch(16)
train = train.prefetch(8)

# Test partition
test = data.skip(round(len(data)*.7))
test = test.take(round(len(data)*.3))
test = test.batch(16)
test = test.prefetch(8)


# 11. Build embedding layer
def make_embed():
    inputlayer = Input(shape=(100, 100, 3), name='Input img')

    # First Block
    cov1 = Conv2D(64, (10, 10), activation='relu')(inputlayer)
    max1 = MaxPooling2D(64, (2, 2), padding='same')(cov1)

    # Second Block
    cov2 = Conv2D(128, (7, 7), activation='relu')(max1)
    max2 = MaxPooling2D(64, (2, 2), padding='same')(cov2)

    # Third Block
    cov3 = Conv2D(128, (4, 4), activation='relu')(max2)
    max3 = MaxPooling2D(64, (2, 2), padding='same')(cov3)

    # Final Block
    cov4 = Conv2D(256, (4, 4), activation='relu')(max3)
    final1 = Flatten()(cov4)
    dense1 = Dense(4096, activation='sigmoid')(final1)

    return Model(inputs=[inputlayer], outputs=[dense1], name=['embedding'])


embedding = make_embed()
print(embedding.summary())


# 12. Build distance layer
class DistLayer(Layer):
    def __int__(self, **kwargs):
        super().__init__()

    # similarity calculation
    @staticmethod
    def calling(self, input_embed, valid_embed):
        return tf.math.abs(input_embed - valid_embed)


# 13. Siamese model
def siamese_model():
    # Inputs
    input_image = Input(name='Input Image', shape=(100, 100, 3))
    # validation
    valid_image = Input(name='Valid Image', shape=(100, 100, 3))
    # Combine siamese distance components
    siameselayer = DistLayer()
    siameselayer._name = 'Distance'
    distances = siameselayer(embedding(input_image), embedding(valid_image))

    # Classification layer
    classifier = Dense(1, activation='sigmoid')(distances)

    return Model(inputs=[input_image, valid_image], outputs=classifier, name='Siamese Network')


siamese_model = siamese_model()
print(siamese_model.summary())
