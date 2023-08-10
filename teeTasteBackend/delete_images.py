"""
Module to delete all Shoe objects from the database.
"""

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "teeTasteBackend.settings")
django.setup()

# pylint: disable=wrong-import-position, import-error
from teeTasteBackend.models import Shoe

# Delete all Shoe objects
Shoe.objects.all().delete()
