from scraper.extract import extract_data
from scraper.transform import transform_data
from scraper.save import save_to_csv

# URL of a product page example
url = "https://books.toscrape.com/catalogue/misery_332/index.html"

# Extraction of datas from the product page url
extracted_datas = extract_data(url)

# Transformation of datas
transformed_datas = transform_data(extracted_datas)

# Saving to csv file
csv_file="./data/books.csv"
save_to_csv(csv_file, transformed_datas)


