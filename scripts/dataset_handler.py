from gutenberg.acquire import load_etext
from gutenberg.cleanup import strip_headers
from bs4 import BeautifulSoup
import requests
import re


def get_html(page):
    r = requests.get(page.replace("\n", ""))
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup

def get_improved_edition(ebook_number):

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
    print("Saving File")
    with open(filename + '.txt', 'w') as f:
        f.write(text)

ebook_numbers = get_popular_books("https://www.gutenberg.org/browse/scores/top")
print(f"Getting {len(ebook_numbers)} ebooks")
print(ebook_numbers)
texts = []
for ebook in ebook_numbers[30:]:

    try:
        print(ebook)
        text = strip_headers(load_etext(ebook)).strip()
        save_txt(str(ebook), text[1000:4000])
    except ValueError:
        improved_ebook = get_improved_edition(ebook)
        print(improved_ebook)
        try:
            text = strip_headers(load_etext(improved_ebook)).strip()
            save_txt(str(improved_ebook), text[1000:4000])
            print("Improved edition")
        except ValueError:
            print("Ebook does not exists")


exit()
texts = []
for ebook in ebook_numbers:

    text = strip_headers(load_etext(ebook)).strip()

    print(len(text))
    texts.append(text[1000:])

print(texts)