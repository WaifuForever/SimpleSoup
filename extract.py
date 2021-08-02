import requests
import re
from bs4 import BeautifulSoup


class Extract:
    
    articles_found = 1
    total = 0
    limit = 61

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
    workbook = ""
    worksheet = ""

    def __init__(self, workbook, worksheet):
        self.workbook = workbook
        self.worksheet = worksheet       
        pass

    def search(self, db):
        number = 0
        
        while self.articles_found < self.limit:
            url = "https://scholar.google.com/scholar?start=%d&q=cnn+fruit+%s&hl=en&as_sdt=0,5&as_ylo=2019&as_yhi=2022" % (number, db)
            number += 10
            search = requests.get(url, headers = self.headers)
            soup = BeautifulSoup(search.text, "html.parser")                   
            mydivs = soup.find_all("div", {"class": "gs_r gs_or gs_scl"})
           
            #iterate over each item from the search 
            for div in mydivs: 
              
                #retrieve data from the paper - 10 per time 
                #self.articles_found = sc.extract(div, self.articles_found)   
                self.__extract(div, db) 

        self.total += self.articles_found
        self.articles_found = 0
        print("total: %d" % self.total)

    def __extract (self, page, db):
        if db == "sciencedirect":
            self.__science_direct(page)
        else :
            self.__arxiv(page)
        
                   

    def __write_xls(self, data):
        
            col = 0
            cell_format = self.workbook.add_format()
            cell_format.set_text_wrap()
            header_format = self.workbook.add_format({'text_wrap': True, 'valign': 'top'})
            
            self.worksheet.write(self.articles_found, col, data[0], header_format)
            self.worksheet.write(self.articles_found, col + 1, data[1], header_format)
            self.worksheet.write(self.articles_found, col + 2, data[2], header_format)
            self.worksheet.write(self.articles_found, col + 3, data[3], header_format)
            

    def __arxiv(self, div):               
            for item in div.find_all("div", {"class": "gs_ri"}):          
            
                    article_url = item.a["href"]
                    if article_url.startswith("https://arxiv.org/"):
                        print("\narticles found %d" % self.articles_found)
                        self.articles_found += 1
                        print("%s" % (article_url))
                                
                        page = requests.get(article_url, headers=self.headers)
                        page_soup = BeautifulSoup(page.text, "html.parser")
                                
                        title = page_soup.find("h1", "title mathjax")
                        abstract = page_soup.find("blockquote", "abstract mathjax")
                        date = page_soup.find("div", "dateline")
                        
                        title = title.get_text()[6:]
                        abstract = abstract.get_text()[12:]                        
                        date = date.get_text()

                        if "," in date:                           
                            date = date.split(",")[0]
                            date = date[-15: -5]
                            
                        else:
                            date = date
                            date = date[-12: -1]
                        

                       

                        print(title)
                        print(abstract)
                        print(date)

                       
                        '''
                        try:
                            data.append(date.split(",")[1])
                            
                        except:
                            data.append(date.get_text())
                        '''
                        authors_name = ""
                        count = 0
                        for author in page_soup.find("div", "authors").find_all("a"):
                            full_name = author.get_text()
                                                       
                            if count == 0:
                                authors_name += full_name
                            else:
                                authors_name += ", " + full_name

                                                    
                        print(authors_name)
                        data = [title, abstract, date, authors_name, "arxiv"]
                          
                        self.__write_xls(data)
                    #else: 
                        #print("\n\nis not from arxiv")
               
            
    def __science_direct(self, div):        
        for item in div.find_all("div", {"class": "gs_ri"}):            
                
                article_url = item.a["href"]
                if article_url.startswith("https://www.sciencedirect.com/s"):
                    print("\n\narticles found %d" % self.articles_found)
                    self.articles_found += 1
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
                    data.append("science_direct")
                    self.__write_xls(data)
                #else: 
                #    print("is not from sciencedirect")
           
        