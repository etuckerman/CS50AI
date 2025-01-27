# https://submit.cs50.io/check50/fac5087ad98c6ba4e3fdb9c6c877772ee6d5b000

import cv2
import numpy as np
import os
import sys
import tensorflow as tf

from sklearn.model_selection import train_test_split

TF_ENABLE_ONEDNN_OPTS = 0
EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4

# Set environment variable for TensorFlow
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """
    
    images = []
    labels = []

    for folder in os.listdir(data_dir):
        folder_path = os.path.join(data_dir, folder)
        if os.path.isdir(folder_path):  # Ensure folder_path is a directory
            for image_file in os.listdir(folder_path):
                image_path = os.path.join(folder_path, image_file)
                img = cv2.imread(image_path)
                if img is not None:
                    img = cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT))
                    images.append(img)
                    labels.append(int(folder))

    # Convert lists to NumPy arrays
    images = np.array(images)
    labels = np.array(labels)

    return images, labels

#model 1, low accuracy
#333/333 - 0s - 1ms/step - accuracy: 0.0558 - loss: 3.4993
# def get_model():
#     """
#     Returns a compiled convolutional neural network model. Assume that the
#     `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
#     The output layer should have `NUM_CATEGORIES` units, one for each category.
#     """
    
#     # Create a convolutional neural network
#     model = tf.keras.models.Sequential([

#         # Convolutional layer. Learn 32 filters using a 3x3 kernel
#         tf.keras.layers.Conv2D(
#             32, (3, 3), activation="relu", input_shape = (IMG_WIDTH, IMG_HEIGHT, 3)
#         ),

#         # Max-pooling layer, using 2x2 pool size
#         tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),

#         # Flatten units
#         tf.keras.layers.Flatten(),

#         # Add a hidden layer with dropout
#         tf.keras.layers.Dense(128, activation="relu"),
#         tf.keras.layers.Dropout(0.5),

#         # Add an output layer with output units for all NUM_CATAGORIES
#         tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
#     ])

#     # Train neural network
#     model.compile(
#         optimizer="adam",
#         loss="categorical_crossentropy",
#         metrics=["accuracy"]
#     )
    
#     return model

#model 2, semi-low accuracy (0.38)
# def get_model():
    # model = tf.keras.models.Sequential([
    #     tf.keras.layers.Conv2D(32, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
    #     tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
    #     tf.keras.layers.Flatten(),
    #     tf.keras.layers.Dense(128, activation="relu"),
    #     tf.keras.layers.Dropout(0.5),
    #     tf.keras.layers.Dense(NUM_CATEGORIES, activation="sigmoid")  # For binary classification, change NUM_CATEGORIES to 1
    # ])
    
    # model.compile(
    #     optimizer="sgd",
    #     loss="binary_crossentropy",
    #     metrics=["accuracy"]
    # )
    
    # return model
#model 3, hyper accuracy setup
#333/333 - 5s - 16ms/step - accuracy: 0.9876 - loss: 0.0425
def get_model():
    # Create a Sequential model
    model = tf.keras.models.Sequential([
        # Input layer specifying the shape of the input data
        tf.keras.layers.Input(shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        
        # First convolutional layer with 64 filters, 3x3 kernel, ReLU activation, and same padding
        tf.keras.layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
        # Batch normalization to stabilize and speed up training
        tf.keras.layers.BatchNormalization(),
        # Second convolutional layer with the same parameters as the first layer
        tf.keras.layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
        # Batch normalization
        tf.keras.layers.BatchNormalization(),
        # MaxPooling layer to reduce spatial dimensions by taking the maximum value in 2x2 pools
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
        # Dropout layer to prevent overfitting by randomly setting 50% of the input units to 0
        tf.keras.layers.Dropout(0.5),
        
        # Second set of convolutional layers with 128 filters
        tf.keras.layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
        tf.keras.layers.BatchNormalization(),
        # MaxPooling layer to reduce spatial dimensions
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
        # Dropout layer
        tf.keras.layers.Dropout(0.5),
        
        # Flatten layer to convert 2D matrix into a 1D vector
        tf.keras.layers.Flatten(),
        # Dense layer with 512 units and ReLU activation function
        tf.keras.layers.Dense(512, activation='relu'),
        # Dropout layer
        tf.keras.layers.Dropout(0.5),
        # Output layer with softmax activation for multi-class classification
        tf.keras.layers.Dense(NUM_CATEGORIES, activation='softmax')
    ])
    
    # Compile the model with Adam optimizer, categorical crossentropy loss, and accuracy metric
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4),  # Using a low learning rate for stable convergence
        loss='categorical_crossentropy',  # Suitable for multi-class classification
        metrics=['accuracy']  # Metric to monitor during training and evaluation
    )
    
    return model



if __name__ == "__main__":
    main()