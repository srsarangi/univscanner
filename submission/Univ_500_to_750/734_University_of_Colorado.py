import csv
import re
import time
import urllib
import urllib.request

import requests
from bs4 import BeautifulSoup


def colarado():
    url = "https://engineering.ucdenver.edu/computer-science-and-engineering/faculty-and-staff"
    response = requests.get(url)
    if response.status_code == 200:
        # scrappable
        soup = BeautifulSoup(response.text, "html.parser")
        csv_filename = "University of Colorado Denver.csv"
        final_csv = "combined.csv"
        
        f1 = open(csv_filename, "w") # write data to the csv
        csvwriter1 = csv.writer(f1)

        f2 = open(final_csv, "a") # append data to the combined csv
        csvwriter2 = csv.writer(f2)

        univ_name = "University of Colorado Denver"
        country = "United States"

        garbage_emails = [] # add garbage emails to this list

        variables = [csvwriter1, csvwriter2, univ_name, country, garbage_emails]

        d = soup.find('div', {'class': 't-list-widget t-expandedList people-list'})

        profs = d.find_all('div')

        for prof in profs:
            h3 = prof.find('h3', {'class': 'people-display-name'})
            if h3 == None:
                continue
            name = h3.get_text().strip()
            a = prof.find_all('a')
            if len(a) >= 2:
                email = a[0].get('href')[7:]
                link = a[1].get('href')
                print(name, link, email)
                try:
                    prof_resp = requests.get(link)
                except:
                    print("prof website not reached on time")
                    continue
                get_email(variables,garbage_emails,name,link,email,prof_resp)

        
        f1.close()
        f2.close()
        print("Finished")
    else:
        #print status code
        print(response.status_code)
        print("Error")
        



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
    print("searching....")
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
    colarado()



            







        