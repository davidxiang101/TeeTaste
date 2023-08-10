from keras.preprocessing import image
from keras.applications.resnet50 import preprocess_input, ResNet50
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Load the pretrained model
model = ResNet50(weights="imagenet", include_top=False)


def process_image(shoe, save_shoe=True):
    print("Loading image from:", shoe.image.path)

    img = image.load_img(shoe.image.path, target_size=(400, 400))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    # Get features
    features = model.predict(x)

    # Flatten the features
    features_flattened = features.reshape(1, -1)

    # Save the feature vector to the database
    shoe.set_feature_vector(features_flattened[0])

    if save_shoe:
        shoe.save()

    return features_flattened


# Define the function to calculate similarity using cosine similarity
def calculate_similarity(shoe1_features, shoe2_features):
    similarity = cosine_similarity(shoe1_features, shoe2_features)
    return similarity[0][0]
