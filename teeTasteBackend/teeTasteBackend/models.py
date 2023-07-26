from django.db import models


class UserInteraction(models.Model):
    session_id = models.CharField(max_length=200)
    selected_tshirt_id = models.CharField(max_length=200)
    not_selected_tshirt_id = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)


def get_interactions(session_id):
    interactions = UserInteraction.objects.filter(session_id=session_id)
    return list(interactions)
