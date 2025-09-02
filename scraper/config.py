from pathlib import Path
import shutil
import os
from scraper.models import Book, Category, Library

# Index page url
index_url = "https://books.toscrape.com/"

# CSV file
csv_file = ""

# Book, Category and Library objects
my_book = Book("","","",0.0,0, "")
my_category = Category("",[])
my_library = Library([])

# Errors list and path
exec_errors = []
errors_path = Path("../data/exec_errors.txt")
errors_path.parent.mkdir(parents=True, exist_ok=True)

# Skipped images list and path
skipped_images = []
skipped_images_path = Path("../data/skipped_images.txt")
skipped_images_path.parent.mkdir(parents=True, exist_ok=True)

# Remove folders and files if exist
data_dir = Path("../data/images/")
if data_dir.exists():
    shutil.rmtree(data_dir)
print("🧹 Dossier ../data/images/ supprimé.")

if errors_path.exists():
    os.remove(errors_path)

if skipped_images_path.exists():
    os.remove(skipped_images_path)