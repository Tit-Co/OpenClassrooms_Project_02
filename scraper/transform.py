from unidecode import unidecode
import re
from urllib.parse import urljoin


def remove_accents(text):
    """Functions that removes accents from a string.

    Args:
        text (string): Text to be cleaned.

    Returns: The cleaned string
    """
    return unidecode(text)



def clean_spaces(text):
    """Function that cleans all types of spaces from a string

    Args:
        text (string): Text to be cleaned.

    Returns:The cleaned string

    """
    return re.sub(r'\s+', '_', text)



def clean_filename(name):
    """Function that cleans a filename from a string and limit it to 100 characters.

    Args:
        name (string): Filename to be cleaned.

    Returns: The cleaned filename

    """
    # Remove accents
    name = remove_accents(name)

    # Replace space and + by dash, and remove "!", "(", ")", "[", "]", "#", "%"
    name = name.replace(" ", "-")
    name = name.replace("+", "-")
    name = name.replace("!", "")
    name = name.replace('&', 'and')
    name = name.replace('[', '').replace(']', '')
    name = name.replace('(', '').replace(')', '')
    name = name.replace("#", "")
    name = name.replace("%", "percent")

    # Remove coma and dot
    name = name.replace(",", "")
    name = name.replace(".", "")

    # Remove prohibited characters and replace by a dash
    name = re.sub(r'[\\/*?:"<>|]', "-", name)

    # Replace apostrophe and quotation marks
    apostrophes = ["'", "’", "‘", "`", "´"]
    quotation_marks = [
    "'",
    "‘",
    "’",
    "‚",

    '"',
    "“",
    "”",
    "„",
    "‟",

    "«",
    "»"]

    for a in apostrophes:
        name = name.replace(a, "-")

    for q in quotation_marks:
        name = name.replace(q, "-")

    # Remove double occurrence of dash
    name = re.sub(r'-+', "-", name)

    # Remove dash at the end if exists
    name = name.rstrip("-")

    # Limit the length to avoid runtime error
    return name[:100]



def transform_data(datas):
    """Function that transforms data from the dictionary got after extraction

    Args:
        datas (dict): Dictionary of datas

    Returns: The transformed datas dictionary

    """

    # Transform image url
    new_datas = datas
    product_url = datas["product_page_url"]
    img_relative_url = datas["image_url"]  # ex: "../../media/cache/...jpg"


    # Create absolute image URL
    absolute_img_url = urljoin(product_url, img_relative_url)

    new_datas["image_url"] = absolute_img_url



    # Transform prices into floats
    pet = datas['price_excluding_tax']
    pit = datas['price_including_tax']

    float_pet = float(pet.split('£')[1])
    float_pit = float(pit.split('£')[1])

    new_datas['price_excluding_tax'] = float_pet
    new_datas['price_including_tax'] = float_pit


    # Transform product availability into integer
    availability_str = datas['number_available']

    availability_list = availability_str.split('(')
    availability_num = int(availability_list[1][0])

    new_datas['number_available'] = availability_num

    return new_datas