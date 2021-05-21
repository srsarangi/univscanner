import requests
import urllib.request
import time
import urllib
import re
import csv
import sys
from bs4 import BeautifulSoup

def mit():
    url = "https://www.eecs.mit.edu/people/faculty-advisors"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "MIT"
    country = "USA"
    grabage_emails = ['news@csail.mit.edu']
    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    d = soup.find_all('div', {'class':"views-field views-field-title"})
    # count = 0 
    # iterating for every prof
    for i in d:
        a = i.find('a')                     # a contains the name and the homepage of prof
        if a == None:
            continue
        link = a.get('href')                # extracting prof page link
        name = a.get_text()                 # extracting prof name
        try:
            prof_resp = requests.get(link)      # requesting prof homepgae
        except:
            continue
        email = "Not Found"

        print(u_name, name, link)
        filterandgetEmail2(var, grabage_emails, name, link, email, prof_resp)

    file.close()
    print("=====", u_name, "Finished =====")
# ================================

def stanford():
    url = "https://cs.stanford.edu/directory/faculty"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Stanford"
    country = "USA"

    grabage_emails = []
    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    d = soup.find_all('tr', {'class':["odd", "even"]})
    # count = 0 
    # iterating for every prof
    for i in d:
        a = i.find('a')                     # a contains the name and the homepage of prof
        if a == None:
            continue
        link = a.get('href')                # extracting prof page link
        name = a.get_text()                 # extracting prof name
        try:
            prof_resp = requests.get(link)      # requesting prof homepgae
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()
    print("=====", u_name, "Finished =====")
# ====================================

def harvard():
    url = "https://www.seas.harvard.edu/computer-science/faculty-research"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Harvard"
    country = "USA"

    grabage_emails = ['santana@seas.harvard.edu', 'gioia@seas.harvard.edu', 'jsalant@harvard.edu', 'jbourge@seas.harvard.edu']
    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    
    d = soup.find('a', text="Computer Architecture").find_next('div')
    dd = d.find_all('div', {'class': 'views-field views-field-title'})

    #iterating for every prof
    for i in dd:
        if i.find('a') == None:
            continue        
        a = i.find('a')                     # a contains the name and the homepage of prof
        link = "https://www.seas.harvard.edu"+ a.get('href')                # extracting prof page link
        name = a.get_text()                 # extracting prof name

        # check if link is valid on not
        try:    
            prof_resp = requests.get(link)        
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        OnlygetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()
    print("=====", u_name, "Finished =====")
# ================================

def caltech():
    url = "https://cms.caltech.edu/people"
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Caltech"
    country = "USA"

    grabage_emails = []
    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    d = soup.find_all('strong', {'class':'name'})
    
    #iterating for every prof
    for i in d:
        a = i.find('a')                     # a contains the name and the homepage of prof
        # print(a.get('href'))
        link = "https://cms.caltech.edu" + a.get('href')                # extracting prof page link
        # print(link)
        name = a.get_text()                 # extracting prof name
        try:
            prof_resp = requests.get(link)      # requesting prof homepgae
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()
    print("=====", u_name, "Finished =====")

# =======================================

def oxford():
    url = "http://www.cs.ox.ac.uk/people/faculty.html"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Oxford"
    country = "UK"

    grabage_emails = ['finance@cs.ox.ac.uk', 'enquiries@cs.ox.ac.uk']

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    d = soup.find_all('li', {'class':'personIndex'})
    # dd = d.find_all('div', {'class': 'views-field views-field-title'})

    #iterating for every prof
    for i in d:
        a = i.find('a')                     # a contains the name and the homepage of prof
        link = "http://www.cs.ox.ac.uk" + a.get('href')                # extracting prof page link
        name = a.get_text()                 # extracting prof name
        # print(name, "\t", link)
        name = name.strip()

        try:    
            prof_resp = requests.get(link)        
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ================================

def cambridge():
    url = "https://www.cst.cam.ac.uk/research/themes/computer-architecture"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of Cambridge"
    country = "England"

    grabage_emails = ['pagemaster@cst.cam.ac.uk']

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'id':"block-views-research-theme-faces-block"})
    d = dd.find_all('div', {'class':"cst-title-with-padding"})
    # print(d)  

    #iterating for every prof
    for i in d:
        # print(i)
        a = i.find('a')                     # a contains the name and the homepage of prof
        link = 'https://www.cst.cam.ac.uk' + a.get('href')
        name = (a.get_text()).strip()                 # extracting prof name
        # name = name.replace("\t", "")
        # name = name.replace("\n", "")
        
        try:
            prof_resp = requests.get(link)          # requesting prof homepgae
        except:
            continue
        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def imperial_college():
    url = "https://www.imperial.ac.uk/computing/people/academic-staff/"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Imperial College, London"
    country = "UK"

    grabage_emails = []
    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    d = soup.find_all('div', {'class':'name-wrapper'})
    # dd = d.find_all('div', {'class': 'views-field views-field-title'})

    #iterating for every prof
    for i in d:
        a = i.find('a', {'class':'name-link'})

        if a == None:
            continue
        a = i.find('a', {'class':'name-link'})                     # a contains the name and the homepage of prof
        link = a.get('href')                # extracting prof page link
        name = a.get_text()                 # extracting prof name

        try:    
            prof_resp = requests.get(link)        
        except:
            continue
        
        a_mail = i.find('a', {'class':'email'})
        if a_mail != None:
            email = a_mail.get('href')
            email = email[7:]
        else:
            email = "Not Found"

        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uchicago():
    url = "https://www.cs.uchicago.edu/people/faculty/"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of Chicago"
    country = "USA"

    grabage_emails = ['cswebmaster@cs.uchicago.edu']
    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    d = soup.find_all('div', {'class':'people_content'})

    #iterating for every prof
    for i in d:
        a = i.find('a')                     # a contains the name and the homepage of prof
        link = a.get('href')                # extracting prof page link
        name = a.get_text()                 # extracting prof name
        name = name.strip()
        # name = name.replace("\t", '')
        # name = name.replace("\n", " ")

        try:    
            prof_resp = requests.get(link)        
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def ucl_london():
    url = "https://www.ucl.ac.uk/computer-science/people/computer-science-academic-staff"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University College London"
    country = "UK"

    grabage_emails = ['portico-services@ucl.ac.uk']
    var = [csvwriter, u_name, country]


    # d gives the array of all profs on the dept homepage
    d = soup.find_all('article', {'class':'article'})
    # print(d)

    #iterating for every prof
    for i in d:
        a = i.find_all('a')                     # a contains the name and the homepage of prof
        for j in a:
            link = j.get('href')                # extracting prof page link
            if link == None:
                continue
            elif link[0] == '#' or link[0:6] == 'mailto':
                continue
            name = j.get_text()                 # extracting prof name
            try:    
                prof_resp = requests.get(link)        
            except:
                continue

            email = "Not Found"
            print(u_name, name, link)
            filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def nus():
    url = "https://www.comp.nus.edu.sg/about/depts/cs/faculty/"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "NUS"
    country = "Singapore"

    grabage_emails = ['socfamily@comp.nus.edu.sg']
    var = [csvwriter, u_name, country]


    # d gives the array of all profs on the dept homepage
    dd = soup.find_all('b')
    d = set(dd)

    #iterating for every prof
    for i in d:
        a = i.find('a') 
        if a == None:
            continue
        a = i.find('a')                     # a contains the name and the homepage of prof
        link = a.get('href')                # extracting prof page link
        name = a.get_text()                 # extracting prof name

        try:    
            prof_resp = requests.get(link)        
        except:
            continue

        # print(u_name, name, link)
        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def princeton():
    url = "https://www.cs.princeton.edu/people/faculty?type=main&research=11"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Princeton"
    country = "USA"

    grabage_emails = []
    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    d = soup.find_all('div', {'class':'person-details'})

    #iterating for every prof
    for i in d:
        a = i.find('a')                     # a contains the name and the homepage of prof
        link = "https://www.cs.princeton.edu" + a.get('href')                # extracting prof page link
        name = a.get_text()                 # extracting prof name
        
        try:    
            prof_resp = requests.get(link)        
        except:
            continue

        # print(u_name, name, link)
        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def ntus():
    url = "https://www3.ntu.edu.sg/SCSE/moss_staffac.asp"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "NTUS"
    country = "Singapore"

    grabage_emails = []
    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    d = soup.find_all('td', {'width':'278', 'align':'left', 'valign':'top'})

    #iterating for every prof
    for i in d:
        a = i.find('a')                     # a contains the name and the homepage of prof
        link =  a.get('href')
        if 'mailto' in link:
            continue
        # print(link)
        prof_resp = requests.get(link)          # requesting prof homepgae
        prof_soup = BeautifulSoup(prof_resp.text, "html.parser") 
        if prof_soup.find('title') != None:
            name = (prof_soup.find('title')).string
        else:
            name = "NAME NOT FOUND"

        # try:    
        #     prof_resp = requests.get(link)        
        # except:
        #     continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def tsinghua():
    url = "http://www.cs.tsinghua.edu.cn/publish/csen/4923/2014/20140108153546275916040/20140108153546275916040_.html"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Tsinghua University"
    country = "China"

    grabage_emails = []
    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    
    dd = soup.find('div', {'class':"box_detail"})
    d = dd.find_all('a')
    # print(d)

    #iterating for every prof
    for i in d:
        # a = i.find('a')                     # a contains the name and the homepage of prof
        link = i.get('href')
        if link[0] == '/':
            link = 'http://www.cs.tsinghua.edu.cn'+link
        name = i.get_text()                 # extracting prof name

        try:
            prof_resp = requests.get(link)          # requesting prof homepgae
            prof_soup = BeautifulSoup(prof_resp.text, "html.parser") 
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_penn():
    url = "https://directory.seas.upenn.edu/computer-and-information-science/"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of Pennsylvania"
    country = "USA"

    grabage_emails = ['mkearns@lehman.com', 'michael.kearns@bofasecurities.com', 'lhoot@seas.upenn.edu', 'kearmic@amazon.com']
    var = [csvwriter, u_name, country, grabage_emails]


    # d gives the array of all profs on the dept homepage
    
    d = soup.find_all('div', {'class':"StaffListName"})
    # print(d)  

    #iterating for every prof
    for i in d:
        a = i.find('a')                     # a contains the name and the homepage of prof
        link = a.get('href')
        name = a.get_text()                 # extracting prof name
        name = name.replace("\t", "")
        name = name.replace("\n", "")
        try:
            prof_resp = requests.get(link)          # requesting prof homepgae
            prof_soup = BeautifulSoup(prof_resp.text, "html.parser") 
        except:
            continue

        # print(u_name, name, link)
        pp = prof_soup.find('a', text='Personal Website')
        # print(pp)
        if pp == None:
            continue
        link2 = pp.get('href')
        print(name, link2)
        try:
            prof_resp = requests.get(link2)          # requesting prof homepgae
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def yale():
    url = "https://cpsc.yale.edu/people/faculty"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")
    
    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Yale University"
    country = "USA"

    grabage_emails = ['portico-services@ucl.ac.uk']
    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    
    d = soup.find_all('td', {'class':"views-field views-field-name"})
    # print(d)

    #iterating for every prof
    for i in d:
        a = i.find('a')                     # a contains the name and the homepage of prof
        name = a.get_text()                 # extracting prof name
        aa = i.find('a', text="Website")
        
        if aa != None:
            link = aa.get('href')                # extracting prof page link
        else:
            continue

        try:
            prof_resp = requests.get(link)          # requesting prof homepgae
        except:
            continue        

        email = "Not Found"

        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_cornell():   
    url = "https://www.cs.cornell.edu/people/faculty"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")

    # file initialization to write
    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Cornell University"
    country = "USA"

    grabage_emails = ['microservices-bench-L@list.cornell.edu']
    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    
    d = soup.find_all('h6', {'class':"text-primary"})
    # print(d)

    #iterating for every prof
    for i in d:
        a = i.find('a')                     # a contains the name and the homepage of prof
        link = a.get('href')                # extracting prof page link
        if link == None:
            continue
        elif link[0] == '#' or link[0:6] == 'mailto':
            continue
        name = a.get_text()                 # extracting prof name
        try:
            prof_resp = requests.get(link)          # requesting prof homepgae 
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_columbia():    
    url = "https://www.cs.columbia.edu/people/faculty/"   # homepage url
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Columbia University"
    country = "USA"

    grabage_emails = ['egc@ee.columbia.edu']
    var = [csvwriter, u_name, country]

    # using set() to store to remove duplicates emails
    emails = set()

    # d gives the array of all profs on the dept homepage
    
    d = soup.find_all('span', {'class':"faculty-name"})
    # print(d)

    #iterating for every prof
    for i in d:
        a = i.find('a')                     # a contains the name and the homepage of prof
        link = a.get('href')                # extracting prof page link
        if link == None:
            continue
        name = a.get_text()                 # extracting prof name

        split_name = name.split(" ")

        # print(u_name, name, link)
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_edinburgh():
    url = "https://www.ed.ac.uk/informatics/people/academic"   # homepage url
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of Edinburgh"
    country = "Scotland"

    grabage_emails = ['school-office@inf.ed.ac.uk', 'timc@inf.ed.ac.uk', 'neil.brown@Ed.ac.uk']
    var = [csvwriter, u_name, country]

    # using set() to store to remove duplicates emails
    emails = set()

    # d gives the array of all profs on the dept homepage
    
    dd = soup.find('div', {'class':"inf-people"})
    d = dd.find_all('a')
    # print(d)

    #iterating for every prof
    for i in d:
        # a = i.find('a')                     # a contains the name and the homepage of prof
        link = i.get('href')                # extracting prof page link
        if link == None:
            continue
        elif link[0] == '#' or link[0:6] == 'mailto':
            continue
        name = i.get_text()                 # extracting prof name
        # print(link, "\t", name)
        split_name = name.split(" ")

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_michigan():
    url = "https://cse.engin.umich.edu/people/faculty/"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of Michigan"
    country = "USA"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':'people_lists'})
    d = dd.find_all('div', {'class':'eecs_person_copy'})

    #iterating for every prof
    for i in d:
        a = i.find('a', text='Website')
        if a == None:
            continue
        link = a.get('href')

        h4 = i.find('h4')
        name = (h4.get_text()).strip()
        name = " ".join(name.split())

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_hongkong():    
    url = "https://www.cs.hku.hk/people/academic-staff"   # homepage url
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of Hong Kong"
    country = "Hong Kong"

    grabage_emails = []
    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    # dd = soup.find('div', {'class':"row"})
    d = soup.find_all('tr')
    # print(d)

    #iterating for every prof
    for i in d:
        a = i.find('a')                     # a contains the name and the homepage of prof
        link = a.get('href')
        if link[0] == '/':
            link = 'https://www.cs.hku.hk'+link
        name = (a.get_text()).strip()                 # extracting prof name
        name = " ".join(name.split())

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def peking_uni():    

    url = "https://eecs.pku.edu.cn/Home/People/Faculty.htm"   # homepage url
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    try:    
        r = requests.get(url, headers=headers)
    except:
        return

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Peking University"
    country = "China"

    grabage_emails = []
    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('ul', {'class':"zzjs1M2"})
    d = soup.find_all('a')
    # print(d)

    #iterating for every prof
    for i in d:
        # a = i.find('a')                     # a contains the name and the homepage of prof
        link = i.get('href')
        l = len(link)
        link = link[l-19:]
        link = 'https://eecs.pku.edu.cn'+link 
        name = i.get_text()                 # extracting prof name

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_tokyo():    
    url = "https://www.i.u-tokyo.ac.jp/edu/course/cs/members_e.shtml"   # homepage url
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of Tokyo"
    country = "Japan"

    grabage_emails = []
    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('table')
    d = dd.find_all('tr')
    # print(d)

    #iterating for every prof
    for i in d:
        a = i.find('a')                     # a contains the name and the homepage of prof
        if a == None:
            continue
        link = a.get('href')
        name = a.get_text()                 # extracting prof name

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def john_hopkins():    
    url = "https://www.cs.jhu.edu/faculty/"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "John Hopkins University"
    country = "USA"

    grabage_emails = ['wse-logo-white-vertical@2x.png', 'csnews@jhu.edu', 'contactus@cs.jhu.edu']
    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    d = soup.find_all('div', {'class':'highlight-box faculty-member-card'})
    # print(d)

    #iterating for every prof
    for i in d:
        # print(i)
        h = i.find('h3')                     # a contains the name and the homepage of prof
        a = h.find('a')
        link = a.get('href')
        name = a.get_text()                 # extracting prof name
        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_toranto():    
    url = "https://web.cs.toronto.edu/contact-us/faculty-directory#teachingstream"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of Totanto"
    country = "Canada"

    grabage_emails = []
    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':'main-content'})
    d = dd.find_all('tr')
    
    for i in d:
        a = i.find('a')
        if a == None:
            continue
        link = a.get('href')                # extracting prof page link
        name = a.get_text()                 # extracting prof name
        if name == 'Stavros Tsogkasm':
            break

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        aa = a.find_next('a')
        mailto = aa['href']
        if mailto[0:6] == "mailto" :
            email = aa.get_text()
        else:
            email = "Not Found"

        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_menchester():    
    url = "https://www.cs.manchester.ac.uk/about/people/academic-and-research-staff/"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of Menchester"
    country = "England"

    grabage_emails = ['mkearns@lehman.com', 'michael.kearns@bofasecurities.com', 'lhoot@seas.upenn.edu', 'kearmic@amazon.com']
    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    d = soup.find_all('li', {'class':["tabrowwhite", "tabrowgrey"]})
    # d2 = soup.find_all('li', {'class':"tabrowgrey"})

    # print(d)  

    #iterating for every prof
    for i in d:
        a = i.find('a')                     # a contains the name and the homepage of prof
        if a == None:
            continue
        link = a.get('href')
        name = a.get_text()                 # extracting prof name
        name = name.replace("\t", "")
        name = name.replace("\n", "")
        try:
            prof_resp = requests.get(link)          # requesting prof homepgae
            prof_soup = BeautifulSoup(prof_resp.text, "html.parser") 
        except:
            continue

        print(u_name, name, link)
        pp = prof_soup.find('a', text='Personal Website')
        # print(pp)
        if pp == None:
            continue
        link2 = pp.get('href')
        print(name, link2)

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link2, headers=headers)   
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def northwestern_uni():    
    url = "https://www.mccormick.northwestern.edu/computer-science/people/faculty.html"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Northwestern University"
    country = "USA"

    grabage_emails = []
    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    d = soup.find_all('div', {'class':"faculty-info"})
    # print(d)

    #iterating for every prof
    for i in d:
        a = i.find('a')                     # a contains the name and the homepage of prof
        link = a.get('href')
        if 'hardav' in link:
            link = 'https://users.cs.northwestern.edu/~hardav/research_interests.htm'
        name = a.get_text()                 # extracting prof name
        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")    

