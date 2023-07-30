from django.http import HttpResponse
import uuid
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import UserInteraction
from django.core import serializers
from .models import Shoe
import random
from sklearn.metrics.pairwise import cosine_similarity


def fetch_next_shoes(request):
    shoe_count = Shoe.objects.count()
    if shoe_count >= 2:
        # Select a random shoe as the query shoe
        query_shoe = random.choice(Shoe.objects.all())

        # Calculate similarity with other shoes based on precomputed feature vectors
        similar_shoes = []
        for shoe in Shoe.objects.exclude(pk=query_shoe.pk):
            # Get their precomputed features
            shoe1_features = query_shoe.get_feature_vector()
            shoe2_features = shoe.get_feature_vector()

            similarity_score = cosine_similarity([shoe1_features], [shoe2_features])
            similar_shoes.append((shoe, similarity_score[0][0]))

        # Sort shoes based on similarity score in descending order
        similar_shoes.sort(key=lambda x: x[1], reverse=True)
        # Get the top 2 most similar shoes
        selected_shoes = [shoe[0] for shoe in similar_shoes[:2]]

        shoes_json = serializers.serialize("json", selected_shoes)
        return JsonResponse({"shoes": shoes_json}, safe=False)
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
