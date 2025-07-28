import requests
from bs4 import BeautifulSoup

def extract_data(url):
    """Function that extracts datas from url.
    The given url represents a product page i.e. a book page

    Args:
        url (string): The product page url

    Returns: The extracted datas dictionary

    """

    # Page of the associated url
    page = requests.get(url)

    if page.status_code != 200:
        print(f"Error: {page.status_code}")
        return None

    soup = BeautifulSoup(page.content, 'html.parser')

    # Dict for collecting all datas
    all_datas = dict()

    all_datas['product_page_url'] = url


    # Extraction of product title
    title = soup.find('li', class_='active').string
    all_datas['title'] = title


    # Extraction of product category
    all_li = soup.find_all('li')
    a_list2 = []
    for li in all_li:
        a_list = li.find_all('a')
        for a in a_list:
            if a.string=='Home' or a.string=='Books' or a.string==None:
                continue
            else:
                a_list2.append(a.string)
    category = a_list2[0]
    all_datas['category'] = category


    # Extraction of universal product code, prices and availability
    all_th = soup.find_all("th")
    all_td = soup.find_all("td")

    for th in all_th:
        match th.string:
            case "UPC":
                upc = all_td[0].string
                all_datas['universal_product_code'] = upc

            case "Price (excl. tax)":
                price_excluding_tax = all_td[2].string
                all_datas['price_excluding_tax'] = price_excluding_tax

            case "Price (incl. tax)":
                price_including_tax = all_td[3].string
                all_datas['price_including_tax'] = price_including_tax

            case "Availability":
                availability_str = all_td[5].string
                all_datas['number_available'] = availability_str


    # Extraction of product description and review rating
    all_p = soup.find_all('p')
    description = all_p[3].string
    all_datas['product_description'] = description


    # Extraction of review rating
    rating_tag = soup.find("p", class_="star-rating")
    rating_classes = rating_tag.get("class",[])
    review_rating = 0
    rating_map = {
        "Zero" : 0,
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }
    for cls in rating_classes:
        if cls in rating_map:
            review_rating = rating_map[cls]
            break

    all_datas['review_rating'] = review_rating


    # Extraction of image url
    img_tag = soup.find('img', attrs={'alt': all_datas['title']})
    img_url = img_tag['src']
    all_datas['image_url'] = img_url


    return all_datas


def extract_url_from_category(url, category):

    page = requests.get(url)

    if page.status_code != 200:
        print(f"Error: {page.status_code}")
        return None

    soup = BeautifulSoup(page.content, 'html.parser')

    # Extraction of urls
    all_a = soup.find_all('a')

    category_url=""

    for a in all_a:
        href = a.get('href')
        if category.lower() in href and "category" in href:
            category_url = href
            break

    return url + category_url


def get_page_number(soup):

    page_number = 0
    li = soup.find('li', class_='current')
    if li == None:
        page_number = 1
    else:
        li_lst = li.string.split()
        for el in li_lst:
            if el == " " or el == "\n":
                li_lst.remove(el)
        page_number = int(li_lst[-1])
    return page_number



def extract_urls_from_category(url, category):
    print("Extracting urls from category...")
    category_url = extract_url_from_category(url, category)

    page = requests.get(category_url)

    if page.status_code != 200:
        print(f"Error: {page.status_code}")
        return None

    soup = BeautifulSoup(page.content, 'html.parser')

    page_number = get_page_number(soup)

    current_page = 1

    all_products_relative_urls = []

    while current_page <= page_number :

        page = requests.get(category_url)

        if page.status_code != 200:
            print(f"Error: {page.status_code}")
            return None

        soup = BeautifulSoup(page.content, 'html.parser')

        all_articles = soup.find_all('article', class_='product_pod')

        for article in all_articles:
            article_href = article.find('a').get('href')

            all_products_relative_urls.append(article_href)

        current_page += 1

        page_suffix = f"page-{current_page}.html"
        base_url = category_url.rsplit('/', 1)[0] + '/'  # remove 'index.html'
        category_url = base_url + page_suffix

        all_products_absolute_urls = []
        for url in all_products_relative_urls:
            url_absolute = url.replace("../../../", "https://books.toscrape.com/catalogue/")

            all_products_absolute_urls.append(url_absolute)

    return all_products_absolute_urls

