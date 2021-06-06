"""
Coded by Ibrahim Enes Duran
06 June 2021 
"""
import requests #TR Web sitelerindeki verileri GET metoduyla çeker | EN Gets data from websites with GET method
from bs4 import BeautifulSoup as bs #TR Çektiği web sitelerindeki verileri ayrıştırır | EN Parses data from websites it pulls
import json #TR Çekilen verilerin JSON formatında kaydedilmesini sağlar | EN Allows the captured data to be saved in JSON format

def getBachelorDegree(Data):
    """
    TR | Bu fonksiyon YOK Atlas sitesindeki üniversitelerin lisans bölümleri olanları çeker.
    EN | This function attracts those with undergraduate departments of universities on the YOK Atlas website.
    """
    
    r = requests.get('https://yokatlas.yok.gov.tr/lisans-anasayfa.php')
    
    soup = bs(r.content, "lxml", from_encoding='UTF-8')
    univs = soup.find("select").find_all("option")
    
    universitiesCode = []
    
    for univ in univs:
        uuid = univ.get('value')
        universitiesCode.append(uuid)
    
    for uuid in universitiesCode:
        url = 'https://yokatlas.yok.gov.tr/lisans-univ.php?u=' + str(uuid)
        r = requests.get(url)
        soup = bs(r.content, "lxml", from_encoding='UTF-8')
        university = soup.find("div", attrs={"class": "page-header"}).find('h1').text.split("'ndeki Tüm Lisans Programları  (Alfabetik Sırada)")[0]
        if(len(university) == 0):
            continue
        sections = soup.findAll("div", attrs={"class": "panel panel-primary"})
        
        json, tempData = {}, []
        for section in sections:
            link = "https://yokatlas.yok.gov.tr/" + section.find('a').get('href')
            name = section.find("div", attrs={"style": "overflow: hidden; text-overflow: ellipsis; white-space: nowrap;width:80%"}).text
            department = section.find('small').text
            examType = section.find("button").text
            json = {"name": name, "department": department, "examType": examType, "link": link}
            tempData.append(json)
            
        Data[university] = tempData
    

Data = {}

getBachelorDegree(Data)

with open('universitiesBachelorDegree.json', 'w', encoding='utf-8') as f:
    json.dump(Data, f, ensure_ascii=False, indent=4)
    
    
    
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from unicodedata import normalize

table_main_info = pd.read_html('https://yokatlas.yok.gov.tr/content/lisans-dynamic/1000_1.php?y=106510077')
table_main_info = pd.read_html('https://yokatlas.yok.gov.tr/content/lisans-dynamic/1000_1.php?y=106510077')"""


