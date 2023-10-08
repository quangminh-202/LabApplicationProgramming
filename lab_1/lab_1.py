import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import os
import time

def download_reviews(base_url, num_pages):
    if not os.path.exists("dataset"):
        os.makedirs("dataset")

    for page in range(20, num_pages + 1):
        ua = UserAgent()
        user_agent = ua.random
        print("User-Agent: ", user_agent)
        headers = {"User-Agent": user_agent}
        page_url = f"{base_url}{page}/?ratio=3"
        time.sleep(20)
        response = requests.get(page_url, headers=headers)
        print(response.status_code)

        if response.status_code == 200:
            print("Success")
            soup = BeautifulSoup(response.content, 'html.parser')
            time.sleep(10)
            titles = soup.find_all('a', class_='review-title')
            time.sleep(10)
            ratings = soup.find_all('div', class_='product-rating tooltip-right')

            for title, rating in zip(titles, ratings):
                rating_text = rating['title']
                num_rating = rating_text[-1]
                comment_text = title.text
                rating_folder = os.path.join("dataset", num_rating)

                if not os.path.exists(rating_folder):
                    os.makedirs(rating_folder)

                files_in_rating_folder = os.listdir(rating_folder)
                file_number = len(files_in_rating_folder) + 1
                file_name = f"{file_number:04d}.txt"

                with open(os.path.join(rating_folder, file_name), "w", encoding="utf-8") as file:
                    file.write(comment_text)
        else:
            print("Unsuccessful")


if __name__ == "__main__":
    base_url = "https://otzovik.com/reviews/sberbank_rossii/"
    num_pages = 32
    download_reviews(base_url, num_pages)