# ============================

def UC_berkeley():    
    url = "https://www2.eecs.berkeley.edu/Faculty/Lists/CS/faculty.html"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of California, Berkeley"
    country = "USA"

    grabage_emails = ['gavinboy@berkeley.edu', 'tamille@eecs.berkeley.edu', 'riamelendres@berkeley.edu', 'damonh@berkeley.edu', 'mkader@berkeley.edu', 
                    'schonenberg@berkeley.edu', 'sarunyon@berkeley.edu', 'marys@eecs.berkeley.edu', 'boban@eecs.berkeley.edu', 'joelmold@berkeley.edu',
                    'mrose@berkeley.edu', 'wkung@berkeley.edu', 'derekj@berkeley.edu', 'elisem@berkeley.edu', 'marleneperez@berkeley.edu', 'jessicagamble@berkeley.edu',
                    'annie@erso.berkeley.edu', 'tracey@berkeley.edu' ]
    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    d = soup.find_all('h3', {'class':"media-heading"})
    # print(d)

    #iterating for every prof
    for i in d:
        a = i.find('a')                     # a contains the name and the homepage of prof
        link = a.get('href')
        link = 'https://www2.eecs.berkeley.edu'+link
        name = a.get_text()                 # extracting prof name 

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def aus_nat_uni():    
    url = "https://cecs.anu.edu.au/people/academic?items_per_page=All"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Australian National University"
    country = "Australia"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':'view-content'})
    d = dd.find_all('tr', {'class':['odd views-row-first', 'odd','even']})

    # print(d)  

    #iterating for every prof
    for i in d:
        a = i.find('a')                     # a contains the name and the homepage of prof
        if a == None:
            continue
        link = 'https://cecs.anu.edu.au' + a.get('href')
        name = a.get_text()                 # extracting prof name
        name = name.replace("\t", "")
        name = name.replace("\n", "")

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        ee = i.find('td', {'class':'views-field views-field-field-acton-person-email'})
        if ee == None:
            email = "Not Found"            
        else:
            email = (ee.find('a')).get_text()

        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def kings_college_london():   
    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Kings College London"
    country = "England"

    grabage_emails = ['pagemaster@cst.cam.ac.uk']
    var = [csvwriter, u_name, country]


    for i in range(1,6):
        url = 'https://www.kcl.ac.uk/informatics/about/people?page='+str(i)+'&role=Teaching-fellows%2cResearchers%2cVisiting%2cAffiliates%2cAcademics'
        # print(url)
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        r = requests.get(url, headers=headers)     
        soup = BeautifulSoup(r.text, "html.parser")

        # d gives the array of all profs on the dept homepage
        dd = soup.find('section', {'class':"block block--people-listing"})
        d = dd.find_all('li', {'role':"listitem"})
        # print(d)  

        #iterating for every prof
        for i in d:
            # print(i)
            aa = i.find('h4')
            a = aa.find('a')                     # a contains the name and the homepage of prof
            link = 'https://www.kcl.ac.uk' + a.get('href')
            name = a.get_text()                 # extracting prof name
            name = name.replace("\t", "")
            name = name.replace("\n", "")

            # print(u_name, name, link)
            # check if link is valid on Not
            try:    
                prof_resp = requests.get(link, headers=headers)   
            except:
                continue

            email = "Not Found"
            print(u_name, name, link)
            filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def mcgill_uni():    
    url = "https://www.cs.mcgill.ca/people/faculty/"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "McGill University"
    country = "Canada"

    grabage_emails = ['hv@cs.mcgill.ca']
    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    d = soup.find_all('div', {'class':'col-md-6'})

    # print(d)  

    #iterating for every prof
    for i in d:
        h = i.find('h4')                     # a contains the name and the homepage of prof
        name = h.get_text()

        a = i.find('a', text='Website')
        link = a.get('href')
        name = name.replace("\t", "")
        name = name.replace("\n", "")

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def fudan_uni():    
    url = "http://www.cs.fudan.edu.cn/en/?page_id=351"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Fudan University"
    country = "China"

    grabage_emails = ['cs_school@fudan.edu.cn']
    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':'cont'})
    d = dd.find_all('a')

    # print(d)  

    #iterating for every prof
    for i in d:
        # a = i.find('a')                     # a contains the name and the homepage of prof
        link = i.get('href')
        name = i.get_text()                 # extracting prof name
        name = name.replace("\t", "")
        name = name.replace("\n", "")

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def nyc_uni():    
    url = "https://cs.nyu.edu/dynamic/people/faculty/"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "New York University"
    country = "USA"

    grabage_emails = []
    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('ul', {'class':"people-listing"})
    d = dd.find_all('div', {'class':"col-sm-8 col-xs-6"})
    # print(d)  

    #iterating for every prof
    for i in d:
        # print(i)
        a = i.find('a')                     # a contains the name and the homepage of prof
        if a == None:
            continue
        link = a.get('href')
        name = a.get_text()                 # extracting prof name
        name = name.replace("\t", "")
        name = name.replace("\n", "")

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def ucla():    
    url = "https://samueli.ucla.edu/search-faculty/#cs"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "UCLA"
    country = "USA"

    grabage_emails = []
    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    d = soup.find_all('div', {'class':"card_description"})

    #iterating for every prof
    for i in d:
        print(i)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def seoul_university():    
    url = "https://cse.snu.ac.kr/en/people/faculty"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Seoul National University"
    country = "South Korea"

    grabage_emails = []
    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':"view-content"})
    d = dd.find_all('div', {'class':"views-field views-field-title"})
    # print(d)  

    #iterating for every prof
    for i in d:
        # print(i)
        a = i.find('a')                     # a contains the name and the homepage of prof
        if a == None:
            continue
        link = 'https://cse.snu.ac.kr' + a.get('href')
        name = a.get_text()                 # extracting prof name
        name = name.replace("\t", "")
        name = name.replace("\n", "")

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def kaist():    
    url = "https://cs.kaist.ac.kr/people/faculty"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "KAIST"
    country = "South Korea"

    grabage_emails = []
    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':"list_warp"})
    d = dd.find_all('li', {'class':"horiz_item"})
    # print(d)  

    #iterating for every prof
    for i in d:
        # print(i)
        aa = i.find('div', {'class':'item fix'})
        oc = aa['onclick']
        oc = oc.replace('facultyView(', "")
        oc = oc.replace(')', "")
        a = oc.split(",")
        a1 = a[0].replace(" ", '')
        a2 = a[1].replace(" ", '')
        link = 'https://cs.kaist.ac.kr/people/view?idx='+ a1 + '&kind=faculty&menu='+ a2
        nam = i.find('p', {'class':'name'})
        name = nam.get_text()                 # extracting prof name
        name = name.replace("\t", "")
        name = name.replace("\n", "")
        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_sydney():    
    url = "https://www.sydney.edu.au/engineering/schools/school-of-computer-science/school-staff.html"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of Sydney"
    country = "Australia"

    grabage_emails = []
    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':"bodyColumn"})
    d = dd.find_all('a')
    # print(d)  

    #iterating for every prof
    for i in d:
        link = i.get('href')
        name = (i.get_text()).strip()
        name = " ".join(name.split())

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_melbourne():
    url = "https://cis.unimelb.edu.au/people/#academic"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of Melbourne"
    country = "Australia"

    grabage_emails = []
    var = [csvwriter, u_name, country]


    # d gives the array of all profs on the dept homepage
    
    dd = soup.find('div', {'class':"tab", 'id':'academic'})
    d = dd.find_all('tr')
    # print(d)  

    #iterating for every prof
    for i in d:
        a = i.find('a')
        name1 = i.find('td') 
        if a == None or name1 == None:
            continue

        name2 = name1.find_next('td')
        name3 = name2.find_next('td')
        name = name2.get_text()+" "+name3.get_text() 

        link = a.get('href')
        # check if link is valid on not
        try:    
            prof_resp = requests.get(link)        
        except:
            continue

        email = "Not Found"
        # print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def duke_university():
    url = "https://www.cs.duke.edu/people/faculty"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Duke University"
    country = "USA"

    grabage_emails = ['webmaster@cs.duke.edu']
    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    
    dd = soup.find('div', {'class':"faculty list"})
    d = dd.find_all('div', {'class':'faculty card'})
    # print(d)  

    #iterating for every prof
    for i in d:
        a = i.find('a')
        name = a.get_text()
        nam = name.split(',')
        name = nam[1]+" "+nam[0]
        link = 'https://www.cs.duke.edu' + a.get('href')
        # check if link is valid on not
        try:    
            prof_resp = requests.get(link)        
        except:
            continue

        mail = i.find('dt', text='Email:')
        # print()
        if mail != None:
            email = (mail.find_next('dd').get_text())
            email = email.replace(" at ", '@')
        else:
            email = 'Not Found'
            
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)

    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def chinese_uni_hongkong():
    url = "https://www.cse.cuhk.edu.hk/research/computer-engineering/computer-architecture/"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Chinese Uni of Hong Kong"
    country = "Hong Kong"

    grabage_emails = ['dept@cse.cuhk.edu.hk', 'pgenquiry@cse.cuhk.edu.hk', 'ug-admiss@cse.cuhk.edu.hk', 'info@msc.cse.cuhk.edu.hk']

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    
    dd = soup.find('div', {'id':"sptp-9823"})
    # print(dd)
    d = dd.find_all('div', {'class':'sptp-member border-bg-around-member sptp-list-item sptp-square '})
    # print(d)  

    #iterating for every prof
    for i in d:
        a = i.find('a',{'class':'sptp-member-avatar'})
        name = (i.find('h2')).get_text()
        link = 'https://www.cse.cuhk.edu.hk' + a.get('href')
        # check if link is valid on not
        try:    
            prof_resp = requests.get(link)        
        except:
            continue

        email = 'Not Found'

        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)

    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_NSW():
    url = "https://www.unsw.edu.au/engineering/computer-science-and-engineering/about-us/our-people"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of New South Wales"
    country = "Australia"

    grabage_emails = ['webmaster@cs.duke.edu']

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    
    dd = soup.find('div', {'class':"objects-wrapper object-items"})
    d = dd.find_all('div', {'class':"node-content"})
    # print(d)  

    #iterating for every prof
    for i in d:
        a = (i.find('div', {'class':'node-title'})).find('a')
        name = a.get_text()
        name = name.strip()
        link = 'https://www.unsw.edu.au' + a.get('href')
        # check if link is valid on not
        try:    
            prof_resp = requests.get(link)        
        except:
            continue
            
        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)

    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def ubc_canada():
    url = "https://www.cs.ubc.ca/people/faculty"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "UBC Canada"
    country = "Canada"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    
    dd = soup.find('div', {'class':"view-content"})
    d = dd.find_all('td', {'headers':"view-field-person-lname-table-column"})
    # print(d)  

    #iterating for every prof
    for i in d:
        a = i.find('a')
        name = (a.get_text()).strip()
        link = 'https://www.cs.ubc.ca' + a.get('href')
        # check if link is valid on not
        try:    
            prof_resp = requests.get(link)        
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)

    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_queensland():
    url = "https://www.itee.uq.edu.au/our-people#academic"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of Queensland"
    country = "Australia"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'id':"block-views-itee-contacts-block-1"})
    d = dd.find_all('tr')
    # print(d)  

    #iterating for every prof
    for i in d:
        aa = i.find('td', {'class':"views-field views-field-title"})
        if aa == None:
            continue
        a = aa.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        link = a.get('href')
        # check if link is valid on not
        try:    
            prof_resp = requests.get(link)        
        except:
            continue

        ee = i.find('td', {'class':"views-field views-field-field-contact-email"})
        if ee == None:
            email = "Not Found"
        else:
            email = (ee.find('a')).get_text()

        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)

    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def shanghai_jt():
    url = "http://www.cs.sjtu.edu.cn/en/Faculty.aspx"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Shanghai JT University"
    country = "China"

    grabage_emails = ['webmaster@cs.sjtu.edu.cn', 'qndeng@sjtu.edu.cn']

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    
    dd = soup.find('p', text='Institute of Computer Architecture')
    ddd = dd.find_next('div', {'class':"Faculty"})
    d = ddd.find_all('li')
    # print(d)  

    #iterating for every prof
    for i in d:
        a = i.find('a')
        name = (a.get_text()).strip()
        link = 'http://www.cs.sjtu.edu.cn/en/' + a.get('href')
        # check if link is valid on not
        try:    
            prof_resp = requests.get(link)        
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)

    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def city_uni_hk():
    url = "https://www.cs.cityu.edu.hk/people/academic_staff.html"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "City University Hong Kong"
    country = "Hong Kong"

    grabage_emails = ['webmaster@cs.sjtu.edu.cn', 'qndeng@sjtu.edu.cn']

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    
    dd = soup.find('div', {'class':'cityu-staff-info'})
    d = dd.find_all('td', style="vertical-align: text-top")
    # print(d)  

    #iterating for every prof
    for i in d:
        a = i.find('a')
        name = (a.get_text()).strip()
        link = a.get('href')
        # check if link is valid on not
        try:    
            prof_resp = requests.get(link)        
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)

    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def carnegie_mellon():
    url = "https://csd.cmu.edu/research-areas/computer-architecture"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Carnegie Mellon University"
    country = "USA"

    grabage_emails = ['csd-marcom-info@cs.cmu.edu']

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    
    dd = soup.find('table', {'class':'views-table cols-4'})
    d = dd.find_all('tr', {'class':["odd views-row-first", "even", "odd"]})
    # print(d)  

    #iterating for every prof
    for i in d:
        aa = i.find('td')
        a = aa.find('a')
        l_name = (a.get_text()).strip()
        f_name = ((aa.find_next('td')).get_text()).strip()
        name = f_name+ " "+l_name
        link = a.get('href')
        # check if link is valid on not
        try:    
            prof_resp = requests.get(link)        
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)

    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_psl():
    url = "https://www.di.ens.fr/directory"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University PSL"
    country = "France"

    grabage_emails = ['acm@2x.png', 'tim@2x.png', 'beig@ens.fr', 'feret@ens.fr',]

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    
    dd = soup.find('div', {'class':"container", 'align':"center"})
    d = dd.find_all('tr')
    # print(d)  

    #iterating for every prof
    for i in d:
        a = i.find('td')
        name = (a.get_text()).strip()
        mail = (a.find_next('td')).find('a')
        if mail == None:
            continue
        link = mail.get('href')
        # check if link is valid on not
        try:    
            prof_resp = requests.get(link)        
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)

    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def zhejiang_uni():
    url = "http://www.en.cs.zju.edu.cn/jsjxtjgywlaqyjs/list.htm"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Zhejiang University"
    country = "China"

    grabage_emails = ['xwmaster@zju.edu.cn']

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    
    dd = soup.find('ul', {'class':"wp_article_list"})
    d = dd.find_all('div', {'class':"fields pr_fields"})
    # print(d)  

    #iterating for every prof
    for i in d:
        a = i.find('a')
        name = (a.get_text()).strip()
        link = a.get('href')
        # check if link is valid on not
        try:    
            prof_resp = requests.get(link)        
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)

    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def ucsd():
    url = "https://cse.ucsd.edu/people/faculty-profiles/faculty"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of California SD"
    country = "USA"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    
    dd = soup.find('div', {'class':'view-content'})
    d = dd.find_all('div', {'class':"col col-xs-6 col-sm-6 col-md-4 col-lg-3 "})

    #iterating for every prof
    for i in d:
        # print(i)
        a = (i.find('a')).find_next('a')
        name = (a.get_text()).strip()
        link = 'https://cse.ucsd.edu'+ a.get('href')

        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link)  
            prof_soup = BeautifulSoup(prof_resp.text, "html.parser")   
        except:
            continue

        aa = prof_soup.find('a', text='Website')
        if aa == None:
            continue
        link2 = aa.get('href')
        try:    
            prof_resp2 = requests.get(link2)  
            prof_soup2 = BeautifulSoup(prof_resp2.text, "html.parser")   
        except:
            continue
            
        email = "Not Found"
        print(name, link2)
        filterandgetEmail(var, grabage_emails, name, link2, email, prof_resp2)

    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def monash_uni():
    url = "https://www.monash.edu/it/about-us/our-people"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Monash University "
    country = "Australia"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    
    dd = soup.find('div', {'id':'content_500581'})
    d = dd.find_all('div', {'class':"profile-content"})

    #iterating for every prof
    for i in d:
        a = i.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        link = a.get('href')
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link)        
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)

    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def tokyo_uni_tech():
    url = "http://www.cs.titech.ac.jp/people-e.html"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Tokyo University of Technology "
    country = "Japan"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    
    dd = soup.find('div', {'class':'section'})
    d = dd.find_all('tr')

    #iterating for every prof
    for i in d:
        a = i.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        link = a.get('href')
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link)        
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)

    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def delft_uni_tech():
    url = "https://www.tudelft.nl/en/eemcs/the-faculty/professors"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Delft University of Technology"
    country = "Netherland"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    
    dd = soup.find('article', {'class':'md-9'})
    d = dd.find_all('tr')

    #iterating for every prof
    for i in d:
        a = i.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        link = a.get('href')
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link)        
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)

    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def brown_uni():
    url = "http://cs.brown.edu/people/faculty/"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Brown University "
    country = "USA  "

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    
    dd = soup.find('div', {'id':'content'})
    d = dd.find_all('li', {'class':"profile-name"})

    #iterating for every prof
    for i in d:
        name = (i.get_text()).strip()
        a = i.find_next('a')
        if a == None:
            continue
        link = 'http://cs.brown.edu' + a.get('href')
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link)        
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)

    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_warwick():
    url = "https://warwick.ac.uk/fac/sci/dcs/people/summaries/"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of Warwick"
    country = "UK"

    grabage_emails = ['RichardKirkOfficeHours@livewarwickac.onmicrosoft.com']

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    
    dd = soup.find('div', {'id':'entries'})
    d = dd.find_all('div', {'class':"entryContent"})

    #iterating for every prof
    for i in d:
        h2 = i.find('h2')
        a = h2.find('a')
        if a == None:
            continue

        if (a.get_text()) == None or (a.get_text()) == "":
            # name = (a.find_next('a')).get_text()
            a = a.find_next('a')

        name = (a.get_text()).strip()
        link = a.get('href')

        check_text = (h2.find_next('p')).get_text()
        check_text = check_text.strip()
        if check_text == 'Research Student':
            continue

        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link)        
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)

    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_wisconsin():
    url = "https://www.cs.wisc.edu/people/faculty/"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of Wisconsin"
    country = "USA"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    
    dd = soup.find('div', {'class':'faculty-list'})
    d = dd.find_all('div', {'class':"faculty-member-content"})

    #iterating for every prof
    for i in d:
        h3 = i.find('h3')
        a = h3.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        link = a.get('href')
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link)        
        except:
            continue

        aaa = h3.find_next('a')
        aa = aaa.find_next('a', href=True)
        if aa == None :
            email = "Not Found"
        else:
            email = aa.get_text()

        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)

    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def taiwan_university():
    url = "https://www.csie.ntu.edu.tw/~new/people_faculty.html.en"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "National Taiwan University"
    country = "Taiwan"

    grabage_emails = ['robin@nis-lab.is.s.u-tokyo.ac.jp', 'robin@cmlab.csie.ntu.edu.tw', 'robin@ntu.edu.tw', 'robin@im.ntu.edu.tw', 'hungsh@gmail.com']

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    
    dd = soup.find('div', {'id':'cbox'})
    d = dd.find_all('table')

    #iterating for every prof
    for i in d:
        link_span = i.find('span')
        a = link_span.find('a')
        if a == None:
            continue
        link = a.get('href')

        name_span = link_span.find_next('span')
        name = name_span.get_text()
        name = name.strip()

        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link)        
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)

    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def korea_university():
    url = "https://cs.korea.edu/en_cs/intro/fulltime_faculty.do?mode=list&&articleLimit=100&article.offset=10"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Korea University"
    country = "South Korea"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    
    dd = soup.find('div',  {'class':"pro_list"})
    d = dd.find_all('div', {'class':" "})
    # print(d)  

    #iterating for every prof
    for i in d:
        dt = (i.find('dl')).find('dt')
        name = (dt.text).strip()

        dd1 = dt.find_next('dd')
        email = dd1.text

        dd2 = dd1.find_next('dd')
        if dd2 == None:
            continue
        link = dd2.text

        # check if link is valid on not
        try:    
            prof_resp = requests.get(link)        
        except:
            continue

        # email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)

    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_austin():
    url = "https://www.cs.utexas.edu/people"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of Austin, Texas"
    country = "USA"

    grabage_emails = ['oea@cs.utexas.edu', 'under-info@cs.utexas.edu', 'csadmis@cs.utexas.edu', 'help@cs.utexas.edu']

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    
    dd = soup.find('div', {'class':'view-content'})
    d = dd.find_all('div', {'class':"field field-name-title field-type-ds field-label-hidden"})

    #iterating for every prof
    for i in d:
        a = i.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        link = "https://www.cs.utexas.edu" + a.get('href')
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link)        
        except:
            continue

        email = "Not Found"

        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)

    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def osaka_uni():
    url = "https://www.ist.osaka-u.ac.jp/english/introduction/professors/computer-science/"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Osaka University"
    country = "Japan"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    
    dd = soup.find('div', {'class':'main-container-section'})
    d = dd.find_all('tr')

    #iterating for every prof
    for i in d:
        a = i.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        link = a.get('href')
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link)        
        except:
            continue

        email = "Not Found"

        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)

    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_washington():
    url = "https://www.cs.washington.edu/people/faculty"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of Washington"
    country = "USA"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    
    dd = soup.find('div', {'class':'view-content'})
    d = dd.find_all('div', {'class':"col-sm-10"})

    #iterating for every prof
    for i in d:
        a = (i.find('div', {'class':'directory-name'})).find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        link = a.get('href')
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link)        
        except:
            continue

        email = "Not Found"

        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)

    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def hong_kong_poly_uni():
    url = "https://www.comp.polyu.edu.hk/en-us/staffs/index/1"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Hong Kong P University"
    country = "Hong Kong"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    
    dd = soup.find('ul', {'class':'staff-post clearfix'})
    d = dd.find_all('div', {'class':"staff-info"})

    #iterating for every prof
    for i in d:
        a = i.find('a', {'class':"name-link"})
        if a == None:
            continue
        name = (a.get_text()).strip()
        link = 'https://www.comp.polyu.edu.hk'+ a.get('href')
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link)        
        except:
            continue

        email = "Not Found"

        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)

    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_copenhagen():
    url = "https://di.ku.dk/english/staff/vip/"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of Copenhagen"
    country = "Denmark"

    grabage_emails = ['info@di.ku.dk']

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    
    dd = soup.find('table', {'class':'medarbejdertable table list '})
    d = dd.find_all('tr')

    #iterating for every prof
    for i in d:
        a = i.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        link = 'https://di.ku.dk/english/staff/vip/'+ a.get('href')
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link)        
        except:
            continue

        email = "Not Found"

        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)

    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def postech_korea():
    url = "https://ecse.postech.ac.kr/member/professor/"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Pohang University"
    country = "South Korea"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    
    dd = soup.find('div', {'class':'professor'})
    d = dd.find_all('div', {'class':'title_box'})

    #iterating for every prof
    for i in d:
        name = (i.find('h3', {'class':'name'})).get_text()
        title = (i.find('span', {'class':"tit"})).get_text()
        name = name.replace(title, "")

        a_span = i.find('span', {'class':"icon step2"})
        if a_span == None:
            continue
        link = (a_span.find('a')).get('href')
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link)        
        except:
            continue

        a_mail = i.find('span', {'class':"icon step1"})
        if a_mail != None:
            email = (a_mail.find('a')).get('href')
            email = email[7:]
        else:
            email = "Not Found"

        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)

    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_glasgow():
    url = "https://www.gla.ac.uk/schools/computing/staff/#research%26teaching"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of Glasgow"
    country = "UK"

    grabage_emails = ['Qi.Cao@glasgow.ac.uk']

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    
    dd = soup.find('ul', {'id':'research-teachinglist'})
    d = dd.find_all('li')

    #iterating for every prof
    for i in d:
        a = i.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        nam = name.split(',')
        name = nam[1]+" "+nam[0]
        link = 'https://www.gla.ac.uk'+ a.get('href')
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link)        
        except:
            continue

        email = "Not Found"

        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)

    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def tohoku_university():
    url = "https://www.is.tohoku.ac.jp/en/laboratory/list_dept/a12.html"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Tohoku University"
    country = "Japan"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    
    dd = soup.find('div', {'class':'page_infomation'})
    d = dd.find_all('li')

    #iterating for every prof
    for i in d:
        a = i.find('a', {'class':'rm'})
        if a == None:
            continue
        aa = i.find('span', {'class':'name'})
        name = (aa.get_text()).strip()
        link = a.get('href')
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link)        
        except:
            continue

        email = "Not Found"

        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)

    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def georgia_inst_tech():
    url = "https://www.scs.gatech.edu/people/faculty"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Georgia Institute of Technology"
    country = "USA"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    
    dd = soup.find('div', {'class':'view-content'})
    d = dd.find_all('div', {'class':'gt-person-box block block-block half-width related-info-block'})

    #iterating for every prof
    for i in d:
        h4 = i.find('h4', {'class':'name fn'})
        a = h4.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        link = 'https://www.scs.gatech.edu/' + a.get('href')
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link)        
        except:
            continue

        a_mail = i.find('a', text='Email')
        if a_mail != None:
            email = a_mail.get('href')
            email = email[7:]
        else:
            email = "Not Found"

        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)

    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_auckland():
    url = "http://www.science.auckland.ac.nz/people/search#?search=&page=1&rows=50&category=staff&orderBy=lastname&filterOrganisation=COMSCI"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of Auckland"
    country = "New Zealand"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    
    dd = soup.find('div', {'class':'content container-fluid'})
    d = dd.find_all('div', {'class':'row ng-scope odd'})
    print(d)

    #iterating for every prof
    for i in d:
        h4 = i.find('h4', {'class':'name fn'})
        a = h4.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        link = 'https://www.scs.gatech.edu/' + a.get('href')
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link)        
        except:
            continue

        a_mail = i.find('a', text='Email')
        if a_mail != None:
            email = a_mail.get('href')
            email = email[7:]
        else:
            email = "Not Found"

        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)

    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_illinois():
    url = "https://cs.illinois.edu/about/people/all-faculty"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of Illinois"
    country = "USA"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    
    dd = soup.find('div', {'class':'directory-list directory-list-4'})
    d = dd.find_all('div', {'class':'name'})

    #iterating for every prof
    for i in d:
        a = i.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        link = 'https://cs.illinois.edu' + a.get('href')
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link)        
        except:
            continue

        div_mail = i.find_next('div', {'class':'email'})
        if div_mail != None:
            a_mail = (div_mail.find('a')).get('href')
            email = a_mail[7:]
        else:
            email = "Not Found"

        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)

    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def ku_leaven():
    url = "https://distrinet.cs.kuleuven.be/people/"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "KU Leuven"
    country = "Belgium"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    
    dd = soup.find('div', {'class':'twocol'})
    d = dd.find_all('li')

    #iterating for every prof
    for i in d:
        a = i.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        link = 'https://distrinet.cs.kuleuven.be' + a.get('href')
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link)        
        except:
            continue

        email = "Not Found"

        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)

    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def durham_university():
    url = "https://www.durham.ac.uk/departments/academic/computer-science/about-us/staff/"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Durham University"
    country = "UK"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    
    dd = soup.find('div', {'class':'text-long u-max-w-measure-lg u-leading-normal u-o-3'})
    dd = dd.find_next('div', {'class':'text-long u-max-w-measure-lg u-leading-normal u-o-3'})
    d = dd.find_all('tr')

    #iterating for every prof
    for i in d:
        a = i.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        link = a.get('href')
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link)        
        except:
            continue

        a_mail = a.find_next('a')
        if a_mail != None:
            email = a_mail.get('href')
            email = email[7:]
        else:
            email = "Not Found"

        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)

    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def yonsei_uni():
    url = "https://yonsei.pure.elsevier.com/en/organisations/department-of-computer-science/persons/"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Yonsei University"
    country = "South Korea"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    
    dd = soup.find('ul', {'class':'grid-results'})
    d = dd.find_all('div', {'class':'result-container'})

    #iterating for every prof
    for i in d:
        a = i.find('a', {'class':'link person'})
        if a == None:
            continue
        name = (a.get_text()).strip()
        link = a.get('href')
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link)        
        except:
            continue

        a_mail = (i.find('ul', {'class':'relations email'})).find('a')
        if a_mail != None:
            email = a_mail.get('href')
            email = email[7:]
        else:
            email = "Not Found"

        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)

    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_bermingham():
    url = "https://www.birmingham.ac.uk/schools/computer-science/people/index.aspx"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of Birmingham"
    country = "UK"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    
    d = soup.find_all('article', {'class':"media staff media--flipped"})
    # d = dd.find_all('div', {'class':'result-container'})

    #iterating for every prof
    for i in d:
        h3 = i.find('h3')
        if h3 == None:
            continue
        a = h3.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        link = 'https://www.birmingham.ac.uk' +a.get('href')
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link)        
        except:
            continue

        # a_mail = (i.find('ul', {'class':'relations email'})).find('a')
        # if a_mail != None:
        #     email = a_mail.get('href')
        #     email = email[7:]
        # else:
        #     email = "Not Found"

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)

    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def sungkyunkwan_uni():
    url = "https://cs.skku.edu/en/people/staff"   # homepage url
    try:    
        r = requests.get(url)
    except:
        return

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Sungkyunkwan University"
    country = "South Korea"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    # d = soup.find('a', {'class':"accordian-title"})
    d = soup.find_all('article', {'class':"media staff media--flipped"})
    # d = dd.find_all('div', {'class':'result-container'})

    #iterating for every prof
    for i in d:
        h3 = i.find('h3')
        if h3 == None:
            continue
        a = h3.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        link = 'https://www.birmingham.ac.uk' +a.get('href')
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link)        
        except:
            continue

        # a_mail = (i.find('ul', {'class':'relations email'})).find('a')
        # if a_mail != None:
        #     email = a_mail.get('href')
        #     email = email[7:]
        # else:
        #     email = "Not Found"

        email = "Not Found"
        print(name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)

    file.close()
    print("=====", u_name, "Finished =====")

