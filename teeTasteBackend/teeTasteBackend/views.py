from django.http import HttpResponse
import uuid
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import UserInteraction


@csrf_exempt
def save_interaction(request):
    if request.method == "POST":
        session_id = request.POST.get("session_id")
        selected_tshirt_id = request.POST.get("selected_tshirt_id")
        not_selected_tshirt_id = request.POST.get("not_selected_tshirt_id")

        interaction = UserInteraction(
            session_id=session_id,
            selected_tshirt_id=selected_tshirt_id,
            not_selected_tshirt_id=not_selected_tshirt_id,
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
