import os
from keras.preprocessing import image
from keras.applications.resnet50 import preprocess_input, ResNet50
import numpy as np

# Load the pretrained model
model = ResNet50(weights="imagenet", include_top=False)


# Define a function to process a single image
def process_image(img_path):
    img = image.load_img(img_path, target_size=(400, 400))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    # Get features
    features = model.predict(x)

    # Flatten the features
    features_flattened = features.reshape(1, -1)

    return features_flattened


# Specify the directory where your images are
dir_path = "../webscrapers/standardizedImages/"

# Create an empty dictionary to store the features
features_dict = {}

# Loop over all subdirectories and files in dir_path
for subdir, dirs, files in os.walk(dir_path):
    for file in files:
        # Construct the full file path
        file_path = os.path.join(subdir, file)

        # Check if the file is an image (you can add more types if needed)
        if file_path.endswith(".jpg") or file_path.endswith(".png"):
            # Process the image and store the features
            features_dict[file] = process_image(file_path)

# features_dict contains the features of each image, indexed by the image filename.
