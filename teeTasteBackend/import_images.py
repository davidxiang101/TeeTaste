import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "teeTasteBackend.settings")
django.setup()

from django.core.files import File
from teeTasteBackend.models import Shoe
from teeTasteBackend.feature_extraction import process_image

image_dir = "teeTasteBackend/webscrapers/images/StockXShoesImages"

for filename in os.listdir(image_dir):
    if filename.endswith(".jpg"):  # assuming you have only .jpg images
        # Check if a Shoe with this image already exists
        if not Shoe.objects.filter(image=filename).exists():
            with open(os.path.join(image_dir, filename), "rb") as f:
                image_file = File(f)
                shoe = Shoe()
                shoe.image.save(filename, image_file, save=False)  # Don't save yet
                # Process image and save feature vector
                process_image(shoe)
                shoe.save()  # Save the shoe object after processing image
