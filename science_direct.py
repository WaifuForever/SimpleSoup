from bs4 import BeautifulSoup
import requests
import re

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

def extract(div, articles_found):   
    
    for item in div.find_all("div", {"class": "gs_ri"}):            
            
            article_url = item.a["href"]
            if article_url.startswith("https://www.sciencedirect.com/s"):
                print("\n\narticles found %d" % articles_found)
                articles_found += 1
                print("%s" % (article_url))
                        
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
           
    return articles_found