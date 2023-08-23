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
from django.views.decorators.http import require_POST
from django.core.serializers import serialize
import numpy as np
import json


# Assuming feature vectors are of length 346112
t = AnnoyIndex(346112, "angular")

# Build the index
for shoe in Shoe.objects.all():
    t.add_item(shoe.pk, shoe.get_feature_vector())

# Build a tree for the index - increase the number of trees for more precision
t.build(2)


@csrf_exempt
@require_POST
def get_recommendations(request):
    try:
        body_unicode = request.body.decode("utf-8")
        body_data = json.loads(body_unicode)
        selected_shoes_ids = body_data.get("selected_shoes_ids")
        selected_shoes = [Shoe.objects.get(pk=pk) for pk in selected_shoes_ids]

        recommendations = []
        for shoe in selected_shoes:
            # Get the 10 most similar shoes
            indices = t.get_nns_by_vector(
                shoe.get_feature_vector(), 10, include_distances=False
            )

            # Exclude the query shoe itself
            similar_shoes = [
                Shoe.objects.get(pk=index) for index in indices if index != shoe.pk
            ]
            recommendations += similar_shoes

        # Serialize the queryset to JSON
        shoes_json_str = serialize("json", recommendations)

        # Parse the serialized JSON string to convert it into actual JSON objects
        shoes_json = json.loads(shoes_json_str)

        return JsonResponse({"recommendations": shoes_json}, safe=False)
    except Exception as e:
        print(e)
        return JsonResponse({"error": str(e)}, status=400)


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


def fetch_random_shoes(request):
    MAX_RETRIES = 5  # Maximum number of times we try to get dissimilar shoes

    max_distance = 0
    max_distance_shoes = (None, None)

    for _ in range(MAX_RETRIES):
        shoes = Shoe.objects.order_by("?")[:2]
        shoe1 = shoes[0]
        shoe2 = shoes[1]

        # Compute cosine distance between feature vectors
        distance = cosine_distances(
            np.array([shoe1.get_feature_vector()]),
            np.array([shoe2.get_feature_vector()]),
        )[0][
            0
        ]  # extract scalar value

        # Update the max distance and corresponding shoes if this distance is greater
        if distance > max_distance:
            max_distance = distance
            max_distance_shoes = (shoe1, shoe2)

        # You can adjust this threshold to define "dissimilarity"
        print(distance)
        if distance > 0.5:  # assuming distance ranges between 0 and 1
            shoes_json = serializers.serialize("json", [shoe1, shoe2])
            return JsonResponse({"shoes": shoes_json}, safe=False)

    # If we reach here, it means none of the retries were greater than the threshold.
    # So, return the pair with the max distance found.
    if max_distance_shoes[0] and max_distance_shoes[1]:
        shoes_json = serializers.serialize("json", max_distance_shoes)
        return JsonResponse({"shoes": shoes_json}, safe=False)

    return JsonResponse({"error": "Couldn't find any pair of shoes"}, status=400)


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
    response.set_cookie(
        "session_id",
        value="session_id",
        secure=True,
        samesite="None",
        max_age=30 * 24 * 60 * 60,
    )
    return response


def read_session_cookie(request):
    session_id = request.COOKIES.get("session_id", None)
    if session_id is not None:
        return HttpResponse(f"Session ID is: {session_id}")
    else:
        return HttpResponse("No session cookie found.")


def select_shoe(request, shoe_id):
    selected_shoes = request.session.get("selected_shoes", [])
    selected_shoes.append(shoe_id)
    request.session["selected_shoes"] = selected_shoes
    return HttpResponse("Shoe selected")


def view_selected_shoes(request):
    selected_shoes = request.session.get("selected_shoes", [])
    shoes = Shoe.objects.filter(id__in=selected_shoes)
    # Now do something with the shoes, like rendering them in a template
