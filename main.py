from bs4 import BeautifulSoup
import base64
import requests
from science_direct import *



articles_found = 1
number = 0

while articles_found < 11:    
    url = "https://scholar.google.com/scholar?start=%d&q=cnn+fruit+sciencedirect&hl=en&as_sdt=0,5&as_ylo=2019&as_yhi=2022" % number
    number += 10
    search = requests.get(url)
    soup = BeautifulSoup(search.text, "html.parser")
    mydivs = soup.find_all("div", {"class": "gs_r gs_or gs_scl"})

 
    #iterate over each item from the search 
    for div in mydivs: 

        #retrieve data from the paper - 10 per time 
        articles_found = extract(div, articles_found)   
        
   
   