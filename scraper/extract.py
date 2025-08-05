import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

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
    print(f"  ▷▷ {title} \n")
    all_datas['title'] = title


    # Extraction of product category
    breadcrumb = soup.select_one("ul.breadcrumb")
    if breadcrumb:
        a_list = breadcrumb.find_all("a")
        category_links = [
            a.get_text(strip=True)
            for a in a_list
            if a.string and a.string not in ('Home', 'Books')
        ]
        category = category_links[0] if category_links else "Unknown"
    else:
        category = "Unknown"

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


def extract_category_url(url, category):
    """Function that extracts the absolute url of a given category from the given html page

    Args:
        url (string): The html page url
        category (string): The category name

    Returns:The absolute url of the specified category

    """
    page = requests.get(url)

    if page.status_code != 200:
        print(f"Error: {page.status_code}")
        return None

    soup = BeautifulSoup(page.content, 'html.parser')

    # Extraction of urls

    category_links = soup.select("ul.nav.nav-list ul li a")

    for link in category_links:
        category_name = link.text.strip()
        href = link.get("href")

        if category_name.lower() == category.lower():
            return urljoin(url, href)

    raise ValueError(f"Category '{category}' not found.")


def get_page_number(soup):
    """Function that gets the page number of the given soup

    Args:
        soup (BeautifulSoup): The content

    Returns: The number of page of the given soup

    """
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


def get_all_categories(url):
    """ Function that gets all category names from the given url

    Args:
        url (string): The url of the index page

    Returns: The list of all category names

    """
    page = requests.get(url)

    if page.status_code != 200:
        print(f"Error: {page.status_code}")
        return None

    soup = BeautifulSoup(page.content, 'html.parser')

    category_links = soup.select("ul.nav.nav-list ul li a")

    return [link.text.strip() for link in category_links]


def extract_books_urls_from_category(url, category):
    """Function that extracts all the urls (all books pages) in a given category from the given html page

    Args:
        url (string): The html page url
        category (string): The category name

    Returns:The list of urls extracted from the given category

    """

    print("▻ Extracting urls from category...")
    category_url = extract_category_url(url, category)

    page = requests.get(category_url)

    if page.status_code != 200:
        print(f"Error: {page.status_code}")
        return []

    soup = BeautifulSoup(page.content, 'html.parser')

    page_number = get_page_number(soup)

    current_page = 1

    all_books_with_category = []

    while current_page <= page_number :

        page = requests.get(category_url)

        if page.status_code != 200:
            print(f"Error: {page.status_code}")
            return []

        soup = BeautifulSoup(page.content, 'html.parser')

        all_articles = soup.find_all('article', class_='product_pod')

        for article in all_articles:
            article_href = article.find('a').get('href')
            url_absolute = article_href.replace("../../../", "https://books.toscrape.com/catalogue/")
            all_books_with_category.append((url_absolute, category))

        current_page += 1
        page_suffix = f"page-{current_page}.html"
        base_url = category_url.rsplit('/', 1)[0] + '/'  # remove 'index.html'
        category_url = base_url + page_suffix


    return all_books_with_category