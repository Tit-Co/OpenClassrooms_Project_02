from scraper.extract import extract_data, extract_urls_from_category
from scraper.transform import transform_data
from scraper.save import save_to_csv

# URL of a product page example
url = "https://books.toscrape.com/catalogue/misery_332/index.html"

# Index URL
index_url = "https://books.toscrape.com/"

# CSV file
csv_file = "./data/books.csv"

# Category example
category = "Romance"

# Extraction of all pages URL of a category
extracted_urls = extract_urls_from_category(index_url, category)

# Loop for scraping all products url of the category example
first = True
for url in extracted_urls:

    # Extraction of datas from the product page url
    extracted_datas = extract_data(url)

    # Transformation of datas
    transformed_datas = transform_data(extracted_datas)
    print("Transformation...")

    # Saving to csv file
    save_to_csv(csv_file, transformed_datas, write_header=first)
    print("Saving to CSV file...")
    first = False

print("Done !")




