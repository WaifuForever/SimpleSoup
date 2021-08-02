from bs4 import BeautifulSoup
import base64
import requests
import re

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

url = "https://scholar.google.com/scholar?q=cnn+fruit+sciencedirect&hl=en&as_sdt=0%2C5&as_ylo=2019&as_yhi=2022"

search = requests.get(url)

soup = BeautifulSoup(search.text, "html.parser")

mydivs = soup.find_all("div", {"class": "gs_r gs_or gs_scl"})



count = 0
article_url =""
for div in mydivs:
    print("\n\n %d" % count)
    count+=1
    for item in div.find_all("div", {"class": "gs_ri"}):
        article_url = item.a["href"]
        print(article_url)
                
        page = requests.get(article_url, headers=headers)
        page_soup = BeautifulSoup(page.text, "html.parser")
                
        title = page_soup.find("span", "title-text")
        abstract = page_soup.find("div", "abstract author").find("p")
        date = page_soup.find("div", "text-xs")
        


        print(title.get_text())
        print(abstract.get_text())
        print(date.get_text().split(",")[1])

        for author in page_soup.find_all("a", {"class": "author size-m workspace-trigger"}):
            full_name = ""
            for name in re.findall('[A-Z][^A-Z]*', author.get_text()):
                full_name += name + " "
            print(full_name)
'''
    for author in div.find_all("div", {"class": "gs_a"}):
        print(author.get_text())

'''
