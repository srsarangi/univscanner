import requests
import urllib.request
import time
import urllib
import re
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager



def cattolica():
    url = "https://dipartimenti.unicatt.it/dmf-staff-professori-e-ricercatori#content"
    response = requests.get(url)
    if response.status_code == 200:
        # scrappable
        soup = BeautifulSoup(response.text, "html.parser")
        csv_filename = "Università Cattolica del Sacro Cuore.csv"
        final_csv = "combined.csv"
        
        f1 = open(csv_filename, "w") # write data to the csv
        csvwriter1 = csv.writer(f1)

        f2 = open(final_csv, "a") # append data to the combined csv
        csvwriter2 = csv.writer(f2)

        univ_name = "Università Cattolica del Sacro Cuore"
        country = "Italy"

        garbage_emails = [] # add garbage emails to this list

        variables = [csvwriter1, csvwriter2, univ_name, country, garbage_emails]

    #     <li><strong><a href="http://docenti.unicatt.it/ita/roberto_auzzi"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Auzzi Roberto</font></font></a></strong><br>
	# <a href="mailto:roberto.auzzi@unicatt.it"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;"> roberto.auzzi@unicatt.it</font></font></a><font style="vertical-align: inherit;"><font style="vertical-align: inherit;"> - ​​Internal tel. 711</font></font><br><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">
	# Theoretical Physics</font></font></li>
        d = soup.find('div',{'class': 'standard-article'})
        dd = d.find_all('li')
        for i in dd:
            if i.find('a') == None:
                continue
            a = i.find('a')
            name = a.get_text()
            link = a.get('href')
            email = "Not Found"
            try:
                prof_resp = requests.get(link)
            except:
                continue
            print(name, link)
            get_email(variables,garbage_emails,name,link,email,prof_resp)
        # GET DATA
        
        
        f1.close()
        f2.close()
        print("Finished")



def get_email(variables,garbage_emails,name,link,email,page_resp):
    csvwriter1, csvwriter2, univ_name, country, garbage_emails = variables
    driver = webdriver.Chrome()

    if email != "Not Found": # if email is already found, no need to find it again (at line 50)
        # just write
        csvwriter1.writerow([univ_name,country,name,email,link])
        csvwriter2.writerow([univ_name,country,name,email,link])
        return
    
    driver.get(link)
    html = driver.page_source
    prof_soup = BeautifulSoup(html, "html.parser")
    prof_text = prof_soup.text
    # print(prof_soup)

    # key_words = ['BASE'] # base is used when there is no use of keywords
    key_words = ['operating systems','Embedded System','embedded system', 'Operating Systems','operating system','Operating System','embedded systems','embedded','Embedded',"Embedded Systems",'reinforcement']
    # prof_text = prof_soup.text   # get the text from the page
    # print(name)
    print(prof_text)
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
    cattolica()



            







        