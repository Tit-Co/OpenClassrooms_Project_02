from scraper.config import csv_file, exec_errors, skipped_images, errors_path, skipped_images_path
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

    for category in all_categories:
        display_category(category)

        # Preparing csv file for the category
        cat = clean_spaces(category)
        csv_dir = Path(f"./data/{cat}/")
        csv_dir.mkdir(parents=True, exist_ok=True)
        csv_file = csv_dir / f"Books_{cat}.csv"

        if csv_file.exists():
            csv_file.unlink()

        # Extraction of all pages URL of a category
        book_urls_with_category = extract_books_urls_from_category(url, category)
        print(f"▻ Extracted urls : {book_urls_with_category}\n")

        book_count = 0
        # Loop for scraping all products url of the category example
        for book_url, cat in book_urls_with_category:

            # Extraction of datas from the product page url
            print("├ Extraction...🚧\n")
            extracted_datas = extract_data(book_url,exec_errors)

            # Transformation of datas
            transformed_datas = transform_data(extracted_datas)
            print("├ Transformation...⭮\n")

            # Save to CSV file
            save_to_csv(csv_file, transformed_datas)
            print("├ Saving to CSV file...💾")

            # Downloading image
            title = transformed_datas["title"]
            category = clean_spaces(cat)
            upc = transformed_datas["universal_product_code"]
            base = f"./data"
            image_url = transformed_datas['image_url']

            safe_title = clean_spaces(clean_filename(title))
            image_name = f"{safe_title}_{upc}.jpg"

            image_dir = Path(base) / category / Path("images")
            image_path = image_dir / image_name

            download_image(image_url, image_path, exec_errors, skipped_images)

            book_count += 1

        display_category_end(category, book_count)

    # Logging files
    if exec_errors:
        with open(errors_path, "w", encoding="utf-8") as f:
            for url, error in exec_errors:
                f.write(f"{url} → {error}\n")

    if skipped_images:
        with open(skipped_images_path, "w", encoding="utf-8") as f:
            for img in skipped_images:
                f.write(f"{img}\n")

    message=""
    if len(exec_errors) == 0:
        message = "\n\n😀"

    else:
        message = "\n\n🙁"
    print(f"{message} Download completed with {len(exec_errors)} error(s).")