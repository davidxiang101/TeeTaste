from django.http import HttpResponse
import uuid
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import UserInteraction
from django.core import serializers
from .models import Shoe
import random
from annoy import AnnoyIndex
from sklearn.metrics.pairwise import cosine_distances
import numpy as np


# Assuming feature vectors are of length 346112
t = AnnoyIndex(346112, "angular")

# Build the index
for shoe in Shoe.objects.all():
    t.add_item(shoe.pk, shoe.get_feature_vector())

# Build a tree for the index - increase the number of trees for more precision
t.build(2)


# Use the index in your view
def fetch_next_shoes(request):
    shoe_count = Shoe.objects.count()
    if shoe_count >= 2:
        # Select a random shoe as the query shoe
        query_shoe = random.choice(Shoe.objects.all())

        # Find the 10 most similar shoes
        indices, distances = t.get_nns_by_vector(
            query_shoe.get_feature_vector(), 10, include_distances=True
        )

        # Fetch the actual Shoe instances along with their distances
        similar_shoes = [
            (Shoe.objects.get(pk=index), distance)
            for index, distance in zip(indices, distances)
        ]

        # Select the top 2 most similar shoes
        selected_shoes = [shoe[0] for shoe in similar_shoes[:2]]

        shoes_json = serializers.serialize("json", selected_shoes)
        return JsonResponse({"shoes": shoes_json}, safe=False)
    else:
        return JsonResponse({"error": "Not enough shoes in the database"}, status=400)


MAX_RETRIES = 10  # Maximum number of times we try to get dissimilar shoes


def fetch_random_shoes(request):
    shoe_count = Shoe.objects.count()

    if shoe_count >= 2:
        retries = 0
        while retries < MAX_RETRIES:
            shoe1, shoe2 = random.sample(list(Shoe.objects.all()), 2)

            # Compute cosine distance between feature vectors
            # Note: the `get_feature_vector()` method should return the vector in a format that's
            # compatible with cosine_distances, such as a list or numpy array.
            distance = cosine_distances(
                np.array([shoe1.get_feature_vector()]),
                np.array([shoe2.get_feature_vector()]),
            )[0][
                0
            ]  # extract scalar value

            # You can adjust this threshold to define "dissimilarity"
            if distance > 0.5:  # assuming distance ranges between 0 and 1
                shoes_json = serializers.serialize("json", [shoe1, shoe2])
                return JsonResponse({"shoes": shoes_json}, safe=False)

            retries += 1

        return JsonResponse(
            {"error": "Couldn't find dissimilar shoes in the given tries"}, status=400
        )
    else:
        return JsonResponse({"error": "Not enough shoes in the database"}, status=400)


def get_interactions(session_id):
    interactions = UserInteraction.objects.filter(session_id=session_id)
    return list(interactions)


@csrf_exempt
def save_interaction(request):
    if request.method == "POST":
        session_id = read_session_cookie(request)
        if session_id is None:
            response = set_session_cookie(request)
            session_id = response.cookies["session_id"].value
        # session_id = request.POST.get("session_id")
        selected_shoe_id = request.POST.get("selected_shoe_id")
        not_selected_shoe_id = request.POST.get("not_selected_shoe_id")

        interaction = UserInteraction(
            session_id=session_id,
            selected_shoe_id=selected_shoe_id,
            not_selected_shoe_id=not_selected_shoe_id,
        )
        interaction.save()

        return JsonResponse({"status": "ok"}, status=200)
    else:
        return JsonResponse({"error": "Invalid HTTP method"}, status=400)


def set_session_cookie(request):
    response = HttpResponse("Setting a session cookie")
    session_id = uuid.uuid4()
    response.set_cookie("session_id", session_id, max_age=30 * 24 * 60 * 60)  # 30 days
    return response


def read_session_cookie(request):
    session_id = request.COOKIES.get("session_id", None)
    if session_id is not None:
        return HttpResponse(f"Session ID is: {session_id}")
    else:
        return HttpResponse("No session cookie found.")
