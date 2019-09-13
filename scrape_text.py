from bs4 import BeautifulSoup
import requests

gutenberg = 'https://www.gutenberg.org/browse/scores/top'

page_response = requests.get(gutenberg, timeout=5)

page_content = BeautifulSoup(page_response.content, "html.parser")

i = 0
for line in list(page_content.find("div", class_="body").children)[11]:
    if line != '':
        print(i, line)
        i+=1