# ================================

def rice_university():
    url = "https://csweb.rice.edu/people/faculty"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Rice University"
    country = "USA"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    
    dd = soup.find('div', {'id':'block-faculty'})
    d = dd.find_all('div', {'class':'result-container'})

    #iterating for every prof
    for i in d:
        a = i.find('a', {'class':'link person'})
        if a == None:
            continue
        name = (a.get_text()).strip()
        link = a.get('href')
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link)        
        except:
            continue

        a_mail = (i.find('ul', {'class':'relations email'})).find('a')
        if a_mail != None:
            email = a_mail.get('href')
            email = email[7:]
        else:
            email = "Not Found"

        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)

    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_southampton():
    url = "https://www.ecs.soton.ac.uk/people"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of Southampton"
    country = "UK"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    
    dd = soup.find('tbody', {'class':'list'})
    d = dd.find_all('tr')

    #iterating for every prof
    for i in d:
        td1 = i.find('td')
        a = td1.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        # break loop on professor as list is very long
        if name == 'Dr Chris Adetunji':
            break

        link = 'https://www.ecs.soton.ac.uk'+a.get('href')
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link)        
        except:
            continue

        # remove research sudents from list
        td2_text = (td1.find_next('td')).get_text()
        if ('student' in td2_text) or ('Visitor' in td2_text) :
            continue

        td4 = (((td1.find_next('td')).find_next('td')).find_next('td'))
        a_mail = td4.find('a')
        if a_mail != None:
            email = a_mail.get('href')
            email = email[7:]
        else:
            email = "Not Found"

        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)

    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_leeds():
    url = "https://eps.leeds.ac.uk/computing/stafflist"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of Leeds"
    country = "UK"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    
    dd = soup.find('table', {'class':'tablesaw table-profiles table-hover'})
    tbody = soup.find('tbody')
    d = tbody.find_all('tr')

    #iterating for every prof
    for i in d:
        td1 = i.find('td', {'class':'title'})
        a = td1.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        last_name = (td1.find_next('td')).get_text()
        name = name+" "+last_name
        link = a.get('href')
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link)        
        except:
            continue

        td4 = (((td1.find_next('td')).find_next('td')).find_next('td'))
        a_mail = td4.find('a')
        if a_mail != None:
            email = a_mail.get('href')
            email = email[7:]
        else:
            email = "Not Found"

        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)

    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_sheffield():
    url = "https://www.sheffield.ac.uk/dcs/people/academic"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of Sheffield"
    country = "UK"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('main', {'class':'large-12 columns'})
    d = dd.find_all('div', {'class':'summary-text'})

    #iterating for every prof
    for i in d:
        a = (i.find('h3')).find('a')
        if a == None:
            continue
        name = (a.get_text())
        name = ' '.join(name.split())
        # name = name.replace("  ", " ")
        # name = name.replace("\t", "")
        # name = name.replace("\n", "")
        # name = name.strip()
        link = 'https://www.sheffield.ac.uk' +a.get('href')
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link)        
        except:
            continue

        strong = i.find('strong')
        if strong != None:
            a_mail = strong.find('a')
            email = a_mail.get('href')
            email = email[7:]
        else:
            email = "Not Found"

        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)

    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_north_carolina():
    url = "https://cs.unc.edu/people-page/faculty/"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of North Carolina"
    country = "USA"

    grabage_emails = ['info@cs.unc.edu']

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    
    dd = soup.find('main', {'class':'main col-sm-12'})
    d = dd.find_all('div', {'class':'uncperson'})

    #iterating for every prof
    for i in d:
        h3 = i.find('h3')
        a = h3.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        link = a.get('href')
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link)        
        except:
            continue

        email = "Not Found"

        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)

    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def lund_university():
    url = "https://www.lunduniversity.lu.se/lucat/group/v1000234"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Lund University"
    country = "Sweden"

    grabage_emails = ['expedition@cs.lth.se']

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    
    dd = soup.find('div', {'class':'lucat-user-list mt-7 mb-7'})
    d = dd.find_all('li', {'class':'border-bottom mb-3 pb-3'})

    #iterating for every prof
    for i in d:
        h4 = i.find('h4')
        a = h4.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        link = 'https://www.lunduniversity.lu.se' +a.get('href')
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link)        
        except:
            continue

        prof_soup = BeautifulSoup(prof_resp.text, "html.parser")

        #getting prof personal homepage from desc page
        prof_span = prof_soup.find('span', text=' Personal website:')
        if prof_span == None:
            continue
        a_prof = prof_span.find_next('a') 
        link = a_prof.get('href')

        try:    
            prof_resp = requests.get(link)        
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)

    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def kth_sweden():
    url = "https://www.kth.se/cs/contact/we-work-at-the-department-of-computer-science-1.1028302"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "KTH Royal Institute"
    country = "Sweden"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    
    dd = soup.find('div', {'class':'paragraphs'})
    d = (dd.find('tbody')).find_all('tr')

    #iterating for every prof
    for i in d:
        a = (i.find('td', {'class':'firstname'})).find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        lname = (i.find('td', {'class':'lastname'})).get_text()
        name = name+" "+lname
        link = a.get('href')
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link)        
        except:
            continue

        title = (i.find('td', {'class':'title'})).get_text()
        if ('STUDENT' in title) or ('POSTDOC' in title):
            continue

        email = (i.find('td', {'class':'email'})).get_text()

        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)

    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_nottingham():
    url = "https://www.nottingham.ac.uk/computerscience/people/index.aspx"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of Nottingham"
    country = "UK"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    
    dd = soup.find('div', {'id':['lookup-academic', 'lookup-research']})
    d = dd.find_all('tr')

    #iterating for every prof
    for i in d:
        td1 = i.find('td')
        if td1 == None:
            continue

        a = td1.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        name = name.split(',')
        name = name[1]+" "+name[0]
        link = 'https://www.nottingham.ac.uk/computerscience/people/' +a.get('href')
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link)        
        except:
            continue

        a_mail = (i.find('td', {'class':"sys_email"})).find('a')
        if a_mail != None:
            email = a_mail.get('href')
            email = email[7:]
        else:
            email = "Not Found"
    
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)

    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def penn_state():
    url = "https://www.eecs.psu.edu/research-areas/computer-architecture.aspx"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Pennsylvania State University"
    country = "USA"

    grabage_emails = ['webmaster@engr.psu.edu']

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':"adjust_right_margin"})
    d = dd.find_all('li')


    #iterating for every prof
    for i in d:
        a = i.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        link = a.get('href')

        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link)        
        except:
            continue

        email = "Not Found"
    
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)

    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def trinity_college_dublin():
    url = "https://www.scss.tcd.ie/personnel/Academic_Staff_personnel.php"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Trinity College Dublin"
    country = "Ireland"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':'tier-main-temporary tier-main-temporary-padding'})
    d = dd.find_all('dl', {'class':"list-associated"})

    #iterating for every prof
    for i in d:
        h2 = i.find_previous('h2')
        name = h2.get_text()
        
        dt_a = i.find('dt', text="College Profile")
        if dt_a == None:
            continue

        a = (dt_a.find_next('dd')).find('a')
        if a == None:
            continue
        link = 'https://www.scss.tcd.ie/personnel/' +a.get('href')

        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link)        
        except:
            continue

        dt_mail = i.find('dt', text="E-mail")
        dd_mail = dt_mail.find_next('dd')
        if dd_mail != None:
            email = dd_mail.get_text()
            email = email.replace(" at ", "@")
        else:
            email = "Not Found"
    
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)

    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def tud_denmark():
    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Technical University Denmark"
    country = "Denmark"

    for x in range(0,9):
        num = x 
        url = "https://orbit.dtu.dk/en/organisations/department-of-applied-mathematics-and-computer-science/persons/?page="+str(num)   # homepage url
        r = requests.get(url)                                        # request to url

        # getting the soup by parsing the html parsel to text to request r
        soup = BeautifulSoup(r.text, "html.parser")
        # print(soup.prettify)

        grabage_emails = []

        var = [csvwriter, u_name, country]

        # d gives the array of all profs on the dept homepage
        dd = soup.find('ul', {'class':'grid-results'})
        d = soup.find_all('div', {'class':"result-container"})

        #iterating for every prof
        for i in d:
            a = (i.find('h3', {'class':"title"})).find('a')
            if a == None:
                continue
            name = (a.get_text()).strip()
            link = a.get('href')

            filter_div = i.find('span', {'class':'minor dimmed'})
            if filter_div != None:
                check = filter_div.get_text()
            else:
                check = []
            #filter
            if ("Student" in check) or ("Postdoc" in check) or ("student" in check):
                continue

            try:    
                prof_resp = requests.get(link)        
            except:
                continue

            li_mail = i.find('li', {'class':"email"})
            if li_mail != None:
                a_mail = li_mail.find('a')
                email = a_mail.get_text()
                # email = email[7:]
            else:
                email = "Not Found"
        
            print(u_name, name, link)
            filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)

    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_helsinki():
    url = "https://www2.helsinki.fi/en/faculty-of-science/research-and-teaching-staff-computer-science"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of Helsinki"
    country = "Finland"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':'textarea'})
    d = dd.find_all('div', {'class':"expert-atom__content"})

    #iterating for every prof
    for i in d:
        a = i.find('a', {'class':' expert-atom__name-container'})
        if a == None:
            continue
        name = ((a.get_text()).strip())
        name = " ".join(name.split())
        name = name.replace('\n', "")

        link = 'https://www2.helsinki.fi' +a.get('href')

        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link)        
        except:
            continue

        a_mail = i.find('div', {'class':'expert-atom-contact-details__item expert-atom-contact-details__item__mail icon--mail'})
        if a_mail != None:
            email = a_mail.get_text()
        else:
            email = "Not Found"
    
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)

    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def washington_uni_sl():
    url = "https://cse.wustl.edu/faculty-research/directory.html"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Washington University St. Louis"
    country = "USA"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':'faculty-directory__list-group directory_group'})
    d = dd.find_all('article')

    #iterating for every prof
    for i in d:
        h3 = i.find('h3', {'class':'faculty-directory__teaser-name'})
        name = h3.get_text()

        a = i.find('a')
        if a == None:
            continue
        link = a.get('href')

        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link)        
        except:
            continue

            
        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)

    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_geneva():
    url = "https://www.unige.ch/dinfo/en/staff/"
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of Geneva"
    country = "Switzerland"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':'c-Collection-content'})
    dd = dd.find_next('div', {'class':'c-Collection-content'})
    d = dd.find_all('li', {'class':'c-Collection-item'})

    #iterating for every prof
    for i in d:
        a = i.find('a', {'class':'c-Collection-itemTitle'})
        if a == None:
            continue

        name = a.get_text()
        name = ' '.join(name.split())
        a = i.find('a')
        link = 'https://www.unige.ch' +a.get('href')

        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link)        
        except:
            continue

            
        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)

    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def ohio_state_university():
    url = "https://cse.osu.edu/research/computer-architecture"
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Ohio State University"
    country = "USA"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':'coe-widget-content-grid-items'})
    d = dd.find_all('article')

    #iterating for every prof
    for i in d:
        h2 = i.find('h2', {'class':'directory-grid-name'})
        if h2 == None:
            continue
        name = h2.get_text()
        name = name.split(" ")
        name = name[1]+" "+name[0]

        a = i.find('a', {'class':'grid-item-link'})
        if a == None:
            continue
        link = 'https://cse.osu.edu' +a.get('href')

        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link)        
        except:
            continue

        a_mail = i.find('div', {'class':'directory-grid-email'})
        if a_mail != None:
            email =  a_mail.get_text()
        else:
           email = "Not Found"
    
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def perdue_uni():
    url = "https://www.cs.purdue.edu/people/faculty/index.html"
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Perdue University"
    country = "USA"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':'maincontent col-lg-9 col-md-9 col-sm-9 col-xs-12 '})
    d = dd.find_all('tr')

    #iterating for every prof
    for i in d:
        td1 = i.find('td')
        if td1 == None:
            continue
        name = td1.get_text()

        a = i.find('a', text='Bio')
        if a == None:
            continue
        link = 'https://www.cs.purdue.edu/people/faculty/' +a.get('href')

        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link)        
        except:
            continue

        email = "Not Found"    
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def boston_uni():
    url = "https://www.bu.edu/cs/people/faculty/"
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Boston University"
    country = "USA"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':'content-container'})
    d = dd.find_all('li', {'class':'has-title'})

    #iterating for every prof
    for i in d:
        a = i.find('a')
        if a == None:
            continue
        link = a.get('href')

        p = i.find('p', {'class':"profile-name"})
        if p == None:
            continue
        name = p.get_text()

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link)        
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def nagoya_uni():
    url = "https://www.i.nagoya-u.ac.jp/en/prof/study_a06/"
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Nagoya University"
    country = "Japan"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('table', {'class':'tablepress tablepress-id-48'})
    d = dd.find_all('tr')

    #iterating for every prof
    for i in d:
        td = i.find('td', {'class':"column-1"})
        if td == None:
            continue
        name = td.get_text()
        
        a = i.find('td', {'class':"column-6"})
        if a == None:
            continue
        link = a.get_text()

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link)        
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uc_davis():
    url = "https://cs.ucdavis.edu/faculty-research/architecture"
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of California, Davis"
    country = "USA"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':'view-content'})
    d = dd.find_all('div', {'class':'o-media__body'})

    #iterating for every prof
    for i in d:
        a = i.find('a')
        if a == None:
            continue
        link = 'https://cs.ucdavis.edu'+a.get('href')
        name = a.get_text()

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link)        
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_oslo():
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of Oslo"
    country = "Norway"

    for x in range(1,4):

        url = "https://www.mn.uio.no/ifi/english/people/aca/?page="+str(x)+"&u-page="+str(x)
        r = requests.get(url)                                        # request to url

        # getting the soup by parsing the html parsel to text to request r
        soup = BeautifulSoup(r.text, "html5lib")
        # print(soup.prettify)

        grabage_emails = []

        var = [csvwriter, u_name, country]

        # d gives the array of all profs on the dept homepage
        dd = soup.find('div', {'class':'vrtx-person-search-hits'})
        d = dd.find_all('tr')

        #iterating for every prof
        for i in d:
            td = i.find('td', {'class':"vrtx-person-listing-name"})
            if td == None:
                continue
            text = td.get_text()
            if ('student' in text) or ('Student' in text) or ('fellow' in text):
                continue

            a = td.find_all('a')
            if a == None:
                continue
            elif len(a) == 2:
                aa = a[1]
            else:
                aa = a[0]
            link = aa.get('href')
            name = aa.get_text()
            # print("NAME: ", name)
            name = name.split(',')
            name = name[1]+" "+name[0]

            # print(u_name, name, link)
            # check if link is valid on Not
            try:    
                prof_resp = requests.get(link)        
            except:
                continue

            td_mail = i.find('td', {'class':"vrtx-person-listing-email"})
            a_mail = td_mail.find('a')
            if a_mail != None:
                email = a_mail.get_text()
            else:
                email = "Not Found"
    
            print(u_name, name, link)
            filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def queen_mary():
    url = "http://eecs.qmul.ac.uk/people/academic/"
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Queen Mary University of London"
    country = "UK"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':'profiles two-column-profiles cd-gallery'})
    d = dd.find_all('div', {'class':'staff-info'})

    #iterating for every prof
    for i in d:
        a = i.find('a')
        if a == None:
            continue
        link = a.get('href')
        name = a.get_text()

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link)        
        except:
            continue


        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_bern():
    url = "https://www.inf.unibe.ch/about_us/team/index_eng.html"
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of Bern"
    country = "Switzerland"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':'col-lg-6 col-lg-offset-0 col-md-11 col-md-offset-1'})
    d = dd.find_all('article', {'class':'team-box'})

    #iterating for every prof
    for i in d:
        a = i.find('a')
        if a == None:
            continue
        link = a.get('href')
        name = a.get_text()

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link)        
        except:
            continue


        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_berlin():
    url = "https://www.informatik.hu-berlin.de/de/org/mitarbeiter"
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of Berlin"
    country = "Germany"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('dl', {'class':'letterDL'})
    d = dd.find_all('dd', {'class':'view_content'})

    #iterating for every prof
    for i in d:
        a = i.find('a')
        if a == None:
            continue
        link = a.get('href')
        name = a.get_text()

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link)
        except:
            continue

        # get prof homepage from dept profile page
        prof_soup = BeautifulSoup(prof_resp.text, "html.parser")
        a = prof_soup.find('a',{'class':'url'})
        if a == None:
            continue

        link =  a.get('href')
        try:    
            prof_resp = requests.get(link)
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_montreal():
    url = "https://diro.umontreal.ca/english/departement-directory/professors/"
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of Montreal"
    country = "Canada"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':'list_individus'})
    d = dd.find_all('div', {'class':'individu with-affiliations with-expertises'})

    #iterating for every prof
    for i in d:
        h4 = i.find('h4', {'class':"nom-prenom"})
        a = h4.find('a')
        if a == None:
            continue
        link = "https://diro.umontreal.ca"+a.get('href')
        name = (a.get_text()).strip()
        name = " ".join(name.split())

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link)        
        except:
            continue

        div_mail = i.find('div', {'class':'courriel'})
        a_mail = div_mail.find('a')
        if a_mail != None:
            email = a_mail.get_text()
        else:
            email = "Not Found"
    
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_alberta():
    url = "https://webapps.cs.ualberta.ca/directory/directory.php?group=Faculty"
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of Alberta"
    country = "Canada"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':'col_main'})
    d = dd.find_all('div', {'class':'dirbox'})

    #iterating for every prof
    for i in d:
        h2 = i.find('h2')
        a = h2.find('a')
        if a == None:
            continue
        link = a.get('href')
        name = (a.get_text()).strip()
        name = " ".join(name.split())

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link)        
        except:
            continue

        span_mail = i.find('span', text="Email:")
        a_mail = span_mail.find_next('a')
        if a_mail != None:
            email = a_mail.get_text()
        else:
            email = "Not Found"
    
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def pontificia_uni():
    url = "https://dcc.uc.cl/people"
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Pontificia University"
    country = "Chile"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':'page-wrapper'})
    d = dd.find_all('div', {'class':'clearfix'})

    #iterating for every prof
    for i in d:
        a_div = i.find('div', {"class":"s-component-content"})
        a = a_div.find('a')
        if a == None:
            continue
        link = a.get('href')
    
        name_div = i.find('div', {"class":"s-item-title"})
        name = (name_div.get_text()).strip()
        name = " ".join(name.split())

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link)        
        except:
            continue

        mail_div = i.find('div', {"class":"s-item-text"})
        a_mail = mail_div.find('a')
        if a_mail != None:
            email = a_mail.get_text()
        else:
            email = "Not Found"
    
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_southern_cal():
    url = "https://www.cs.usc.edu/directory/faculty/"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of Southern California"
    country = "USA"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':'resultsModule'})
    d = dd.find_all('div', {'class':'faculty-text'})

    #iterating for every prof
    for i in d:
        a = i.find('a')
        if a == None:
            continue
        link = "https://www.cs.usc.edu"+a.get('href')
        name = (a.get_text()).strip()
        name = " ".join(name.split())

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers) 
            prof_soup = BeautifulSoup(prof_resp.text, "html.parser")    
        except:
            continue

        mail_div = i.find('div')
        a_mail = mail_div.find('a')
        if a_mail != None:
            email = a_mail.get_text()
        else:
            email = "Not Found"

    
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def utretch_uni():
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    
    url = "https://www.uu.nl/en/research/intelligent-software-systems"
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of Southern California"
    country = "USA"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('ul', {'class':'grid grid--2'})
    d = dd.find_all('div', {'class':'profile__main'})

    #iterating for every prof
    for i in d:
        a = i.find('a')
        if a == None:
            continue
        link = a.get('href')
        name = (a.get_text()).strip()
        name = " ".join(name.split())

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link)        
        except:
            continue

        mail_div = i.find('div', {'class':"profile__email"})
        a_mail = mail_div.find('a')
        if a_mail != None:
            email = a_mail.get_text()
        else:
            email = "Not Found"
    
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def kyusu_uni():
    url = "https://www.eecs.kyushu-u.ac.jp/e/staff.html"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Kyusu University"
    country = "Japan"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':'flex2'})
    d = dd.find_all('a')

    #iterating for every prof
    for i in d:
        a = i
        if a == None:
            continue
        link = a.get('href')
        name = (a.get_text()).strip()
        name = " ".join(name.split())

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers) 
            prof_soup = BeautifulSoup(prof_resp.text, "html.parser")    
        except:
            continue


        email = "Not Found"    
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uppsala_uni():
    url = "http://www.it.uu.se/katalog/byjobgroup?wiki_nocache=true&division="
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Uppsala University"
    country = "Sweden"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('table', {'class':'wiki'})
    d = dd.find_all('tr')

    #iterating for every prof
    for i in d:
        a = i.find('a', {'class':'nametag'})
        if a == None:
            continue
        link = "http://www.it.uu.se"+a.get('href')
        name = (a.get_text()).strip()
        if name == 'Ahani, Ghafour':
            break
        name = name.split(",")
        name = name[1]+" "+name[0]
        name = " ".join(name.split())

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers) 
        except:
            continue

        a_mail = i.find('a', alt="Email")
        if a_mail != None:
            email = a_mail.get('href')
            email = email[7:]
        else:
            email = "Not Found"    
    
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def aalto_uni():
    url = "https://www.aalto.fi/en/department-of-computer-science/faculty"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Aalto University"
    country = "Finland"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':'aalto-table-wrapper'})
    d = dd.find_all('td')

    #iterating for every prof
    for i in d:
        a = i.find('a')
        if a == None:
            continue
        link = "https://www.aalto.fi"+a.get('href')
        name = (a.get_text()).strip()
        name = " ".join(name.split())

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers) 
            prof_soup = BeautifulSoup(prof_resp.text, "html.parser")    
        except:
            continue


        email = "Not Found"    
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def leiden_uni():
    url = "https://www.universiteitleiden.nl/en/science/computer-science/staff?_ga=2.53055201.852038052.1618384824-1207103337.1618384824#tab-2"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Leiden University"
    country = "Netherland"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('section', {'data-tab-label':"Academic Staff"})
    d = dd.find_all('li')
    # print(d)
    print(len(d))
    #iterating for every prof
    for i in d:
        # print(i)
        a = i.find('a')
        if a == None:
            continue
        link = "https://www.universiteitleiden.nl"+a.get('href')
        aa = i.find('strong')
        name = (aa.get_text()).strip()
        name = " ".join(name.split())

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue


        email = "Not Found"    
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_grogingen():
    url = "https://www.rug.nl/about-ug/how-to-find-us/find-an-expert?discipline=Computer+Science%2C+Hardware+%26+Architecture"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of Grogingen"
    country = "Netherlands"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':"rug-background-alternating--inverse"})
    d = dd.find_all('div', {'class':'rug-pv-s rug-ph-xs'})
    # print(len(d))

    #iterating for every prof
    for i in d:
        a_div = i.find('div', {'class':'rug-h3'})
        a = a_div.find('a')
        if a == None:
            continue
        link = "https://www.rug.nl"+a.get('href')
        name = (a.get_text()).strip()
        name = " ".join(name.split())

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        a_mail = i.find('span', {'class':"js--decode"})
        if a_mail != None:
            email = a_mail.get_text()
            email = email.replace(" ", "@")
        else:
            email = "Not Found"

        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)



    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def free_uni_germany():
    url = "https://www.mi.fu-berlin.de/en/inf/index.html"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Free University of Berlin"
    country = "Germany"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    d = soup.find_all('div', {'class':"box-carousel-text-wrapper-half"})
    # d = dd.find_all('li')
    # print(d)

    #iterating for every prof
    for i in d:
        # print(i)
        a = i.find('h2', {'class':"box-carousel-title"})
        if a == None:
            continue
        name = (a.get_text()).strip()
        name = " ".join(name.split())
        
        a = i.find('a', href=True)
        if a == None:
            continue
        link = "https://www.mi.fu-berlin.de"+a.get('href')

        print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue


        email = "Not Found"    
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_putra_malaysia():
    url = "https://eng.upm.edu.my/department/department_of_computer_and_communication_systems_engineering/academic_staff-1897"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University Putra Malaysia"
    country = "Malaysia"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':"L3-container"})
    d = dd.find_all('tr')

    #iterating for every prof
    for i in d:
        td = i.find('td')
        td2 = td.find_next('td')
        if td2 == None:
            continue
        a = td2.find('a')
        if a == None:
            continue
        link = a.get('href')
        name = (a.get_text()).strip()
        name = " ".join(name.split())

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        text = td2.get_text()
        if text == "":
            continue
        email = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}", text)
        if len(email) == 0:
            email = "Not Found"
        else:
            email = email[0]
            l = len(email)
            # print(email[l-2:])
            if email[l-2:] == 'OR':
                email = email[0:l-2]

        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_tech_sydney():
    url = "https://www.uts.edu.au/about/faculty-engineering-and-information-technology/computer-science/school-computer-science-staff"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of Technology, Sydney"
    country = "Australia"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('table', {'class':"staff-list"})
    d = dd.find_all('tr')

    #iterating for every prof
    for i in d:
        td = i.find('td', {'class':'table--cell-width-l'})
        if td == None:
            continue 
        a = td.find('a')
        if a == None:
            continue
        link = "https://www.uts.edu.au"+a.get('href')
        name = (a.get_text()).strip()
        name = " ".join(name.split())
        name = name.split(',')
        name = name[1]+' '+name[0]

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        email = "Not Found"

        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def lancaster_uni():
    url = "https://www.lancaster.ac.uk/scc/about-us/people/"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Lancaster University"
    country = "UK"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':"grid-container staff-list hidden"})
    d = dd.find_all('div', {'class':'feature-title'})

    #iterating for every prof
    for i in d:
        a = i.find('a')
        if a == None:
            continue
        link = "https://www.lancaster.ac.uk"+a.get('href')

        h3 = i.find('h3', {'class':'name'})
        name = (h3.get_text()).strip()
        name = " ".join(name.split())

        span = i.find('span', {'class':'job-title'})
        text = span.get_text()
        if 'student' in text or "Student" in text:
            continue

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        email = "Not Found"

        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_ghent():
    url = "https://telefoonboek.ugent.be/en/faculties/we02"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of Ghent"
    country = "Belgium"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':"content-list no-border mbottom-default"})
    d = dd.find_all('div', {'class':'col-sm-4'})

    #iterating for every prof
    for i in d:
        a = i.find('a')
        if a == None:
            continue
        link = a.get('href')
        if link[0:3] == 'mail' or link[0:2] == 'tel':
            continue
        name = (a.get_text()).strip()
        name = " ".join(name.split())

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        email = "Not Found"

        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_centrale():
    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of Centrale"
    country = "France"

    grabage_emails = []

    ar = ["a","b","c","d","e","f","g","h","i","j",'k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

    for x in ar:
        url = "https://www.lri.fr/annuaire_en.php?alpha="+x
        print(url)
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        r = requests.get(url, headers=headers)

        # getting the soup by parsing the html parsel to text to request r
        soup = BeautifulSoup(r.text, "html5lib")
        # print(soup.prettify)


        var = [csvwriter, u_name, country]

        # d gives the array of all profs on the dept homepage
        dd = soup.find('table', {'class':"tabtext"})
        d = dd.find_all('td', {'width':'155'})

        #iterating for every prof
        for i in d:
            a = i.find('a')
            if a == None:
                continue
            link = 'https://www.lri.fr/annuaire_en.php/'+a.get('href')

            if link[0:3] == 'mail' or link[0:2] == 'tel':
                continue
            name = (a.get_text()).strip()
            name = " ".join(name.split())

            # print(u_name, name, link)
            # check if link is valid on Not
            try:    
                prof_resp = requests.get(link, headers=headers)   
            except:
                continue

            email = "Not Found"

            print(u_name, name, link)
            filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def chalmers_uni():
    url = "https://www.chalmers.se/en/departments/cse/organisation/ce/Pages/Staff.aspx"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Chalmers University of Technology"
    country = "Sweden"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('ul', {'class':"employee-list"})
    d = dd.find_all('li')

    #iterating for every prof
    for i in d:
        a = i.find('a')
        if a == None:
            continue
        link = 'https://www.chalmers.se'+a.get('href')
        if link[0:3] == 'mail' or link[0:2] == 'tel':
            continue
        div_name = i.find('div', {'class':'header'})
        name = (div_name.get_text()).strip()
        name = " ".join(name.split())

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        email = "Not Found"

        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def hokkaido_uni():
    url = "https://www.ist.hokudai.ac.jp/eng/staff/"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of Ghent"
    country = "Belgium"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':"content-block staff-list"})
    d = dd.find_all('tr', {'class':['gr', 'lgr']})

    #iterating for every prof
    for i in d:
        a = i.find('a')
        if a == None:
            continue
        link = "https://www.ist.hokudai.ac.jp/eng/staff/"+a.get('href')
        name = (a.get_text()).strip()
        name = " ".join(name.split())

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        email = "Not Found"

        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def usm_malaysia():
    url = "https://cs.usm.my/index.php/about/our-people/facultycs-member"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "USM Malaysia"
    country = "Malaysia"

    grabage_emails = ['cs@usm.my']

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':"tm-article-content"})
    d = dd.find_all('p')

    #iterating for every prof
    for i in d:
        a = i.find('a')
        if a == None:
            continue
        link = a.get('href')
        if link == None or link[0] == '#':
            continue
        link = "https://cs.usm.my" + link
        name = (a.get_text()).strip()
        name = " ".join(name.split())

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        email = "Not Found"

        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def king_abdulaziz_uni():
    url = "https://cs.usm.my/index.php/about/our-people/facultycs-member"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "King Abdulaziz University"
    country = "Saudi Arabia"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':"tm-article-content"})
    d = dd.find_all('p')

    #iterating for every prof
    for i in d:
        a = i.find('a')
        if a == None:
            continue
        link = a.get('href')
        if link == None or link[0] == '#':
            continue
        link = "https://cs.usm.my" + link
        name = (a.get_text()).strip()
        name = " ".join(name.split())

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        email = "Not Found"

        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def mcmaster_uni():
    url = "https://www.eng.mcmaster.ca/cas/people/faculty"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "McMaster University"
    country = "Canada"

    grabage_emails = ['cs@usm.my']

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':"row equal-row no-space text-center"})
    d = dd.find_all('h3', {'class':'card-title'})

    #iterating for every prof
    for i in d:
        a = i.find('a')
        if a == None:
            continue
        link = a.get('href')
        if link == None or link[0] == '#':
            continue
        link = "https://www.eng.mcmaster.ca" + link
        name = (a.get_text()).strip()
        name = " ".join(name.split())

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)
            prof_soup = BeautifulSoup(prof_resp.text, "html.parser")
        except:
            continue

        a2 = prof_soup.find('a', text='&ensp;Visit Personal Website')
        if a2 != None:
            link = a2.get('href')

        try:    
            prof_resp = requests.get(link, headers=headers)
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def rwth_uni():
    url = "https://www.informatik.rwth-aachen.de/cms/Informatik/Forschung/Forschungsbereiche/~mrys/Liste-der-Forschungsbereiche/lidx/1/"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "RWTH University"
    country = "Germany"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':"text"})
    d = dd.find_all('tr')

    #iterating for every prof
    for i in d:
        td1 = i.find('td')
        td2 = td1.find_next('td')
        a = td2.find('a')
        if a == None:
            continue
        link = a.get('href')
        if link[0:3] == 'mail' or link[0:2] == 'tel':
            continue
        link = "https://www.informatik.rwth-aachen.de" + link
        name = (a.get_text()).strip()
        name = " ".join(name.split())

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def hanyang_uni():
    url = "http://cse.hanyang.ac.kr/eng/department/member.php"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Hanyang University"
    country = "South Korea"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':"photo_table"})
    d = dd.find_all('table')

    #iterating for every prof
    for i in d:
        a = i.find('a')
        if a == None:
            continue

        a2 = a.find_next('a')
        if a2 == None:
            continue    
        link = a2.get('href')

        td = i.find('td', {'class':"or_name"})
        name = (td.get_text()).strip()
        name = " ".join(name.split())

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def aarhus_uni():
    url = "https://cs.au.dk/contact/people/"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Aarhus University"
    country = "Denmark"

    grabage_emails = ['cs@au.dk']

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'id':["c29122", 'c30449']})
    d = dd.find_all('tr')

    #iterating for every prof
    for i in d:
        td = i.find('td')
        if td == None:
            continue
        a = td.find('a')
        if a == None:
            continue
        link = a.get('href')
        if link == None or link[0] == '#':
            continue
        name = (a.get_text()).strip()
        name = " ".join(name.split())

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)
            prof_soup = BeautifulSoup(prof_resp.text, "html.parser")
        except:
            continue

        a2 = prof_soup.find('a', text='&ensp;Visit Personal Website')
        if a2 != None:
            link = a2.get('href')

        try:    
            prof_resp = requests.get(link, headers=headers)
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def tech_uni_berlin():
    url = "https://www.eecs.tu-berlin.de/menue/faculty_institutions/professorships/professorschairs/parameter/en/"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Technical University Berlin"
    country = "Germany"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'id':'main'})
    d = dd.find_all('td')

    #iterating for every prof
    for i in d:
        a = i.find('a')
        if a == None:
            continue
        link = a.get('href')
        name = (a.get_text()).strip()
        name = " ".join(name.split())

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_basel():
    url = "https://dmi.unibas.ch/en/department/people/computer-science/"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of Basel"
    country = "Switzerland"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'id':['c4877', 'c4879']})
    d = dd.find_all('tr', {'class':'item'})

    #iterating for every prof
    for i in d:
        td1 = i.find('td')
        a = td1.find('a')
        if a == None:
            continue
        link = a.get('href')
        if link[0] == '/':
            link = 'https://dmi.unibas.ch'+link

        td2 = td1.find_next('td')
        lname = td2.get_text()
        fname = (td2.find_next('td')).get_text()
        name = fname +" "+lname

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)
            prof_soup = BeautifulSoup(prof_resp.text, "html.parser")
        except:
            continue

        a2 = prof_soup.find('a', text='&ensp;Visit Personal Website')
        if a2 != None:
            link = a2.get('href')

        try:    
            prof_resp = requests.get(link, headers=headers)
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_york():
    url = "https://www.cs.york.ac.uk/people/"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of York"
    country = "UK"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('table', {'class':"searchbox"})
    d = dd.find_all('tr')
    # print(len(d))

    #iterating for every prof
    for i in d:
        a_div = i.find('td', {'class':'white'})
        if a_div==None:
            continue
        a = a_div.find('a')
        link = "https://www.cs.york.ac.uk/people/"+a.get('href')
        name = (a.get_text()).strip()
        name = " ".join(name.split())

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue


        email = "Not Found"

        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)



    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def newcastle_uni():
    url = "https://www.ncl.ac.uk/computing/staff/academic/"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Newcastle University"
    country = "UK"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':"relatedPeopleList"})
    d = dd.find_all('div', {'class':"relatedPerson"})
    # print(len(d))

    #iterating for every prof
    for i in d:
        a = i.find('a')
        if a == None:
            continue
        link = "https://www.ncl.ac.uk"+a.get('href')
        h4 = a.find('h4')
        if h4 == None:
            continue
        name = (h4.get_text()).strip()
        name = " ".join(name.split())

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        a_mail = i.find('a', {"class":'relatedPersonLink relatedPersonLinkMail'})
        if a_mail != None:
            email = a_mail.get('href')
            email = email[7:]
        else:
            email = "Not Found"

        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)



    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uc_santa_barbara():
    url = "https://www.cs.ucsb.edu/people"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of California, Santa Barbara"
    country = "USA"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('table', {'class':"views-table cols-6"})
    d = dd.find_all('tr')
    # print(len(d))

    #iterating for every prof
    for i in d:
        td = i.find('td', {'class':'views-field views-field-title'})
        if td == None:
            continue
        a = td.find('a')
        if a == None:
            continue
        link = "https://www.cs.ucsb.edu"+a.get('href')
        name = (a.get_text()).strip()
        name = " ".join(name.split())

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        a_mail = i.find('td', {'class':'views-field views-field-field-email'})
        if a_mail != None:
            email = a_mail.get_text()
            email = email.strip()
        else:
            email = "Not Found"

        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)



    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_maryland():
    url = "https://www.cs.umd.edu/people/faculty"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of Maryland"
    country = "USA"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':"region region-content"})
    d = dd.find_all('div', {'class':"media-body"})
    print(len(d))

    #iterating for every prof
    for i in d:
        a = i.find('a')
        if a == None:
            continue
        link = "https://www.cs.umd.edu"+a.get('href')
        name = (a.get_text()).strip()
        name = " ".join(name.split())

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        email = "Not Found"

        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)



    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_pittsburgh():
    url = "https://www.cs.pitt.edu/people"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of Pittsburgh"
    country = "USA"

    grabage_emails = ['computer.science@pitt.edu']

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':"region region-content"})
    d = dd.find_all('div', {'class':"field-content"})
    # print(len(d))

    #iterating for every prof
    for i in d:
        a_name = i.find('div', {'class':"views-field views-field-title"})
        if a_name == None:
            continue
        name = (a_name.get_text()).strip()
        name = " ".join(name.split())

        a = i.find('a')
        if a == None:
            continue
        link = "https://www.cs.pitt.edu"+a.get('href')

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        email = "Not Found"

        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)



    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def michigan_state():
    url = "https://www.cse.msu.edu/People/"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Michigan State University"
    country = "USA"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('table', {'class':"profiles-table"})
    d = dd.find_all('tr')
    # print(len(d))

    #iterating for every prof
    for i in d:
        td = i.find('td')
        if td == None:
            continue
        a = (td.find_next('td')).find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        name = " ".join(name.split())
        link = a.get('href')

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        email = "Not Found"

        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)



    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def emory_university():
    url = "https://www.cs.emory.edu/people/faculty/"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Emory University"
    country = "USA"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':"span9"})
    d = dd.find_all('tr')
    # print(len(d))

    #iterating for every prof
    for i in d:
        td = i.find('td')
        if td == None:
            continue
        a = td.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        name = " ".join(name.split())
        link = "https://www.cs.emory.edu/people/faculty/"+a.get('href')

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        email = "Not Found"

        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)



    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def cardiff_university():
    url = "https://www.cardiff.ac.uk/computer-science/people/academic-and-research-staff"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Cardiff University"
    country = "UK"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'id':"new_content_container_119293_119293"})
    d = dd.find_all('div', {'class':'profile profile-student with-image vcard'})
    # print(len(d))

    #iterating for every prof
    for i in d:
        h2 = i.find('h2', {'class':'profile-title fn'})
        if h2 == None:
            continue
        a = h2.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        name = " ".join(name.split())
        link = a.get('href')

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        email = "Not Found"

        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)



    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def ens_lyon():
    url = "http://informatique.ens-lyon.fr/en/team/faculty"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "ENS lyon"
    country = "France"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('table', {'class':"table table-striped table-bordered table-hover table-condensed cols-4 views-view-table"})
    d = dd.find_all('tr')
    # print(len(d))

    #iterating for every prof
    for i in d:
        td = i.find('td', {'class':'col-sm-3 views-field views-field-title is-active'})
        if td == None:
            continue
        a = td.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        name = " ".join(name.split())
        link = "http://informatique.ens-lyon.fr"+a.get('href')

        # print(link)
        # check if link is valid or Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        # prof_resp = requests.get(link, headers=headers)
        email = "Not Found"

        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)



    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def case_western():
    url = "https://engineering.case.edu/computer-and-data-sciences/faculty-and-staff"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Case Western Reserve University"
    country = "USA"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':"content l--constrained-padded"})
    d = dd.find_all('div', {'class':'person--content'})
    # print(len(d))

    #iterating for every prof
    for i in d:
        h2 = i.find('h2', {'class':'person--name teaser--title'})
        if h2 == None:
            continue
        a = h2.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        name = " ".join(name.split())
        link = "https://engineering.case.edu"+a.get('href')

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        email = "Not Found"

        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)



    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_florida():
    url = "https://www.cise.ufl.edu/people/faculty/"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of Florida"
    country = "USA"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':"entry-content"})
    d = dd.find_all('div', {'class':'wp-show-posts-inner'})
    # print(len(d))

    #iterating for every prof
    for i in d:
        h2 = i.find('p', {'class':'wp-show-posts-entry-title'})
        if h2 == None:
            continue
        a = h2.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        name = " ".join(name.split())
        link = a.get('href')

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        a_mail = i.find('div', {'class':'wp-show-posts-entry-summary'})
        a = a_mail.find('a')
        if a != None:
            email = a.get('href')
            email = email[7:]
        else:
            email = "Not Found"

        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)



    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_exeter():
    url = "http://emps.exeter.ac.uk/computer-science/staff/#academic"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of Exeter"
    country = "UK"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('table', {'class':"profile_list"})
    d = dd.find_all('tr')
    # print(len(d))

    #iterating for every prof
    for i in d:
        a = i.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        name = " ".join(name.split())
        link = "http://emps.exeter.ac.uk"+a.get('href')

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue


        email = "Not Found"

        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)



    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_rochester():
    url = "https://www.cs.rochester.edu/people/index.html"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of Rochester"
    country = "USA"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':"columns small-12 medium-9 medium-push-3 section--thin content"})
    d = dd.find_all('div', {"class":'row margin--thin'})
    # print(len(d))

    #iterating for every prof
    for i in d:
        h4 = i.find('h4')
        if h4 == None:
            continue
        a = h4.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        name = " ".join(name.split())
        a2 = i.find('a', text='Website')
        if a2 == None:
            link = a.get('href')
        else:
            link = a2.get('href')

        text = (i.find('li', {'class':'lead'})).get_text()
        if 'Student' in text:
            continue
        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        email = "Not Found"

        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)



    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_waterloo():
    url = "https://cs.uwaterloo.ca/about/people"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of Waterloo"
    country = "Cananda"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':"region region-content"})
    d = dd.find_all('div', {'class':"staff-contact clearfix"})

    #iterating for every prof
    for i in d:
        h2 = i.find('div', {'class':"entry clearfix"})
        a = h2.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        name = " ".join(name.split())

        aa = i.find('div', {'class':"info"})
        a = aa.find('a')
        if a == None:
            continue
            print("if")
        else:
            link = a.get('href')
            if link[0:6] == 'mailto':
                a = a.find_next('a')
                if a == None:
                    continue

        link = a.get('href')

        # print(u_name, name, link)
        # break
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue


        email = "Not Found"

        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def national_tsing_hua():
    url = "https://www.cs.rochester.edu/people/index.html"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "National Tsing Hua University"
    country = "China"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':"columns small-12 medium-9 medium-push-3 section--thin content"})
    d = dd.find_all('div', {"class":'row margin--thin'})
    # print(len(d))

    #iterating for every prof
    for i in d:
        h4 = i.find('h4')
        if h4 == None:
            continue
        a = h4.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        name = " ".join(name.split())
        a2 = i.find('a', text='Website')
        if a2 == None:
            link = a.get('href')
        else:
            link = a2.get('href')

        text = (i.find('li', {'class':'lead'})).get_text()
        if 'Student' in text:
            continue
        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        email = "Not Found"

        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)



    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def sapienza_uni():
    url = "https://www.di.uniroma1.it/en/people/professors"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Sapienza University of Rome"
    country = "Italy"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':"region region-content"})
    d = dd.find_all('tr', {'class':["odd", 'even']})

    #iterating for every prof
    for i in d:
        h2 = i.find('td', {'class':"views-field views-field-title"})
        a = h2.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        name = " ".join(name.split())
        link = "https://www.di.uniroma1.it"+a.get('href')

        # print(u_name, name, link)
        # break
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
            prof_soup = BeautifulSoup(prof_resp.text, "html.parser")
        except:
            continue

        p = prof_soup.find('strong', text="web-page:")
        a = p.find_next('a')
        if a == None:
            continue
        link = a.get('href')
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        a_mail = i.find('td', {'class':"views-field views-field-field-email"})
        if a_mail != None:
            email = (a_mail.get_text()).strip()
            l = len(email)
            email = email[0:l-14]+"@"+email[l-14:]
        else:
            email = "Not Found"

        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def iit_bombay():
    url = "https://www.cse.iitb.ac.in/people/faculty.php"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "IIT Bombay"
    country = "India"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    d = soup.find_all('div', {'class':"region region-content"})
    # d = dd.find_all('div', {'class':"staff-contact clearfix"})

    #iterating for every prof
    for i in d:
        h2 = i.find('div', {'class':"entry clearfix"})
        a = h2.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        name = " ".join(name.split())

        aa = i.find('div', {'class':"info"})
        a = aa.find('a')
        if a == None:
            continue
            print("if")
        else:
            link = a.get('href')
            if link[0:6] == 'mailto':
                a = a.find_next('a')
                if a == None:
                    continue

        link = a.get('href')

        # print(u_name, name, link)
        # break
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue


        email = "Not Found"

        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_bath():
    url = "https://www.bath.ac.uk/teams/department-of-computer-science-academic-staff/"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of Bath"
    country = "UK"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('section', {'class':"team-members"})
    d = dd.find_all('li')

    #iterating for every prof
    for i in d:
        a = i.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        name = " ".join(name.split())
        link = a.get('href')

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue


        email = "Not Found"

        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_tubingen():
    url = "https://www.embedded.uni-tuebingen.de/en/team/"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Eberhard Karls University of Tübingen"
    country = "Germany"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('table')
    d = dd.find_all('tr')

    #iterating for every prof
    for i in d:
        a = i.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        name = " ".join(name.split())
        link = "https://www.embedded.uni-tuebingen.de"+a.get('href')

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue


        email = "Not Found"

        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_freiburg():
    url = "http://www.informatik.uni-freiburg.de/Personen-en"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of Freiburg"
    country = "Germany"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'id':"content"})
    d = dd.find_all('div', {'class':['employee filterable even', 'employee filterable odd']})

    #iterating for every prof
    for i in d:
        div = i.find('div', {'class':'name'})
        a = div.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        name = " ".join(name.split())
        link = a.get('href')

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        div2 = i.find('div', {'class':'function'})
        text = div2.get_text()
        if 'Student' in text or 'student' in text:
            continue

        div2 = i.find('div', {'class':'email'})
        a_mail = div2.find('a')
        if a_mail != None:
            email = a_mail.get('href')
            email = email[7:]
        else:
            email = "Not Found"

        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def hebrew_uni():
    url = "http://www.informatik.uni-freiburg.de/Personen-en"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "The Hebrew University of Jerusalem"
    country = "Israel"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'id':"content"})
    d = dd.find_all('div', {'class':['employee filterable even', 'employee filterable odd']})

    #iterating for every prof
    for i in d:
        div = i.find('div', {'class':'name'})
        a = div.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        name = " ".join(name.split())
        link = a.get('href')

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        div2 = i.find('div', {'class':'function'})
        text = div2.get_text()
        if 'Student' in text or 'student' in text:
            continue

        div2 = i.find('div', {'class':'email'})
        a_mail = div2.find('a')
        if a_mail != None:
            email = a_mail.get('href')
            email = email[7:]
        else:
            email = "Not Found"

        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_college_dublin():    
    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    for x in range(2,11):
        url = "https://www.ucd.ie/cs/people/academicstaff/"+str(x)+"/index.html"
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        r = requests.get(url, headers=headers)

        # getting the soup by parsing the html parsel to text to request r
        soup = BeautifulSoup(r.text, "html5lib")
        # print(soup.prettify)

        u_name = "University College Dublin"
        country = "Ireland"

        grabage_emails = []

        var = [csvwriter, u_name, country]

        # d gives the array of all profs on the dept homepage
        dd = soup.find('section', {'id':"staffProfile"})
        d = dd.find_all('div', {'class':'intro'})

        #iterating for every prof
        for i in d:
            div = i.find('h3')
            a = div.find('a')
            if a == None:
                continue
            name = (a.get_text()).strip()
            name = " ".join(name.split())
            link = a.get('href')

            # print(u_name, name, link)
            # check if link is valid on Not
            try:    
                prof_resp = requests.get(link, headers=headers)   
            except:
                continue

            a_mail = i.find('a', {'class':'email'})
            if a_mail != None:
                email = a_mail.get_text()
            else:
                email = "Not Found"

            print(u_name, name, link)
            filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_minnesota():
    url = "https://cse.umn.edu/cs/faculty-directory"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of Minnesota"
    country = "USA"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':"field--name-field-oc-widgets field--type-paragraphs"})
    d = dd.find_all('div', {'class':'col-sm-7 col-md-7 col-lg-6 col-xl-7'})

    #iterating for every prof
    for i in d:
        div = i.find('div', {'class':'person-entry-name'})
        a = div.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        name = " ".join(name.split())
        link = "https://cse.umn.edu"+a.get('href')

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        div2 = i.find('div', {'class':'field field--name-field-person-email field--type-email field--label-inline'})
        if div2 == None:
            continue
        a_mail = div2.find('a')
        if a_mail != None:
            email = a_mail.get_text()
        else:
            email = "Not Found"

        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def stockholm_uni():
    url = "https://dsv.su.se/en/research/research-areas/itmanagement/people"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Stockholm University"
    country = "Sweden"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':"articleBody"})
    d = dd.find_all('p')

    #iterating for every prof
    for i in d:
        a = i.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        name = " ".join(name.split())
        link = a.get('href')

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        email = "Not Found"

        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_liverpool():
    url = "https://www.liverpool.ac.uk/computer-science/staff/"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of Liverpool"
    country = "UK"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':"org-chart"})
    d = dd.find_all('tr')

    #iterating for every prof
    for i in d:
        td = i.find('td')
        a = td.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        name = " ".join(name.split())
        link = a.get('href')

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        text = i.get_text()
        email = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}", text)
        if len(email) == 0:
            email = "Not Found"
        else:
            email = email[0]

        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_barcelona():
    url = "https://www.liverpool.ac.uk/computer-science/staff/"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of Barcelona"
    country = "Spain"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'id':"body-page"})
    d = dd.find_all('div', {'class':'row'})

    #iterating for every prof
    for i in d:
        td = i.find('h3')
        if td == None:
            continue
        a = td.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        name = " ".join(name.split())
        link = a.get('href')

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        text = i.get_text()
        email = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}", text)
        if email == None:
            email = "Not Found"
        else:
            email = email[0]

        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_otago():
    url = "https://www.otago.ac.nz/computer-science/people/index.html"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of Otago"
    country = "New Zealand"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'id':"content"})
    d = dd.find_all('p')

    #iterating for every prof
    for i in d:
        h3 = i.find_previous('h3')
        if h3 == None:
            continue
        a = h3.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        name = " ".join(name.split())
        link = "https://www.otago.ac.nz"+a.get('href')

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        text = i.get_text()
        if text == "":
            continue
        email = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}", text)
        if len(email) == 0:
            email = "Not Found"
        else:
            email = email[0]

        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def iisc_banglore():
    url = "https://www.csa.iisc.ac.in/people-all/faculty/"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "IISC Banglore"
    country = "India"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':"grid"})
    d = dd.find_all('div', {'class':"peoplebox"})

    #iterating for every prof
    for i in d:
        a = i.find('a')
        if a == None:
            continue
        link = a.get('href')
        div_name = a.find('div', {'class':'name'})
        name = (div_name.get_text()).strip()
        name = " ".join(name.split())

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        a_mail = a.find('div', {'class':'email'})
        if a_mail != None:
            email = (a_mail.get_text()).strip()
            email = email.replace(" [AT] ", "@")
        else:
            email = "Not Found"

        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def king_fahd_uni():
    url = "http://www.kfupm.edu.sa/departments/ics/SitePages/en/Faculty.aspx"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "King Fahd University"
    country = "Saudi Arabia"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':"ContentPanel media-body"})
    # print(dd)
    d = dd.find_all('div', {'class':'media'})

    #iterating for every prof
    for i in d:
        # print(i)
        div1 = i.find('div', text='Website:')
        div2 = div1.find_next('div')
        a = div2.find('a')
        if a == None:
            continue
        link = a.get('href')

        div = i.find('div', {'class':'shortDetails staffsTitle'})
        name = (div.get_text()).strip()
        name = " ".join(name.split())

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue


        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_tech_malaysia():
    url = "https://engineering.utm.my/computing/discipline-of-computer-science/"
    # url = "https://engineering.utm.my/computing/discipline-of-software-engineering/"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of Technology"
    country = "Malaysia"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':"entry-content"})
    d = dd.find_all('div', {'class':'et_pb_blurb_description'})

    #iterating for every prof
    for i in d:
        a = i.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        name = " ".join(name.split())
        link = a.get('href')

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue


        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_vanderbilt():
    url = "https://engineering.vanderbilt.edu/eecs/faculty-staff/index.php"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of Vanderbilt"
    country = "USA"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('table', {'class':"display"})
    d = dd.find_all('tr')

    #iterating for every prof
    for i in d:
        a = i.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        name = " ".join(name.split())
        link = "https://engineering.vanderbilt.edu"+a.get('href')

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue


        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def vienna_uni_tech():
    url = "https://informatics.tuwien.ac.at/people/all"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Vienna University of Technology"
    country = "Austria"

    grabage_emails = ['Models@run.time', 'Requirements@Run.Time']

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('main', {'id':"main"})
    d = dd.find_all('div', {'class':'col-12 col-sm-6 col-md-4 col-lg-3'})

    #iterating for every prof
    for i in d:
        a = i.find('a')
        if a == None:
            continue
        link = 'https://informatics.tuwien.ac.at'+a.get('href')

        div = i.find('div', {'class':'text-truncate'})
        name = (div.get_text()).strip()
        name = " ".join(name.split())

        div2 = i.find('div', {'class':'text-truncate text-muted'})
        pos = (div2.get_text()).strip()
        pos = " ".join(pos.split())

        # print(pos)
        if pos == 'PostDoc Researcher' or pos == 'PreDoc Researcher':
            continue
        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue


        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_bergen():
    url = "https://www.uib.no/en/ii/persons"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of Bergen"
    country = "Norway"

    grabage_emails = ['post@uib.no']

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':"view-content"})
    d = dd.find_all('div', {'class':'uib-user-teaser'})

    #iterating for every prof
    for i in d:
        a = i.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        name = " ".join(name.split())
        link = "https://www.uib.no"+a.get('href')

        p = i.find('p', {'class':'uib-user-position'})
        pos = p.get_text()
        if pos == "PhD Candidate" or pos == "Postdoctoral Fellow":
            continue

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue


        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_goettingen():
    url = "https://www.uni-goettingen.de/en/628113.html"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "university of goettingen"
    country = "Germany"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':"card card-bubble"})
    d = dd.find_all('div', {'class':'adressContact'})

    #iterating for every prof
    for i in d:
        a = i.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        name = " ".join(name.split())
        link = a.get('href')

        # print(name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue


        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()
    print("=====", u_name, "Finished =====")


