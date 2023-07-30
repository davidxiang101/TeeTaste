import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "teeTasteBackend.settings")
django.setup()

from teeTasteBackend.models import Shoe

# Delete all Shoe objects
Shoe.objects.all().delete()
