from bs4 import BeautifulSoup
import requests
import re


gutenberg = 'https://www.gutenberg.org/browse/scores/top'

page_response = requests.get(gutenberg, timeout=5)

page_content = BeautifulSoup(page_response.content, "html.parser")

urls = []
for line in list(page_content.find("div", class_="body").children)[11]:
    line = line.find("a")
    if line != -1:
        urls.append(line.attrs["href"])

for url in urls:
    book_url = "https://www.gutenberg.org"+url
    book_page = requests.get(book_url, timeout=5)
    book_soup = BeautifulSoup(book_page.content, "html.parser")
    text_link = book_soup.find("a", type="text/plain")

    if not text_link:
        text_link = book_soup.find("a", type="text/plain; charset=utf-8")

    text_link = "https://www.gutenberg.org"+text_link.attrs["href"]

    print(text_link)

    with open("data/gutenberg.txt", "a") as file:
        text_page = requests.get(text_link, timeout=5)
        text = re.findall(r"GUTENBERG EBOOK.*PROJECT GUTENBERG",
                           text_page.text, re.DOTALL)[0]
        text = re.sub(r'[^\x00-\x7f]',r'',text)
        file.write(text)