# ==============================

def uni_wollongong():
    url = "https://www.uow.edu.au/engineering-information-sciences/schools-entities/scit/our-people/"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of Wollongong"
    country = "Australia"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':"page-content grid-container uw-text-block uw-profile-block"})
    d = dd.find_all('div', {'class':'cell uw-profile-card'})

    #iterating for every prof
    for i in d:
        a = i.find('a', {'class':'uw-profile-link'})
        if a == None:
            continue

        div1 = i.find('div', {'class':'uw-profile-person'})
        name = (div1.get_text()).strip()
        name = " ".join(name.split())
        link = a.get('href')

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue


        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_newcastle():
    url = "https://search.newcastle.edu.au/s/search.html?query=&search-submit=&f.Staff+Division+%2F+Faculty%7CStaffDivisionFaculty=College+of+Engineering%2C+Science+and+Environment&f.Staff+Unit+%2F+School%7CStaffUnitSchool=School+of+Electrical+Engineering+and+Computing&f.Staff+Academic+Area+of+Focus%7CStaffFocusArea=Computer+Science+and+Software+Engineering&profile=_default&collection=default_collection&clive=staff_directory"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of NewCastle"
    country = "Australia"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('ol', {'class':"list-unstyled main-results"})
    d = dd.find_all('li', {'class':'g profile-result'})

    #iterating for every prof
    for i in d:
        a = i.find('a', {'class':'result-title'})
        if a == None:
            continue

        name = (a.get_text()).strip()
        name = " ".join(name.split())
        link = "https://search.newcastle.edu.au"+a.get('href')

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue


        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_twente():
    url = "https://www.utwente.nl/en/eemcs/caes/staff/"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of Twente"
    country = "Netherlands"

    grabage_emails = ['info@utwente.nl']

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':"main__contents--12col peopleoverview__summary"})
    d = dd.find_all('a')

    #iterating for every prof
    for i in d:
        a = i
        name = (a.get_text()).strip()
        name = " ".join(name.split())
        link = a.get('href')

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        if name == 'D.M. Abeln (Dorus)':
            break

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def vrije_uni_brussel():
    url = "https://we.vub.ac.be/en/computer-science-department/who-is-who"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Vrije University of Brussel"
    country = "Belgium"

    grabage_emails = ['']

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':"ds-1col entity entity-field-collection-item field-collection-item-field-researcher-categories view-mode-full clearfix"})
    d = dd.find_all('div', {'class':'group-right-info field-group-div'})

    #iterating for every prof
    for i in d:
        div = i.find('div', {"class":'field field-name-title field-type-ds field-label-hidden'})
        a = div.find('a')
        name = (a.get_text()).strip()
        name = " ".join(name.split())
        link = 'https://we.vub.ac.be'+a.get('href')

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)
            prof_soup = BeautifulSoup(prof_resp.text, "html.parser")  
        except:
            continue

        a = prof_soup.find('a', text='Homepage')
        if a == None:
            continue
        link = a.get('href')
        try:    
            prof_resp = requests.get(link, headers=headers)
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_gothenburg():
    url = "https://www.utwente.nl/en/eemcs/caes/staff/"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of Gothernburg"
    country = "Sweden"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':"main__contents--12col peopleoverview__summary"})
    d = dd.find_all('a')

    #iterating for every prof
    for i in d:
        a = i
        name = (a.get_text()).strip()
        name = " ".join(name.split())
        link = a.get('href')

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        if name == 'D.M. Abeln (Dorus)':
            break

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def dartmouth_college():
    url = "https://web.cs.dartmouth.edu/people"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Dartmouth College"
    country = "USA"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':"view-content"})
    d = dd.find_all('div', {'class':'content'})

    #iterating for every prof
    for i in d:
        h3 = i.find('h3')
        a = h3.find('a')
        name = (a.get_text()).strip()
        name = " ".join(name.split())
        link = 'https://web.cs.dartmouth.edu'+a.get('href')

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers) 
            prof_soup = BeautifulSoup(prof_resp.text, "html.parser")  
        except:
            continue

        a = prof_soup.find('a', text='Personal Website')
        if a == None:
            continue
        link = a.get('href')
        try:    
            prof_resp = requests.get(link, headers=headers)
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def western_uni():
    url = "https://www.csd.uwo.ca/people/faculty/index.html"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Western University"
    country = "Canada"

    grabage_emails = ['cs-dept@uwo.ca']

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':"grid_9"})
    d = dd.find_all('div', {'class':'teamgrid'})

    #iterating for every prof
    for i in d:
        h2 = (i.find('div', {'class':'infoleft'})).find('h2')
        name = (h2.get_text()).strip()
        name = " ".join(name.split())
        
        a = i.find('a', text='Biography')
        if a == None:
            continue
        link = 'https://www.csd.uwo.ca/people/faculty/'+a.get('href')

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_reading():
    url = "https://www.reading.ac.uk/computer-science/staff"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of Reading"
    country = "UK"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':"component text-section col-12"})
    d = dd.find_all('tr')

    #iterating for every prof
    for i in d:
        td = i.find('td')
        if td == None:
            continue
        a = td.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        name = " ".join(name.split())
        link = a.get('href')

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_aberdeen():
    url = "https://www.abdn.ac.uk/ncs/departments/computing-science/people-158.php"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of Aberdeen"
    country = "UK"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('dd', {'id':"panel1312"})
    d = dd.find_all('tr')

    #iterating for every prof
    for i in d:
        td = i.find('td')
        if td == None:
            continue
        a = td.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        name = " ".join(name.split())
        link = a.get('href')

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def chulalongkorn_uni():
    url = "https://www.cp.eng.chula.ac.th/en/about/faculty/"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Chulalongkorn University"
    country = "Thailand"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('table', {'id':"instructorList"})
    d = dd.find_all('tr')

    #iterating for every prof
    for i in d:
        td1 = i.find('td')
        if td1 == None:
            continue
        a = (td1.find('a')).find_next('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        name = " ".join(name.split())
        td2 = td1.find_next('td')
        a = td2.find('a')
        if a == None:
            continue
        link = a.get('href')

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def queens_uni_belfast():
    url = "https://www.qub.ac.uk/schools/eeecs/Connect/Staff/"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Queens University Belfast"
    country = "UK"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('main', {'class':"l_two-column"})
    d = dd.find_all('span')

    #iterating for every prof
    for i in d:
        a = i.find('a')
        if a == None:
            continue
        name = (i.get_text()).strip()
        name = " ".join(name.split())
        link = "https://www.qub.ac.uk"+a.get('href')

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_cal_irvine():
    url = "https://www.cs.uci.edu/faculty/"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of California, Irvine"
    country = "USA"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':"entry-content"})
    d = dd.find_all('tr')

    #iterating for every prof
    for i in d:
        a = i.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        name = " ".join(name.split())
        link = a.get('href')

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def khalifa_uni():
    url = "https://www.ku.ac.ae/academics/college-of-engineering/department/department-of-electrical-engineering-and-computer-science#people"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Khalifa University, Abu Dhabi"
    country = "UAE"

    grabage_emails = ['support@ku.ac.ae', 'md@ku.ac.ae', 'coas@ku.ac.ae', 'coe@ku.ac.ae', 'info@ku.ac.ae']

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':"common-members-block clear Faculty"})
    d = dd.find_all('span', {'class':'name'})

    #iterating for every prof
    for i in d:
        a = i.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        name = " ".join(name.split())
        link = a.get('href')

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_notre_dame():    
    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of Notre dame"
    country = "USA"

    grabage_emails = ['cse@nd.edu']
    
    for l in range(1,4):
        url = "https://cse.nd.edu/faculty/page/"+str(l)
        print(url)
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        r = requests.get(url, headers=headers)

        # getting the soup by parsing the html parsel to text to request r
        soup = BeautifulSoup(r.text, "html5lib")
        # print(soup.prettify)

        var = [csvwriter, u_name, country]

        # d gives the array of all profs on the dept homepage
        dd = soup.find('div', {'class':"entry-content"})
        d = dd.find_all('div', {'class':'grid directory-grid'})

        #iterating for every prof
        for i in d:
            h2 = i.find('h2')
            a = h2.find('a')
            if a == None:
                continue
            name = (a.get_text()).strip()
            name = " ".join(name.split())
            link = a.get('href')

            # print(u_name, name, link)
            # check if link is valid on Not
            try:    
                prof_resp = requests.get(link, headers=headers)   
            except:
                continue

            email = "Not Found"
            print(u_name, name, link)
            filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def macquarie_uni():
    url = "https://www.mq.edu.au/faculty-of-science-and-engineering/departments-and-schools/department-of-computing/our-people"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Macquarie University"
    country = "Australia"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('table', {'id':"table48609"})
    d = dd.find_all('tr')

    #iterating for every prof
    for i in d:
        a = i.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        name = " ".join(name.split())
        link = a.get('href')

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def radboud_uni():
    url = "https://www.ru.nl/icis/about_icis/staff/"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Radboud University"
    country = "Netherlands"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    # dd = soup.find('table', {'id':"table48609"})
    d = soup.find_all('tr')

    #iterating for every prof
    for i in d:
        a = i.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        name = " ".join(name.split())
        link = a.get('href')

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_padova():
    url = "https://www.dei.unipd.it/en/people"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of Padova"
    country = "Italy"

    grabage_emails = ['webmaster@dei.unipd.it', 'info@dei.unipd.it']

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('ul', {'class':"personale"})
    d = dd.find_all('li')

    #iterating for every prof
    for i in d:
        a = i.find('a')
        if a == None:
            continue
        span1 = i.find('span')
        name_l = (span1.get_text()).strip()
        span2 = span1.find_next('span')
        name_f = (span2.get_text()).strip()
        name = name_f+" "+name_l 
        link = "https://www.dei.unipd.it/en/"+a.get('href')

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def curtin_uni():    
    url = "https://scieng.curtin.edu.au/schools/electrical-eng-computing-maths/our-people/"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

        # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Curtin University"
    country = "Australia"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('main', {'class':"main-content"})
    d = dd.find_all('li')

    #iterating for every prof
    for i in d:
        a = i.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        name = " ".join(name.split())
        link = a.get('href')

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def queensland_uni_tech():    
    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Queensland University of Technology"
    country = "Australia"

    grabage_emails = []
    
    for l in range(1,6):
        url = "https://staff.qut.edu.au/?upage="+str(l)+"&school=Computer+Science"
        print(url)
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        r = requests.get(url, headers=headers)

        # getting the soup by parsing the html parsel to text to request r
        soup = BeautifulSoup(r.text, "html5lib")
        # print(soup.prettify)

        var = [csvwriter, u_name, country]

        # d gives the array of all profs on the dept homepage
        dd = soup.find('ul', {'id':"members-list"})
        d = dd.find_all('li')

        #iterating for every prof
        for i in d:
            div = i.find('div', {'class':'item-title'})
            a = div.find('a')
            if a == None:
                continue
            name = (a.get_text()).strip()
            name = " ".join(name.split())
            link = a.get('href')

            # print(u_name, name, link)
            # check if link is valid on Not
            try:    
                prof_resp = requests.get(link, headers=headers)   
            except:
                continue

            email = "Not Found"
            print(u_name, name, link)
            filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_virginia():    
    url = "https://engineering.virginia.edu/departments/computer-science/faculty"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of Virginia"
    country = "USA"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':"listings faculty results"})
    d = dd.find_all('div', {'class':'user-markup content-container'})

    #iterating for every prof
    for i in d:
        h3 = i.find('h3')
        a = h3.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        name = " ".join(name.split())
        link = "https://engineering.virginia.edu"+a.get('href')

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def arizona_state_uni():    
    url = "https://cidse.engineering.asu.edu/faculty/"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Arizona State University"
    country = "USA"

    grabage_emails = ['Number-1-in-the-us-for-innovation@2x.png']

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':"et_builder_inner_content et_pb_gutters3"})
    d = dd.find_all('article')

    #iterating for every prof
    for i in d:
        div = i.find('div', {'class':'et_pb_text_inner'})
        a = div.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        name = " ".join(name.split())
        link = a.get('href')

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_cape_town():    
    url = "https://www.cs.uct.ac.za/staff"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of Cape Town"
    country = "South Africa"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('table', {'class':"staff"})
    d = dd.find_all('tr')

    #iterating for every prof
    for i in d:
        td = (i.find('td')).find_next('td')
        b = td.find('b')
        name = (b.get_text()).strip()
        name = " ".join(name.split())
        
        a = (i.find('blockquote')).find('a')
        if a == None:
            continue

        link = a.get('href')
        if link[0] == '~':
            link = "https://www.cs.uct.ac.za/"+link

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def rmit_uni():    
    url = "https://www.rmit.edu.au/about/schools-colleges/science/contact/computer-science-and-information-technology"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "RMIT University"
    country = "Australia"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':"responsivegrid"})
    d = dd.find_all('li')

    #iterating for every prof
    for i in d:
        a = i.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        name = " ".join(name.split())
        link = a.get('href')
        if link == None:
            continue
        link = "https://www.rmit.edu.au"+link

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def victoria_uni_wellington():    
    url = "https://www.wgtn.ac.nz/engineering/school-of-engineering-and-computer-science/staff"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Victoria University of Wellington"
    country = "New Zealand"

    grabage_emails = ['info@vuw.ac.nz']

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':"staff-list"})
    d = dd.find_all('div', {'class':'summary'})

    #iterating for every prof
    for i in d:
        h3 = i.find('h3')
        a = h3.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        name = " ".join(name.split())
        link = a.get('href')

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def saint_petesburg_state_uni():    
    url = "https://math-cs.spbu.ru/en/people/"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Saint Petesburg State University"
    country = "Russia"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    # dd = soup.find('div', {'class':"staff-list"})
    d = soup.find_all('div', {'class':'col-sm-12 col-md-4 col-lg-2 teachers'})

    #iterating for every prof
    for i in d:
        a = i.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        name = " ".join(name.split())
        link = "https://math-cs.spbu.ru"+a.get('href')

        # print(u_name, name, link)
        # check if link is valid on Not
        if name == 'Yurii Lyubarskii':
            break

        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def loughborough_uni():    
    url = "https://www.lboro.ac.uk/departments/compsci/staff/"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Loughborough University"
    country = "UK"

    grabage_emails = ['compsci@lboro.ac.uk']

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':"container-fluid"})
    dd = dd.find_next('div', {'class':"container-fluid"})
    # print(dd)
    d = dd.find_all('div', {'class':'picture-item__inner'})

    #iterating for every prof
    for i in d:
        a = i.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        name = " ".join(name.split())
        link = "https://www.lboro.ac.uk"+a.get('href')

        # print(u_name, name, link)
        # check if link is valid on Not

        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def novosibirsk_state_uni():    
    url = "https://research.nsu.ru/en/organisations/%D0%BA%D0%B0%D1%84%D0%B5%D0%B4%D1%80%D0%B0-%D0%B8%D0%BD%D1%84%D0%BE%D1%80%D0%BC%D0%B0%D1%82%D0%B8%D0%BA%D0%B8-%D0%B2%D0%BA%D0%B8/persons/"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Novosibirsk State University"
    country = "Russia"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('ul', {'class':"grid-results"})
    d = dd.find_all('div', {'class':'result-container'})

    #iterating for every prof
    for i in d:
        a = i.find('a', {'class':'link person'})
        if a == None:
            continue
        name = (a.get_text()).strip()
        name = " ".join(name.split())
        link = a.get('href')

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        aa = i.find('a', {'class':'link'})
        if aa == None:
            email = "Not Found"
        else:
            email = (aa.get_text()).strip()
            email = " ".join(email.split())

        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def university_hamburg():    
    url = "https://www2.informatik.uni-hamburg.de/fiona/pers.php?lang=en&ltype=ordner&group=PROF"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of Hamburg"
    country = "Germany"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':"sortierung"})
    d = soup.find_all('div', {'class':'name'})

    #iterating for every prof
    for i in d:
        a = i.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        name = " ".join(name.split())
        link = a.get('href')

        # print(u_name, name, link)
        # check if link is valid on Not

        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def georgetown_uni():    
    url = "https://cs.georgetown.edu/faculty/#"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Georgetown University"
    country = "USA"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('main', {'class':"l-main-page"})
    d = soup.find_all('div', {'class':'profile-content'})

    #iterating for every prof
    for i in d:
        h2 = i.find('h2')
        a = h2.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        name = " ".join(name.split())
        link = a.get('href')

        # print(u_name, name, link)
        # check if link is valid on Not

        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def tel_aviv_uni():    
    url = "https://en-exact-sciences.tau.ac.il/computer/faculty_members"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Tel Aviv University"
    country = "Israel"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('table', {'class':"tau-person-results-table tau-person-results-table-ptg sticky-enabled"})
    d = soup.find_all('tr', {"class":['odd', 'even']})

    #iterating for every prof
    for i in d:
        td = i.find('td')
        if td == None:
            continue
        a = td.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        name = " ".join(name.split())

        div = i.find('div', {'class':"tau-person-social-network"})
        div = div.find_next('div', {'class':"tau-person-social-network"})
        aa = div.find('a')
        if aa == None:
            continue
        link = aa.get('href')

        # print(u_name, name, link)
        # check if link is valid on Not

        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_colorado_boulder():    
    url = "https://www.colorado.edu/cs/faculty-staff-directory"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of Colorado Boulder"
    country = "USA"

    grabage_emails = ['cueng@colorado.edu']

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':"people-list-wrapper-table"})
    d = soup.find_all('tr')

    #iterating for every prof
    for i in d:
        td = i.find('td', {'class':'person-table-name'})
        if td == None:
            continue
        strong = td.find('strong')
        a = strong.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        name = " ".join(name.split())
        link = "https://www.colorado.edu"+a.get('href')

        # print(u_name, name, link)
        # check if link is valid on Not

        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def unicamp():    
    url = "https://www.ic.unicamp.br/en/docentes/"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University Estadual De Campinas"
    country = "Brazil"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'id':"grid-people"})
    d = soup.find_all('div', {'class':'people-box'})

    #iterating for every prof
    for i in d:
        h4 = i.find('h4', {'class':'name'})
        if h4 == None:
            continue
        a = h4.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        name = " ".join(name.split())
        link = a.get('href')

        # print(u_name, name, link)
        # check if link is valid on Not

        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def maastritch_uni():    
    url = "https://www.maastrichtuniversity.nl/faculty-and-staff"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Maastritch University"
    country = "Netherlands"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('table', {'class':"extended"})
    d = soup.find_all('tr')

    #iterating for every prof
    for i in d:
        h2 = i.find('h2')
        if h2 == None:
            continue
        name = (h2.get_text()).strip()
        name = " ".join(name.split())
        span = i.find('span', {'class':'icon-user'})
        a = span.find('a')
        if a == None:
            continue
        link = "https://www.maastrichtuniversity.nl"+a.get('href')

        # print(u_name, name, link)
        # check if link is valid on Not

        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def cheng_kung_uni():    
    url = "https://www.csie.ncku.edu.tw/ncku_csie/depmember/teacher?lang=en"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "National Cheng Kung University"
    country = "Taiwan"

    grabage_emails = ['em62500@email.ncku.edu.tw']

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('table', {'class':"teacherTableStyle"})
    d = dd.find_all('td', {'class':'teacherInfo'})

    #iterating for every prof
    for i in d:
        a = i.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        name = " ".join(name.split())
        link = "https://www.csie.ncku.edu.tw/ncku_csie/depmember/"+a.get('href')

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def kyung_hee_uni():    
    url = "http://ce.khu.ac.kr/eng/members/list_hi.php"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Kyung Hee University"
    country = "South Koria"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'id':"members_01"})
    d = dd.find_all('td', {'class':'teacherInfo'})

    #iterating for every prof
    for i in d:
        a = i.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        name = " ".join(name.split())
        link = a.get('href')

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def vrije_uni_amsterdam():    
    url = "https://www.cs.vu.nl/en/research/computer-systems/hpdc/people/index.aspx"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Vrije University Amsterdam"
    country = "Netherlands"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('article', {'class':"col-xs-12 text-item"})
    # print(dd)
    d = dd.find_all('p')

    #iterating for every prof
    for i in d:
        a = i.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        name = " ".join(name.split())
        link = a.get('href')

        # print(u_name, name, link)
        # check if link is valid on Not
        text = i.get_text()
        if "Post" in text or "PhD" in text:      
            continue

        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def nat_uni_ireland():    
    url = "https://www.nuigalway.ie/science-engineering/school-of-computer-science/people/#"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "National University of Ireland Galway"
    country = "Ireland"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'id':"pageContentWrapper"})
    d = dd.find_all('div', {'class':'person clearfix'})

    #iterating for every prof
    for i in d:
        strong = i.find('strong')
        a = strong.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        name = " ".join(name.split())
        link = a.get('href')

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_antwerp():    
    url = "https://www.uantwerpen.be/nl/personeel/?q=UA324"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of Antwerp"
    country = "Belgium"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':"listWrap"})
    d = dd.find_all('div', {'class':'wrap'})

    #iterating for every prof
    for i in d:
        h3 = i.find('h3', {'class':'heading'})
        a = h3.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        name = " ".join(name.split())
        link = "https://www.uantwerpen.be"+a.get('href')

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def national_chiao_tung_uni():    
    url = "https://www.cs.nycu.edu.tw/members/prof"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "National Chiao Tung University"
    country = "Taiwan"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':"col-sm-9"})
    d = dd.find_all('div', {'class':'col-md-3 col-sm-4 col-xs-6'})

    #iterating for every prof
    for i in d:
        small = (i.find('h2', {'class':'member-name'})).find('small')
        name = (small.get_text()).strip()
        name = " ".join(name.split())

        div = i.find('div', {'class':'member-links'})
        a = div.find('a')
        if a == None:
            continue
        link = a.get('href')

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_bonn():    
    url = "https://gsg.cs.uni-bonn.de/mirror/staff-en.html"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of Bonn"
    country = "Germany"

    grabage_emails = ['webmaster@cs.uni-bonn.de', 'i@c.mult.ps.gz']

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = (soup.find('table')).find_next('table')
    d = dd.find_all('tr')

    #iterating for every prof
    for i in d:
        td = i.find('td')
        if td == None:
            continue
        name = (td.get_text()).strip()
        name = " ".join(name.split())

        a = td.find('a')
        if a == None:
            continue
        link = a.get('href')

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def uni_leicester():    
    url = "https://le.ac.uk/informatics/people/academic-and-research-staff"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of Leicester"
    country = "UK"

    grabage_emails = ['webmaster@mcs.le.ac.uk', 'pgadmissions@le.ac.uk', 'seadmissions@le.ac.uk', 'csadmin@mcs.le.ac.uk']

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':"page-body-description"})
    d = dd.find_all('tr')

    #iterating for every prof
    for i in d:
        td = i.find('td')
        if td == None:
            continue
        a = td.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        name = " ".join(name.split())
        link = a.get('href')

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        td_e = (((td.find_next('td')).find_next('td')).find_next('td')).find_next('td')
        aa = td_e.find('a')
        if aa == None:
            email = "Not Found"
        else:
            email = (aa.get_text()).strip()
            email = " ".join(email.split())

        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def qatar_uni():    
    url = "http://www.qu.edu.qa/engineering/Academic-Departments/Department-of-Computer-Science-&-Engineering/Faculty-and-Staff"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Qatar University"
    country = "Qatar"

    grabage_emails = []
    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'id':"breadcrumbs_holder"})
    d = dd.find_all('div', {'class':'col-xs-12 col-sm-6 margin-md-ver'})

    #iterating for every prof
    for i in d:
        span = i.find('span', {'class':'bold block blue'})
        if span == None:
            continue
        name = (span.get_text()).strip()
        name = " ".join(name.split())


        a = i.find('a', {'target':'_blank'})
        if a == None:
            continue
        link = a.get('href')

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# ============================

