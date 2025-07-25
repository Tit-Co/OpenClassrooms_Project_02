from pathlib import Path, PurePosixPath

def transform_data(datas):
    """Function that transforms data from the dictionary get after extraction

    Args:
        datas (dict): Dictionary of datas

    Returns: The transformed datas dictionary

    """

    # Transform image url
    product_url = datas["product_page_url"]
    img_url = datas["img_url"]

    img_url_root = Path(product_url).parent.parent.parent

    transformed_img_url = PurePosixPath(img_url).relative_to("..", "..")

    absolute_img_url = img_url_root / transformed_img_url

    datas["img_url"] = absolute_img_url


    # Transform prices into floats
    pet = datas['price_excluding_tax']
    pit = datas['price_including_tax']

    float_pet = float(pet.split('£')[1])
    float_pit = float(pit.split('£')[1])

    datas['price_excluding_tax'] = float_pet
    datas['price_including_tax'] = float_pit


    # Transform product availability into integer
    availability_str = datas['number_available']

    availability_list = availability_str.split('(')
    availability_num = int(availability_list[1][0])

    datas['number_available'] = availability_num

    return datas
