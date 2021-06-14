"""
Coded by Ibrahim Enes Duran
06 June 2021 
"""
import requests #TR Web sitelerindeki verileri GET metoduyla çeker | EN Gets data from websites with GET method
from bs4 import BeautifulSoup as bs #TR Çektiği web sitelerindeki verileri ayrıştırır | EN Parses data from websites it pulls
import json #TR Çekilen verilerin JSON formatında kaydedilmesini sağlar | EN Allows the captured data to be saved in JSON format
import pandas as pd
from progress.bar import ChargingBar
import time

yokAtlas_links = {
    "bachelor_Degree": {
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

}

def getBachelorDegree(Data):
    
    """
    TR | Bu fonksiyon YÖK Atlas sitesindeki üniversitelerin lisans bölümleri olanları çeker.
    EN | This function attracts those with undergraduate departments of universities on the YOK Atlas website.
    """

    print("Starting! Getting bachelor degrees")

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

    print("Starting! Getting associate degrees")

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

def getDetailsFromWeb(Data, Universities):
    if(len(Universities["BachelorDegree"]) == 0 and len(Universities["AssociateDegree"]) == 0):
        return print("Error! Not found degrees")
    
    if(len(Universities["BachelorDegree"]) > 0):
        print("Starting! Getting bachelor degree details from yokatlas.yok.gov.tr")
        maxBach = 0
        for i in Universities["BachelorDegree"]:
            for section in Universities["BachelorDegree"][i]:
                maxBach = maxBach + 1
        bar = ChargingBar('Getting Bachelor Degrees details', max= maxBach * len(yokAtlas_links["bachelor_Degree"]), suffix = '%(percent).1f%% - %(eta)ds')
        BachelorDegree = {}
        for i in Universities["BachelorDegree"]:
            BachelorDegree[i] = {}
            for section in Universities["BachelorDegree"][i]:
                BachelorDegree[i][section["name"]] = {}
                code = section["link"].split("https://yokatlas.yok.gov.tr/lisans.php?y=")[1]

                for j in yokAtlas_links["bachelor_Degree"]:

                    table_main_info = pd.read_html('https://yokatlas.yok.gov.tr/content/lisans-dynamic/{}{}'.format(yokAtlas_links["bachelor_Degree"][j], code))
                    parsed = {}
                   
                    for x in table_main_info:
                        try:
                            if j not in ["students_school_firsts", "in_which_preferences_students_settled"]:
                                x = x.set_index(x.columns[0])
                            x = x.to_json(force_ascii = False, orient="index")
                            parsed.update(json.loads(x))
                        except:
                            print(x)
                            continue
                        
                    bar.next()
                    BachelorDegree[i][section["name"]][j] = parsed
                    
            
                    
           
        Data["BachelorDegree"] = BachelorDegree
        bar.finish()




print("Hey person! Welcome the Yok Atlas crawler.")
print("This program will help you to get Turkish Universities Statistics and save with Json format.")
inputs = {}
while(True):
    inputs[0] = input("Do you have universities.json? Y [Yes] N [No]: ")

    if(inputs[0].upper() == "N"):
        BachelorDegree, AssociateDegree = {}, {}

        while(True):
            inputs[1] = input("Do you want to get bachelor degrees? Y [Yes] N [No]:")
            inputs[2] = input("Do you want to get associate degrees? Y [Yes] N [No]:")

            if(inputs[1].upper() == "Y" and inputs[2].upper() == "Y"):
                getBachelorDegree(BachelorDegree)
                getAssociateDegree(AssociateDegree)
                inputs[3] = "bachelor degrees and associate degrees"
                break
            elif(inputs[1].upper() == "Y" and inputs[2].upper() == "N"):
                getBachelorDegree(BachelorDegree)
                inputs[3] = "bachelor degrees"
                break
            elif(inputs[1].upper() == "N" and inputs[2].upper() == "Y"):
                getAssociateDegree(AssociateDegree)
                inputs[3] = "associate degrees"
                break
            else:
                print("Error! Undefined input")

        Data = {"BachelorDegree" : BachelorDegree,
                "AssociateDegree" : AssociateDegree}

        with open('universities.json', 'w', encoding='utf-8') as f:
            json.dump(Data, f, ensure_ascii=False, indent=4)
            print("Completed! Succesfully {} was getted. Saved universities.json".format(inputs[3]))
            break
        
    elif(inputs[0].upper() == "Y"):
        with open('universities.json', 'r', encoding='utf-8') as f:
            try:
                universities = json.load(f)
                print("Succesful! {} bachelor degrees and {} associate degrees loaded from file.".format(len(universities["BachelorDegree"]), len(universities["AssociateDegree"])))
            except Exception as e:
                print("Error! Json file loading failed")
                print(e)
                break
            try:
                Data = {}
                getDetailsFromWeb(Data, universities)
                filename = int(time.time())
                with open('{}.json'.format(filename), 'w', encoding='utf-8') as f:
                    json.dump(Data, f, ensure_ascii=False, indent=4)
                    print("Completed! Succesfully universities details was getted. Saved {}.json".format(filename))
                    break
            except Exception as e:
                print("Error! Get details failed")
                print(e)
                break
            break
    else:
        print("Error! Undefined input")




