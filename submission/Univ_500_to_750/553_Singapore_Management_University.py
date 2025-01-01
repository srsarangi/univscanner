import requests
import urllib.request
import time
import urllib
import re
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def smu(url):
    # url = "https://computing.smu.edu.sg/people/full-time-faculty?faculty%5Bpage%5D=1&faculty%5BhierarchicalMenu%5D%5Bresearcharea.lvl0%5D%5B0%5D=School%20of%20Computing%20and%20Information%20Systems"
    # Setup Selenium WebDriver
    driver = webdriver.Chrome()  # Replace with your WebDriver (e.g., ChromeDriver path)
    driver.get(url)
    try:
        # Wait until the 'hits' div is fully loaded
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "hits"))
        )
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # scrappable
        # soup = BeautifulSoup(response.text, "html.parser")
        csv_filename = "Singapore Management University.csv"
        final_csv = "combined.csv"
        
        f1 = open(csv_filename, "a") # write data to the csv
        csvwriter1 = csv.writer(f1)

        f2 = open(final_csv, "a") # append data to the combined csv
        csvwriter2 = csv.writer(f2)

        univ_name = "Singapore Management University"
        country = "Singapore"

        garbage_emails = [] # add garbage emails to this list

        variables = [csvwriter1, csvwriter2, univ_name, country, garbage_emails]
        d = soup.find('div', {'id': 'hits'})
        # print(len(d))
        # print(d)
        if d == None:
            print("No data found")
            return False
        dd = d.find_all('li', {'class': 'ais-Hits-item col-12 mb-4'})
        # print(len(dd))
        if len(dd) == 0:
            return False
        for i in dd:
            name_div = i.find('div', {'class': 'hit-name'})
            name = name_div.find('a').get_text()
            link = "https://computing.smu.edu.sg" + name_div.find('a').get('href')
            email = "Not Found"
            email_div = i.find('div', {'class': 'email'})
            if email_div != None:
                email = email_div.get_text()
            print(name, link,email)
            try:
                prof_resp = requests.get(link)
            except:
                print("prof website not reached on time")
                continue
            get_email(variables,garbage_emails,name,link,email,prof_resp)
        # GET DATA
        
        f1.close()
        f2.close()
        print("Finished")
        return True
    except:
        # print(response.status_code)
        print("Error")
        return False



def get_email(variables,garbage_emails,name,link,email,page_resp):
    csvwriter1, csvwriter2, univ_name, country, garbage_emails = variables
    # if email != "Not Found": # if email is already found, no need to find it again (at line 50)
    #     # just write
    #     csvwriter1.writerow([univ_name,country,name,email,link])
    #     csvwriter2.writerow([univ_name,country,name,email,link])
    #     return
    prof_soup = BeautifulSoup(page_resp.text, "html.parser")
    # key_words = ['BASE'] # base is used when there is no use of keywords
    key_words = ['operating systems','Embedded System','embedded system', 'Operating Systems','operating system','Operating System','embedded systems',"Embedded Systems"]
    # key_words_spanish = ['sistemas operativos', 'sistema embebido', 'sistema embebido', 'Sistemas Operativos', 'sistema operativo', 'Sistema Operativo', 'sistemas embebidos', 'Sistemas Embebidos']

    prof_text = prof_soup.text   # get the text from the page

    for word in key_words:
        if re.search(word,prof_text,re.IGNORECASE) or word == 'BASE':
            print("matched_word: ",word)
            if email != "Not Found": # if email is already found, no need to find it again (at line 50)
                # just write
                csvwriter1.writerow([univ_name,country,name,email,link])
                csvwriter2.writerow([univ_name,country,name,email,link])
            else:
                new_emails = list(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", prof_text))
                for em in garbage_emails:
                    if em in new_emails:
                        new_emails.remove(em)
                if len(new_emails) == 0:
                    email = "Email Not Found"
                    csvwriter1.writerow([univ_name,country,name,email,link])
                    csvwriter2.writerow([univ_name,country,name,email,link])
                else:
                    prof_email = new_emails[0]
                    csvwriter1.writerow([univ_name,country,name,prof_email,link])
                    csvwriter2.writerow([univ_name,country,name,prof_email,link])
            
            break


                
            


if __name__ == '__main__':
    # smu()
    # url = "https://computing.smu.edu.sg/people/full-time-faculty?faculty%5Bpage%5D=1&faculty%5BhierarchicalMenu%5D%5Bresearcharea.lvl0%5D%5B0%5D=School%20of%20Computing%20and%20Information%20Systems"
    # smu(url)
    prefix = "https://computing.smu.edu.sg/people/full-time-faculty?faculty%5Bpage%5D="
    suffix = "&faculty%5BhierarchicalMenu%5D%5Bresearcharea.lvl0%5D%5B0%5D=School%20of%20Computing%20and%20Information%20Systems"
    i = 1
    while True:
        print("Page: ",i)
        if not smu(prefix+str(i)+suffix):
            break
        else:
            i += 1
    



            







        