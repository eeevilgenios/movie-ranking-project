import requests
import csv

def download_image(url, save_path):
    try:
        # Send an HTTP GET request to the image URL
        response = requests.get(url, stream=True)
        # Check if the request was successful
        response.raise_for_status()
        
        # Open the save path in binary write mode and save the image
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        
        print(f"Image successfully downloaded to {save_path}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download image: {e}")

# Example usage

posters = {}
with open("unsorted - Copy.csv","r") as f:
    reader = csv.reader(f)
    for row in reader:
        movie = row[0]
        url = row[1]
        if not url:
            continue
        posters[movie] = url
        image_url = posters[movie]
        save_path = "C:\\Users\\jonah\\Desktop\\Aidan_Ranking_Project\\Updated_Ranking\\poster_images\\" + movie + ".jpg"
        download_image(image_url, save_path)
