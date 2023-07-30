from django.db import models
import numpy as np
from .feature_extraction import process_image


class UserInteraction(models.Model):
    session_id = models.CharField(max_length=200)
    selected_shoe_id = models.CharField(max_length=200)
    not_selected_shoe_id = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)


def get_interactions(session_id):
    interactions = UserInteraction.objects.filter(session_id=session_id)
    return list(interactions)


class Shoe(models.Model):
    image = models.ImageField(upload_to="shoe_images/")
    feature_vector = models.TextField(null=True, blank=True)

    def get_feature_vector(self):
        # Convert the feature vector string back to a numpy array
        return np.fromstring(self.feature_vector, sep=",")

    def set_feature_vector(self, feature_vector):
        # Convert the numpy array to a string
        self.feature_vector = ",".join(map(str, feature_vector))
