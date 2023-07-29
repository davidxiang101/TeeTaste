import os
import django

os.environ["DJANGO_SETTINGS_MODULE"] = "teeTasteBackend.settings"
django.setup()

from django.core.files import File
from teeTasteBackend.models import Shoe

# Replace with your actual directory
image_dir = "teeTasteBackend/webscrapers/images/StockXShoesImages"

for filename in os.listdir(image_dir):
    if filename.endswith(".jpg"):  # assuming you have only .jpg images
        with open(os.path.join(image_dir, filename), "rb") as f:
            image_file = File(f)
            shoe = Shoe()
            shoe.image.save(filename, image_file, save=True)
