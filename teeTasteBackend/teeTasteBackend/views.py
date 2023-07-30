from django.http import HttpResponse
import uuid
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import UserInteraction
from django.core import serializers
from .models import Shoe
import random

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User

from django.contrib.auth import login

class UserAuthenticationView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                # Password matches
                login(request, user)  # Log the user in (optional)
                return Response({'message': 'User authenticated', 'user_id': user.id})
            else:
                # Password does not match
                return Response({'message': 'Authentication failed'}, status=status.HTTP_401_UNAUTHORIZED)

        except User.DoesNotExist:
            # User does not exist
            return Response({'message': 'Authentication failed'}, status=status.HTTP_401_UNAUTHORIZED)

class CreateUserView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        # Check if a user with the given username already exists
        if User.objects.filter(username=username).exists():
            return Response({'message': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        # Create the user
        user = User.objects.create_user(username=username, password=password, email=email)

        # Optionally, you can log in the user after creation
        # (You'll need to have the appropriate authentication backend configured)
        # from django.contrib.auth import login
        # login(request, user)

        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)

def fetch_next_shoes(request):
    shoe_count = Shoe.objects.count()
    if shoe_count >= 2:
        random_indexes = random.sample(range(shoe_count), 2)
        shoes = [Shoe.objects.all()[i] for i in random_indexes]
        shoes_json = serializers.serialize("json", shoes)
        return JsonResponse({"shoes": shoes_json}, safe=False)
    else:
        return JsonResponse(
            {"error": "Not enough T-shirts in the database"}, status=400
        )


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


