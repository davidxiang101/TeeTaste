import os

# Step 1: Read sneakers.txt and store the links and corresponding image numbers
links = []
imgs = []
dupImgs = []
dupLinks = []
with open('sneakers.txt', 'r') as f:
    for line in f:
        parts = line.strip().split()
        img_number = parts[1].split(':')[0]
        link = parts[2]
        if link in links:
            dupImgs.append(img_number)
            dupLinks.append(link)
        else:
            imgs.append(img_number)
            links.append(link)

with open('sneakersTrimmed.txt', 'w') as f:
    for i in range(len(imgs)):
        nondupImg = (f'Image {imgs[i]}: {links[i]}\n')
        f.write(nondupImg)

with open('sneakersDeleted.txt', 'w') as f:
    for i in range(len(dupLinks)):
        deletedImage = (f'Image {dupImgs[i]}: {dupLinks[i]}\n')
        f.write(deletedImage)

directory = "images/sneakers"  # Directory containing the files
for img_number in dupImgs:
    filename = f"image_{img_number}.jpg"
    file_path = os.path.join(directory, filename)

    try:
        os.remove(file_path)
        print(f"Deleted {filename}")
    except FileNotFoundError:
        print(f"File {filename} not found")
    except Exception as e:
        print(f"Error deleting {filename}: {e}")