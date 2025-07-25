import csv
import os
from os import mkdir
from pathlib import Path


def save_to_csv(url, datas):
    """Function to save datas into csv file. The file is created if not existing.

    Args:
        url (str): The url to save csv file
        datas (dict): The product page datas in a dictionary
    """

    # Sorted product datas
    header = ["product_page_url",
              "universal_product_code",
              "title",
              "price_including_tax",
              "price_excluding_tax",
              "number_available",
              "product_description",
              "category",
              "review_rating",
              "image_url"]

    # Open the file in exclusive writing mode
    try:
        with open(url, 'x', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(header)

            # List comprehension for datas values
            writer.writerow([datas.get(key, "") for key in header])

    except FileExistsError:
        print("✅ File already exists")
