"""
Coded by Ibrahim Enes Duran
06 June 2021 
"""

import requests #TR Web sitelerindeki verileri GET metoduyla çeker | EN Gets data from websites with GET method
from bs4 import BeautifulSoup as bs #TR Çektiği web sitelerindeki verileri ayrıştırır | EN Parses data from websites it pulls
import json #TR Çekilen verilerin JSON formatında kaydedilmesini sağlar | EN Allows the captured data to be saved in JSON format
import pandas as pd
from progress.bar import ChargingBar

def getBachelorDegree(Data):
    
    """
    TR | Bu fonksiyon YÖK Atlas sitesindeki üniversitelerin lisans bölümleri olanları çeker.
    EN | This function attracts those with undergraduate departments of universities on the YOK Atlas website.
    """
    r = requests.get('https://yokatlas.yok.gov.tr/lisans-anasayfa.php')
    
    soup = bs(r.content, "lxml", from_encoding='UTF-8')
    univs = soup.find("select").find_all("option")
    
    universitiesCode = []
    
    for univ in univs:
        uuid = univ.get('value')
        universitiesCode.append(uuid)
        
    bar = ChargingBar('Getting Bachelor Degrees', max=len(universitiesCode), suffix = '%(percent).1f%% - %(eta)ds')
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
            
        bar.next()
        Data[university] = tempData
    
    bar.finish()

def getAssociateDegree(Data):
    
    """
    TR | Bu fonksiyon YÖK Atlas sitesindeki üniversitelerin önlisans bölümleri olanları çeker.
    EN | This function attracts those who have associate degree departments of universities on the YOK Atlas website.
    """
    
    r = requests.get('https://yokatlas.yok.gov.tr/onlisans-anasayfa.php')
    
    soup = bs(r.content, "lxml", from_encoding='UTF-8')
    univs = soup.find("select").find_all("option")
    
    universitiesCode = []
    
    for univ in univs:
        uuid = univ.get('value')
        universitiesCode.append(uuid)
    
    bar = ChargingBar('Getting Associate Degrees', max=len(universitiesCode), suffix = '%(percent).1f%% - %(eta)ds')
    for uuid in universitiesCode:
        url = 'https://yokatlas.yok.gov.tr/onlisans-univ.php?u=' + str(uuid)
        r = requests.get(url)
        soup = bs(r.content, "lxml", from_encoding='UTF-8')
        university = soup.find("div", attrs={"class": "page-header"}).find('h1').text.split("'ndeki Tüm Önlisans Programları  (Alfabetik Sırada)")[0]
        if(len(university) == 0):
            continue
        sections = soup.findAll("div", attrs={"class": "panel panel-danger"})
        
        json, tempData = {}, []
        for section in sections:
            link = "https://yokatlas.yok.gov.tr/" + section.find('a').get('href')
            name = section.find("div", attrs={"style": "overflow: hidden; text-overflow: ellipsis; white-space: nowrap;width:80%"}).text
            department = section.find('small').text
            examType = section.find("button").text
            json = {"name": name, "department": department, "examType": examType, "link": link}
            tempData.append(json)
            
        bar.next()
        Data[university] = tempData
        
    bar.finish()

BachelorDegree, AssociateDegree = {}, {}

getBachelorDegree(BachelorDegree)
getAssociateDegree(AssociateDegree)

Data = {"BachelorDegree" : BachelorDegree,
        "AssociateDegree" : AssociateDegree}

with open('universities.json', 'w', encoding='utf-8') as f:
    json.dump(Data, f, ensure_ascii=False, indent=4)
    
"""  

yokAtlas_links = {
  "main_info" : "1000_1.php?y=",
  "quota_placement_statistics" : "1000_2.php?y=",
  "gender_distribution_of_students" : "1010.php?y=",
  "geographic_places_where_students_come_from": "1020ab.php?y=",
  "provinces_of_students": "1020c.php?y=",
  "educational_status_of_students": "1030a.php?y=",
  "high_school_graduation_years_of_students": "1030b.php?y=",
  "high_school_fields_of_students": "1050b.php?y=",
  "high_school_types_of_students": "1050a.php?y=",
  "high_schools_from_which_students_graduated": "1060.php?y=",
  "students_school_firsts": "1030c.php?y=",
  "base_score_and_achievement_statistics": "1000_3.php?y=",
  "last_placed_student_profile": "1070.php?y=",
  "YKS_net_averages_of_students": "1210a.php?y=",
  "students_YKS_scores": "1220.php?y=",
  "YKS_success_order_of_students": "1230.php?y=",
  "preference_statistics_across_the_country": "1080.php?y=",
  "in_which_preferences_students_settled": "1040.php?y=",
  "preference_tendency_general": "1300.php?y=",
  "preference_tendency_university_type": "1310.php?y=",
  "preference_tendency_universities": "1320.php?y=",
  "preference_tendency_provinces": "1330.php?y=",
  "preference_tendency_same_programs": "1340a.php?y=",
  "preference_tendency_programs": "1340b.php?y=",
  "conditions": "1110.php?y="
  }

B = {}
data = {}
code = "102210277"
for j in yokAtlas_links:

    table_main_info = pd.read_html('https://yokatlas.yok.gov.tr/content/lisans-dynamic/{}{}'.format(yokAtlas_links[j], code))
    parsed = {}
    
    for x in table_main_info:
        if j not in ["students_school_firsts", "in_which_preferences_students_settled"]:
            x = x.set_index(x.columns[0])
        x = x.to_json(force_ascii = False, orient="index")
        parsed.update(json.loads(x))
            
    B[j] = parsed
    
with open('{}.json'.format(code), 'w', encoding='utf-8') as f:
    json.dump(B, f, ensure_ascii=False, indent=4)
    
#print(json.dumps(B, indent = 4, ensure_ascii=False))
   """     

