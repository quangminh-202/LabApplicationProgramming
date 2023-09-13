import requests
from bs4 import BeautifulSoup
import os
base_url = "https://otzovik.com/reviews/sberbank_rossii/?ratio="

if not os.path.exists("dataset"):
    os.makedirs("dataset")

def save_otzovik_to_file(otzovik, star_rating, index):
    folder_name = os.path.join("dataset", str(star_rating))
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    filename = os.path.join(folder_name, f"{index:04d}.txt")
    with open(filename, "w", encoding="utf-8") as file:
        file.write(otzovik)
    for page_num in range(1, 6):
        url = f"{base_url}{page_num}"
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            reviews = soup.find_all("div", class_="review-teaser")
            