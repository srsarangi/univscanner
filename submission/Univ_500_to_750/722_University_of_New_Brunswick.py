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

# JUST TEMPLATE
def brunswick():
    url = "https://www.unb.ca/fredericton/cs/faculty-staff.html"
    return
    driver = webdriver.Chrome()  # Replace with your WebDriver (e.g., ChromeDriver path)
    driver.get(url)
    flag = True
    try:
        # scrappable
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
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
        csv_filename = "University of New Brunswick.csv"
        final_csv = "combined.csv"
        
        f1 = open(csv_filename, "w") # write data to the csv
        csvwriter1 = csv.writer(f1)

        f2 = open(final_csv, "a") # append data to the combined csv
        csvwriter2 = csv.writer(f2)

        univ_name = "University of New Brunswick"
        country = "Canada"

        garbage_emails = [] # add garbage emails to this list

        variables = [csvwriter1, csvwriter2, univ_name, country, garbage_emails]

        table = soup.find('table',{'class':'table table-striped table-responsive'})
        if table == None:
            print("Table not found")
            return
        
        profs = table.find_all('tr')
        for prof in profs:
            a = prof.find('a')
            if a == None:
                continue
            link = a.get('href')
            name = a.get_text().strip()
            print(name,link)
            try:
                prof_resp = requests.get(link)
            except:
                print("prof website not reached on time")
                continue
            email = "Not Found"
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
    brunswick()


            







        