def queens_uni_kingston():    
    url = "https://www.cs.queensu.ca/people/faculty.php"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Queens University Kingston"
    country = "Canada"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'id':"qsc_content"})
    d = dd.find_all('a')

    #iterating for every prof
    for i in d:
        span = i.find('span', {'class':'name'})
        if span == None:
            continue
        
        name = (span.get_text()).strip()
        name = " ".join(name.split())
        link = i.get('href')

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        email = "Not Found"
        
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")


# ============================

def uni_calgary():    
    url = "https://www.cs.queensu.ca/people/faculty.php"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    file_name = sys.argv[0]
    # file_name = file_name[4:]

    txt_file = file_name.replace(".py", ".txt")
    f = open(txt_file, "w")

    csv_file = file_name.replace(".py", ".csv")
    f2 = open(csv_file, "w")
    csvwriter = csv.writer(f2)

    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of Calgary"
    country = "Canada"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'id':"qsc_content"})
    d = dd.find_all('a')

    #iterating for every prof
    for i in d:
        span = i.find('span', {'class':'name'})
        if span == None:
            continue
        
        name = (span.get_text()).strip()
        name = " ".join(name.split())
        link = i.get('href')

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        email = "Not Found"
        
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()
    f2.close()
    f3.close()
    print("=====", u_name, "Finished =====")

