import csv
import requests
from pathlib import Path

def download_image(url_img, file_path, errors_log, skipped_images):
    """Function that downloads an image from a url and saves it in the given path.
    Two lists are given in parameters in order to log the errors and skipped images.

    Args:
        url_img (string): URL where the image should be downloaded.
        file_path (string): Path where the image should be saved.
        errors_log (list): List of errors logged.
        skipped_images (list): List of skipped images.
    """


    print(f"\n├ Saving image... {url_img}")

    try:
        page = requests.get(url_img, timeout=10)
        page.raise_for_status()

        directory = file_path.parent
        directory.mkdir(parents=True, exist_ok=True)

        print(f"➥ Image destination : {file_path}")
        print(f"➥ Path length : {len(str(file_path))}")

        if not file_path.exists():
            with open(file_path, "wb") as fp:
                fp.write(page.content)
                print("✅ Image downloaded successfully.")
        else :
            print(f"⚠️ Image already exists : {file_path}")
            skipped_images.append(file_path)

        print("═════\n")

    except Exception as e:
        print(f"❌ Error for {url_img} → {e}\n")
        errors_log.append((url_img, str(e)))



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


    file_path = Path(url)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # verify if file path exists or not and declare boolean accordingly
    write_header = not file_path.exists()

    # Open the file in 'append' writing mode
    with open(url, "a", newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)

        # if file doesn't exist, file is created and header is written
        if write_header:
            writer.writerow(header)
        
        writer.writerow([datas.get(key, "") for key in header])


