from django.db import models
from django.contrib.auth.models import AbstractUser


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

class User(AbstractUser):
    is_manager = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)

    def __str__(self):
        return self.username