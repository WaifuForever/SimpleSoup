from bs4 import BeautifulSoup
import base64
import requests
import re


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

articles_found = 1
number = 0

while articles_found < 61:    
    url = "https://scholar.google.com/scholar?start=%d&q=cnn+fruit+sciencedirect&hl=en&as_sdt=0,5&as_ylo=2019&as_yhi=2022" % number
    number += 10
    search = requests.get(url)
    soup = BeautifulSoup(search.text, "html.parser")
    mydivs = soup.find_all("div", {"class": "gs_r gs_or gs_scl"})



    count = 0
    article_url =""   
    #iterate over each item from the search 
    for div in mydivs:     
        #retrieve data from the paper   
        for item in div.find_all("div", {"class": "gs_ri"}):            
            count+=1
            article_url = item.a["href"]
            if article_url.startswith("https://www.sciencedirect.com/s"):
                print("\n\narticles found %d" % articles_found)
                articles_found += 1
                print("%d - %s" % (count, article_url))
                        
                page = requests.get(article_url, headers=headers)
                page_soup = BeautifulSoup(page.text, "html.parser")
                        
                title = page_soup.find("span", "title-text")
                abstract = page_soup.find("div", "abstract author").find("p")
                date = page_soup.find("div", "text-xs")
                


                print(title.get_text())
                print(abstract.get_text())
                try:
                    print(date.get_text().split(",")[1])
                except:
                    print(date.get_text())
                for author in page_soup.find_all("a", {"class": "author size-m workspace-trigger"}):
                    full_name = ""
                    for name in re.findall('[A-Z][^A-Z]*', author.get_text()):
                        full_name += name + " "
                    print(full_name)
            else: 
                print("is not from sciencedirect")
    '''
        for author in div.find_all("div", {"class": "gs_a"}):
            print(author.get_text())

    '''
