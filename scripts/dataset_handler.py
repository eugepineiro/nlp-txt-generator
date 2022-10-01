from gutenberg.acquire import load_etext
from gutenberg.cleanup import strip_headers
from bs4 import BeautifulSoup
import requests
import re


def get_html(page):
    """
    Requests HTML for web scraping the page

    :param page: url for web scraper
    :return: Soup HTML parser
    """
    r = requests.get(page.replace("\n", ""))
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup

def get_improved_edition(ebook_number):
    """
    When ebook is deprecated must get improved edition

    :param ebook_number: deprecated ebook number
    :return: new ebook number
    """

    page = 'https://www.gutenberg.org/ebooks/' + str(ebook_number)
    r = requests.get(page.replace("\n", ""))
    soup = BeautifulSoup(r.content, 'html.parser')
    td = soup.find_all('a')
    url = '/ebooks/'
    ebook_regex = re.compile(url + '[0-9]+$')

    for link in td:
        link_str = str(link.get('href'))
        if ebook_regex.match(link_str):
            print(link_str)
            ebook_number = int(link_str[(len(url)):])
            return ebook_number

def get_popular_books(page):
    """
    Web scraping for popular books from Gutenberg page
    :param page: url for web scrapping
    :return: ebook numbers
    """

    soup = get_html(page)  # Download HTML

    atags = soup.find_all('a')                   # Get all tags <a href=/ebooks/number></a>
    tags = [tag.get('href') for tag in atags]    # Tag = /ebooks/number

    url = '/ebooks/'
    ebook_regex = re.compile(url + '[0-9]+')     # Get every ebook number, only digits and can be repeated

    ebook_numbers = []
    for link in tags:
        if ebook_regex.match(link):              # Verify the link matches the pattern
            ebook_numbers.append(int(link[(len(url)):])) # Just get numbers from ebooks

    return ebook_numbers

def save_txt(filename, text):
    """
    Saves text to file.txt

    :param filename: save to filename.txt
    :param text: text to save
    :return: void
    """
    with open(filename + '.txt', 'w') as f:
        f.write(text)

def build_popular_books_corpus(text_start=0, text_end=-1):
    """
    Generates top Gutenberg books corpus with web scraping

    :param text_start: Save text from text_start
    :param text_end: Save text until text_end. If text_end = -1 saves whole book from text_start
    :return: void, saves to file.txt
    """

    print("Building POPULAR corpus")
    url = "https://www.gutenberg.org/browse/scores/top"
    ebook_numbers = get_popular_books(url)
    print(f"Scraping from: {url}")
    print(f"Trying to get {len(ebook_numbers)} ebooks\nEbook Numbers:\n{ebook_numbers}")

    for ebook in ebook_numbers:

        try:
            text = strip_headers(load_etext(ebook)).strip()
            if text_end == -1:
                text = text[text_start:]
            else:
                text = text[text_start:text_end]
            save_txt(str(ebook), text)
            print(f"Ebook {ebook} successfully saved")

        except ValueError:
            improved_ebook = get_improved_edition(ebook)
            try:
                text = strip_headers(load_etext(improved_ebook)).strip()
                if text_end == -1:
                    text = text[text_start:]
                else:
                    text = text[text_start:text_end]
                save_txt(str(improved_ebook), text)
                if improved_ebook is not None:
                    print(f"Improved ebook {improved_ebook} successfully saved")

            except ValueError:
                print(f"Ebook {ebook} is not supported anymore")


def build_specific_corpus(query, paging=-1, text_start=0, text_end=-1):
    print(f"Building {query} corpus")
    """
    Generates Gutenberg books corpus about specific topic

    :param query: specific topic. ex: vampire
    :param paging: get paginated ebooks from page: paging. If paging = -1 gets first page
    :param text_start: Save text from text_start
    :param text_end: Save text until text_end . If text_end = -1 saves whole book from text_start
    :return:
    """
    BOOKS_PER_PAGE = 25

    url = f"https://www.gutenberg.org/ebooks/search/?query={query}&submit_search=Go%21"
    if paging != -1:
        url += f"&start_index={BOOKS_PER_PAGE*paging+1}"
    print(f"Scraping from: {url}")

    ebook_numbers = get_popular_books(url)

    for ebook in ebook_numbers:

        try:
            text = strip_headers(load_etext(ebook)).strip()
            if text_end == -1:
                text = text[text_start:]
            else:
                text = text[text_start:text_end]
            save_txt(str(ebook), text)
            print(f"Ebook {ebook} successfully saved")

        except ValueError:
            print(f"Ebook {ebook} is not supported anymore")
