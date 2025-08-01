from scraper.config import csv_file, image_errors, skipped_images, errors_path, skipped_images_path
from scraper.extract import get_all_categories, extract_books_urls_from_category, extract_data
from scraper.transform import transform_data, clean_spaces, clean_filename
from scraper.save import save_to_csv, download_image
from pathlib import Path


def display_category(cat):
    n = len(cat)
    c = "┈" * int((35 - n) / 2)
    l = "┈" * 60
    print(l)
    print(c + " PROCESSING CATEGORY ⯈⯈ " + cat + " " + c)
    print(l)

def display_category_end(cat, count):
    print(f"\n▻ Total books scraped for category {cat} : {count}")
    print(f"\n▻ Category {cat} saved to {csv_file}\n\n")
    print("─" * 60 + "\n")

def scraper(url):

    all_categories = get_all_categories(url)
    print(f"All categories extracted from {url}\n")

    first = True
    for category in all_categories:
        display_category(category)

        # Extraction of all pages URL of a category
        book_urls_with_category = extract_books_urls_from_category(url, category)
        print(f"▻ Extracted urls : {book_urls_with_category}\n")

        book_count = 0
        # Loop for scraping all products url of the category example
        for book_url, cat in book_urls_with_category:

            # Extraction of datas from the product page url
            print("├ Extraction...🚧\n")
            extracted_datas = extract_data(book_url)

            # Transformation of datas
            transformed_datas = transform_data(extracted_datas)
            print("├ Transformation...⭮\n")

            # Saving to csv file
            save_to_csv(csv_file, transformed_datas, write_header=first)
            print("├ Saving to CSV file...💾")

            # Downloading image
            title = transformed_datas["title"]
            category = clean_spaces(cat)
            upc = transformed_datas["universal_product_code"]
            base = "./data/images/"
            image_url = transformed_datas['image_url']

            safe_title = clean_spaces(clean_filename(title))
            image_name = f"{safe_title}_{upc}.jpg"

            image_dir = Path(base) / category / safe_title
            image_path = image_dir / image_name

            download_image(image_url, image_path, image_errors, skipped_images)

            first = False

            book_count += 1

        display_category_end(category, book_count)

    # Logging files
    if image_errors:
        with open(errors_path, "w", encoding="utf-8") as f:
            for url, error in image_errors:
                f.write(f"{url} → {error}\n")

    if skipped_images:
        with open(skipped_images_path, "w", encoding="utf-8") as f:
            for img in skipped_images:
                f.write(f"{img}\n")

    message=""
    if len(image_errors) == 0:
        message = "\n\n😀"

    else:
        message = "\n\n🙁"
    print(f"{message} Download completed with {len(image_errors)} error(s).")