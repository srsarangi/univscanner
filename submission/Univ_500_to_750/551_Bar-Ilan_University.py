import requests
import urllib.request
import time
import urllib
import re
import csv
from bs4 import BeautifulSoup

def ilan():
    url = "https://cs.biu.ac.il/faculty"
    response = requests.get(url)
    if response.status_code == 200:
        # scrappable
        soup = BeautifulSoup(response.text, "html.parser")
        csv_filename = "Bar-Ilan University.csv"
        final_csv = "combined.csv"
        
        f1 = open(csv_filename, "w") # write data to the csv
        csvwriter1 = csv.writer(f1)

        f2 = open(final_csv, "a") # append data to the combined csv
        csvwriter2 = csv.writer(f2)

        univ_name = "Bar-Ilan University"
        country = "Israel"

        garbage_emails = [] # add garbage emails to this list

        variables = [csvwriter1, csvwriter2, univ_name, country, garbage_emails]
        d = soup.find('div',{'class':'field__item field__item-label-hidden'})
        dd = d.find_all('div', {'class': 'content'})
        # print(len(dd))
        #<div class="views-field views-field-field-person-email"><div class="field-content"><a href="mailto:marina.kogan-sadetsky@biu.ac.il">marina.kogan-sadetsky@biu.ac.il</a></div></div>
        
        for i in dd:
            profs = i.find_all('li')
            for j in profs:
                name = j.find('h3').get_text().strip()
                # link = "https://cs.biu.ac.il"+j.find('a').get('href')
                link = "https://cs.biu.ac.il"+j.find('h3').find('a').get('href')
                email = "Not Found"
                # print(name, link)
                try:
                    prof_resp = requests.get(link)
                except:
                    print("prof website not reached on time")
                    continue
                # start email as not found, if found keep the email
                # get the above element from j
                if j.find('div',{'class':'views-field views-field-field-person-email'}) != None:

                    if j.find('div',{'class':'views-field views-field-field-person-email'}).find('a') != None:
                        email = j.find('div',{'class':'views-field views-field-field-person-email'}).find('a').get('href')[7:]
                print(name, link, email)
                get_email(variables,garbage_emails,name,link,email,prof_resp)
                
                


        # GET DATA
        
        f1.close()
        f2.close()
        print("Finished")
    else:
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
    ilan()



            







        