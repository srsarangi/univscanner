import csv
import re
import time
import urllib
import urllib.request

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def micki():
    url = "https://wmi.amu.edu.pl/en/faculty/staff"
    response = requests.get(url)
    driver = webdriver.Chrome()  # Replace with your WebDriver (e.g., ChromeDriver path)
    driver.get(url)
    flag = True
    try:
        # scrappable
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "page-content-wrapper"))
        )
        # scrappable
        print("element loaded")
    
        soup = BeautifulSoup(driver.page_source, "html.parser")
        # soup = BeautifulSoup(response.text, "html.parser")
    except:
        print("ERROR: Page not loaded")
        flag = False
        return False
    finally:
        
        driver.quit()
        if not flag:
            return False
        csv_filename = "Adam Mickiewicz University.csv"
        final_csv = "combined.csv"
        
        f1 = open(csv_filename, "w") # write data to the csv
        csvwriter1 = csv.writer(f1)

        f2 = open(final_csv, "a") # append data to the combined csv
        csvwriter2 = csv.writer(f2)

        univ_name = "Adam Mickiewicz University"
        country = "Poland"

        garbage_emails = [] # add garbage emails to this list

        variables = [csvwriter1, csvwriter2, univ_name, country, garbage_emails]

        d = soup.find('div',{'id':'faculty-members'})
        ul = d.find('ul')
        dd = ul.find_all('li')
        for i in dd:
            #list-people__item__wrapper
            div = i.find('div',{'class':'list-people__item__wrapper'})
            if div == None:
                continue
            h3 = div.find('h3')
            if h3 == None:
                continue
            a = h3.find('a')
            if a == None:
                continue
            name = a.get_text().strip()
            link = a.get('href')
            email = "Not Found"
            print(name, link)
            try:
                prof_resp = requests.get(link)
            except:
                print("prof website not reached on time")
                continue
            get_email(variables,garbage_emails,name,link,email,prof_resp)


        
        f1.close()
        f2.close()
        print("Finished")

        



def get_email(variables,garbage_emails,name,link,email,page_resp):
    csvwriter1, csvwriter2, univ_name, country, garbage_emails = variables
    # if email != "Not Found": # if email is already found, no need to find it again (at line 50)
    #     # just write
    #     csvwriter1.writerow([univ_name,country,name,email,link])
    #     csvwriter2.writerow([univ_name,country,name,email,link])
    #     return
    prof_soup = BeautifulSoup(page_resp.text, "html.parser")
    # key_words = ['BASE'] # base is used when there is no use of keywords
    key_words = ['operating systems','Embedded System','embedded system', 'Operating Systems','operating system','Operating System','embedded systems',"Embedded Systems",'kernel','Microcontroller Systems','Integrated Systems','Embedded Computing','Embedded Software','unix','linux']
    # key_words_spanish = ['sistemas operativos', 'sistema embebido', 'sistema embebido', 'Sistemas Operativos', 'sistema operativo', 'Sistema Operativo', 'sistemas embebidos', 'Sistemas Embebidos']
    # Distributed computing
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
    micki()



            







        