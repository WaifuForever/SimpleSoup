from bs4 import BeautifulSoup
import requests
import re

class ScienceDirect:
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
    workbook = ""
    worksheet = ""

    def __init__(self, workbook, worksheet):
        self.workbook = workbook
        self.worksheet = worksheet       
        pass

    def extract(self, div, articles_found):   
        
        for item in div.find_all("div", {"class": "gs_ri"}):            
                
                article_url = item.a["href"]
                if article_url.startswith("https://www.sciencedirect.com/s"):
                    print("\n\narticles found %d" % articles_found)
                    articles_found += 1
                    print("%s" % (article_url))
                            
                    page = requests.get(article_url, headers=self.headers)
                    page_soup = BeautifulSoup(page.text, "html.parser")
                            
                    title = page_soup.find("span", "title-text")
                    abstract = page_soup.find("div", "abstract author").find("p")
                    date = page_soup.find("div", "text-xs")
                    
                    data = [title.get_text(), abstract.get_text()]
                
                    try:
                        data.append(date.get_text().split(",")[1])
                        
                    except:
                        data.append(date.get_text())
                    authors_name = ""
                    count = 0
                    for author in page_soup.find_all("a", {"class": "author size-m workspace-trigger"}):
                        full_name = ""
                        for name in re.findall('[A-Z][^A-Z]*', author.get_text()):
                            full_name += name + " "
                        
                        if count == 0:
                            authors_name += full_name
                        else:
                            authors_name += ", " + full_name

                    data.append(authors_name)
                    self.write_xls(data, row = articles_found)
                else: 
                    print("is not from sciencedirect")
            
        return articles_found

    def write_xls(self, data, row):
    
        col = 0
        cell_format = self.workbook.add_format()
        cell_format.set_text_wrap()

        
        self.worksheet.write(row, col, data[0])
        self.worksheet.write(row, col + 1, data[1], cell_format)
        self.worksheet.write(row, col + 2, data[2])
        self.worksheet.write(row, col + 3, data[3])
        