# ============================

def uni_sussex():    
    url = "http://www.sussex.ac.uk/informatics/people/peoplelists/group/teaching-faculty"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "University of Sussex"
    country = "UK"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'id':"contentWrapper"})
    d = dd.find_all('div', {'class':'vcard palette4 swatch1'})

    #iterating for every prof
    for i in d:
        a = i.find('a', {'class':'url fn'})
        if a == None:
            continue
        name = (a.get_text()).strip()
        name = " ".join(name.split())
        link = "www.sussex.ac.uk"+a.get('href')

        # print(u_name, name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        span = i.find('span', {'class':'email'})
        aa = span.find('a')
        if aa == None:
            email = "Not Found"
        else:
            email = (aa.get_text()).strip()
            email = " ".join(email.split())

        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()

    print("=====", u_name, "Finished =====")

# =================================

def tomsk_state_uni():    
    url = "http://en.tsu.ru/schools_and_departments/department_of_applied_mathematics_and_cybernetics.php"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    overall_file = "all_emails.csv"
    file = open(overall_file, "a")
    csvwriter = csv.writer(file)

    u_name = "Tomsk State University"
    country = "Russia"

    grabage_emails = []

    var = [csvwriter, u_name, country]

    # d gives the array of all profs on the dept homepage
    # dd = soup.find('div', {'id':"contentWrapper"})
    d = soup.find_all('div', {'class':'row html-text'})

    #iterating for every prof
    for i in d:
        a = i.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        name = " ".join(name.split())
        link = a.get('href')

        # print(name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue


        email = "Not Found"
        print(u_name, name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    file.close()
    print("=====", u_name, "Finished =====")

# ===============================



# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ==========================================================

def filterandgetEmail(var, grabage_emails, name, link, email, prof_resp):
    
    csvwriter = var[0]

    u_name = var[1]
    country = var[2]

    keyword_list = ['Computer Architecture','hardware and system architecture', 'hardware and architecture', 'Computerarchitectuur', 'embedded system', 'computer organization','VLSI Design', 'Computer and System',
                    'multiprocessor architecture']
    flag = 1
    prof_soup = BeautifulSoup(prof_resp.text, "html.parser")
    # print(prof_soup)
    research_text = prof_soup.text
    for pattern in keyword_list:
        if re.search(pattern, research_text, re.IGNORECASE):
            flag = 0
            if email != 'Not Found':
                csvwriter.writerow([u_name, country, name, email, link])
            else:
                new_emails = set(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}", prof_resp.text))
                for eemail in grabage_emails:
                    if eemail in new_emails:
                        new_emails.remove(eemail)
                if len(new_emails) == 0:
                    email = "Email Not Found"
                    csvwriter.writerow([u_name, country, name, email, link])
                else:
                    for email in new_emails:
                        csvwriter.writerow([u_name, country, name, email, link])
                    
            break

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def filterandgetEmail2(var, grabage_emails, name, link, email, prof_resp):
    csvwriter = var[0]

    u_name = var[1]
    country = var[2]

    keyword_list = ['computer architecture', 'Computer architecture', 'Embedded System', 'Embedded system', 'embedded system']   # 'Computer Architecture',
    flag = 1
    prof_soup = BeautifulSoup(prof_resp.text, "html.parser") 
    research_text = prof_soup.text
    for pattern in keyword_list:
        if re.search(pattern,research_text):
            flag = 0
            if email != 'Not Found':
                csvwriter.writerow([u_name, country, name, email, link])
            else:
                new_emails = set(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}", prof_resp.text))
                for eemail in grabage_emails:
                    if eemail in new_emails:
                        new_emails.remove(eemail)
                if len(new_emails) == 0:
                    email = "Email Not Found"
                    csvwriter.writerow([u_name, country, name, email, link])
                else:
                    for email in new_emails:
                        csvwriter.writerow([u_name, country, name, email, link])
 
            break

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def OnlygetEmail(var, grabage_emails, name, link, email, prof_resp):
    csvwriter = var[0]

    u_name = var[1]
    country = var[2]

    prof_soup = BeautifulSoup(prof_resp.text, "html.parser") 

    if email != 'Not Found':
        csvwriter.writerow([u_name, country, name, email, link])
    else:
        new_emails = set(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}", prof_resp.text))
        for eemail in grabage_emails:
            if eemail in new_emails:
                new_emails.remove(eemail)
        if len(new_emails) == 0:
            email = "Email Not Found"
            csvwriter.writerow([u_name, country, name, email, link])
        else:
            for email in new_emails:
                csvwriter.writerow([u_name, country, name, email, link])


# +++++++++++++++++++++++++++++++++++++++++++++++++++++


if __name__ == '__main__':
    # mit()
    stanford()
    harvard()
    caltech()
    oxford()
    uni_cambridge()
    imperial_college()
    uchicago()
    ucl_london()
    nus()
    princeton()
    ntus()
    tsinghua()
    uni_penn()
    yale()
    cornell()
    uni_columbia()
    uni_edinburgh()
    uni_michigan()
    uni_hongkong()
    peking_uni()
    uni_tokyo()
    john_hopkins()
    uni_toranto()
    uni_menchester()
    northwestern_uni()
    UC_berkeley()
    aus_nat_uni()
    kings_college_london()
    mcgill_uni()
    fudan_uni()
    nyc_uni()
    ucla()
    seoul_university()
    kaist()
    uni_sydney()
    uni_melbourne()
    duke_university()
    chinese_uni_hongkong()
    uni_NSW()
    ubc_canada()
    uni_queensland()
    shanghai_jt()
    city_uni_hk()
    carnegie_mellon()
    uni_psl()
    zhejiang_uni()
    ucsd()
    monash_uni()
    tokyo_uni_tech()
    delft_uni_tech()
    brown_uni()
    uni_warwick()
    uni_wisconsin()
    taiwan_university()
    korea_university()
    uni_austin()
    osaka_uni()
    uni_washington()
    hong_kong_poly_uni()
    uni_copenhagen()
    postech_korea()
    uni_glasgow()
    tohoku_university()
    georgia_inst_tech()
    uni_auckland()
    uni_illinois()
    ku_leaven()
    durham_university()
    yonsei_uni()
    uni_bermingham()
    sungkyunkwan_uni()
    rice_university()
    uni_southampton()
    uni_leeds()
    uni_sheffield()
    uni_north_carolina()
    lund_university()
    kth_sweden()
    uni_nottingham()
    # 100
    penn_state()
    trinity_college_dublin()
    tud_denmark()
    uni_helsinki()
    washington_uni_sl()
    uni_geneva()
    ohio_state_university()
    perdue_uni()
    boston_uni()
    nagoya_uni()
    uc_davis()
    uni_oslo()
    queen_mary()
    uni_bern()
    uni_berlin()
    uni_montreal()
    uni_alberta()
    pontificia_uni()
    uni_southern_cal()
    utretch_uni()
    kyusu_uni()
    uppsala_uni()
    aalto_uni()
    leiden_uni()
    uni_grogingen()
    free_uni_germany()
    uni_putra_malaysia()
    uni_tech_sydney()
    lancaster_uni()
    uni_ghent()
    uni_centrale()
    chalmers_uni()
    hokkaido_uni()
    usm_malaysia()
    king_abdulaziz_uni()
    mcmaster_uni()
    rwth_uni()
    hanyang_uni()
    aarhus_uni()
    tech_uni_berlin()
    uni_basel()
    # 150
    uni_york()
    newcastle_uni()
    uc_santa_barbara()
    uni_maryland()
    uni_pittsburgh()
    michigan_state()
    emory_university()
    cardiff_university()
    ens_lyon()
    case_western()
    uni_florida()
    uni_exeter()
    uni_rochester()
    uni_waterloo()
    national_tsing_hua()
    sapienza_uni()
    iit_bombay()
    uni_bath()
    uni_tubingen()
    uni_freiburg()
    hebrew_uni()
    uni_college_dublin()
    uni_minnesota()
    stockholm_uni()
    uni_liverpool()
    uni_barcelona()
    uni_otago()
    iisc_banglore()
    king_fahd_uni()
    uni_tech_malaysia()
    uni_vanderbilt()
    vienna_uni_tech()
    uni_bergen()
    uni_goettingen()
    uni_wollongong()
    uni_newcastle()
    uni_twente()
    # 200
    vrije_uni_brussel()
    uni_gothenburg()
    dartmouth_college()
    western_uni()
    uni_reading()
    uni_aberdeen()
    chulalongkorn_uni()
    queens_uni_belfast()
    uni_cal_irvine()
    khalifa_uni()
    uni_notre_dame()
    macquarie_uni()
    radboud_uni()
    uni_padova()
    curtin_uni()
    queensland_uni_tech()
    uni_virginia()
    arizona_state_uni()
    uni_cape_town()
    rmit_uni()
    victoria_uni_wellington()
    saint_petesburg_state_uni()
    loughborough_uni()
    novosibirsk_state_uni()
    university_hamburg()
    georgetown_uni()
    tel_aviv_uni()
    uni_colorado_boulder()
    unicamp()
    maastritch_uni()
    cheng_kung_uni()
    kyung_hee_uni()
    vrije_uni_amsterdam()
    nat_uni_ireland()
    uni_antwerp()
    national_chiao_tung_uni()
    uni_bonn()
    uni_leicester()
    qatar_uni()
    queens_uni_kingston()
    uni_calgary()
    uni_sussex()
    tomsk_state_uni()

    print("All Complete")


