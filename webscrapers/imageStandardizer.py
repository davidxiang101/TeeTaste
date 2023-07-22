from PIL import Image
import os
import cv2

def verify_image_with_opencv(image_path):
    try:
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError("Failed to open image.")
        print("Image successfully opened with OpenCV.")
    except Exception as e:
        print(f"Error: {e}")


def standardize_images(input_folder, output_folder, target_width, target_height, output_format='PNG'):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for root, _, files in os.walk(input_folder):
        for filename in files:
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                input_path = os.path.join(root, filename)
                output_path = os.path.join(output_folder, filename)

                # Open the image
                img = Image.open(input_path)

                # Resize the image to fit the target width and height without stretching
                img.thumbnail((target_width, target_height))

                # Save the standardized image to the output folder
                img.save(output_path, format=output_format)
                print(f"Standardized: {filename}")

if __name__ == "__main__":
    input_folders = ["images/AEImages", "images/AmazonImages/mens_polos", "images/AmazonImages/mens_shirts", 
                     "images/AmazonImages/mens_tshirts", "images/AsosImages", 
                     "images/DiorImages", "images/GapGraphicImages", "images/GapImages", 
                     "images/GucciImages", "images/HMImages", "images/MacysImages",
                     "images/NorthFaceImages", "images/OldNavyImages", "images/PacSunImages",
                     "images/PradaImages", "images/RalphLaurenImages", "images/SssenseImages",
                     "images/TillysImages", "images/TommyHilfigerImages", "images/UniqloGraphicImages",
                     "images/UniqloImages", "images/UrbanOutfittersImages", "images/VansImages", "images/ZaraImages"]
    
    output_folders = ["standardizedImages/AEImagesStandardized", "standardizedImages/AmazonImages/mens_polosStandardized", "standardizedImages/AmazonImages/mens_shirtsStandardized", 
                     "standardizedImages/AmazonImages/mens_tshirtsStandardized", "standardizedImages/AsosImagesStandardized", 
                     "standardizedImages/DiorImagesStandardized", "standardizedImages/GapGraphicImagesStandardized", "standardizedImages/GapImagesStandardized", 
                     "standardizedImages/GucciImagesStandardized", "standardizedImages/HMImagesStandardized", "standardizedImages/MacysImagesStandardized",
                     "standardizedImages/NorthFaceImagesStandardized", "standardizedImages/OldNavyImagesStandardized", "standardizedImages/PacSunImagesStandardized",
                     "standardizedImages/PradaImagesStandardized", "standardizedImages/RalphLaurenImagesStandardized", "standardizedImages/SssenseImagesStandardized",
                     "standardizedImages/TillysImagesStandardized", "standardizedImages/TommyHilfigerImagesStandardized", "standardizedImages/UniqloGraphicImagesStandardized",
                     "standardizedImages/UniqloImagesStandardized", "standardizedImages/UrbanOutfittersImagesStandardized", "standardizedImages/VansImagesStandardized", "standardizedImages/ZaraImagesStandardized"]
    
    target_width = 400  # Replace with your desired width
    target_height = 400  # Replace with your desired height

    for i in range(len(input_folders)):
        standardize_images(input_folders[i], output_folders[i], target_width, target_height)