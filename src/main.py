import requests
from bs4 import BeautifulSoup as bs
import timeit

r = requests.get('https://yokatlas.yok.gov.tr/lisans-anasayfa.php')

soup = bs(r.content, "lxml", from_encoding='UTF-8')
univs = soup.find("select").find_all("option")
universitiesCode = []

for univ in univs:
    uuid = univ.get('value')
    universitiesCode.append(uuid)

Data= {}
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

