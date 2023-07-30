import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "teeTasteBackend.settings")
django.setup()

from teeTasteBackend.models import Shoe
from teeTasteBackend.feature_extraction import process_image

for shoe in Shoe.objects.all():
    if shoe.feature_vector is None:
        # This shoe doesn't have a feature vector, so compute and save it
        process_image(shoe)
