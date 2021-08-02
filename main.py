import requests
import xlsxwriter
from science_direct import ScienceDirect
from bs4 import BeautifulSoup

workbook = xlsxwriter.Workbook('Articles.xlsx')
worksheet = workbook.add_worksheet()

articles_found = 1
number = 0
 
worksheet.write(0, 0, "Title")
worksheet.write(0, 1, "Abstract")
worksheet.write(0, 2, "Date")
worksheet.write(0, 3, "Authors")

sc = ScienceDirect(workbook, worksheet)
while articles_found < 11:    
    url = "https://scholar.google.com/scholar?start=%d&q=cnn+fruit+sciencedirect&hl=en&as_sdt=0,5&as_ylo=2019&as_yhi=2022" % number
    number += 10
    search = requests.get(url)
    soup = BeautifulSoup(search.text, "html.parser")
    mydivs = soup.find_all("div", {"class": "gs_r gs_or gs_scl"})

 
    #iterate over each item from the search 
    for div in mydivs: 

        #retrieve data from the paper - 10 per time 
        articles_found = sc.extract(div, articles_found)   
        
   
workbook.close()