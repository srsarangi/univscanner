import requests
import urllib.request
import time
import urllib
import re
import csv
from bs4 import BeautifulSoup

def ajou():
    url = "https://www.ajou.ac.kr/ict_en/faculty/faculty.do#a"
    response = requests.get(url)
    if response.status_code == 200:
        # scrappable
        soup = BeautifulSoup(response.text, "html.parser")
        csv_filename = "Ajou University .csv"
        final_csv = "combined.csv"
        
        f1 = open(csv_filename, "w") # write data to the csv
        csvwriter1 = csv.writer(f1)

        f2 = open(final_csv, "a") # append data to the combined csv
        csvwriter2 = csv.writer(f2)

        univ_name = "Ajou University"
        country = "South Korea"

        garbage_emails = [] # add garbage emails to this list

        variables = [csvwriter1, csvwriter2, univ_name, country, garbage_emails]

        # GET DATA
        
        # dp-faculty-list faculuty-list-type01
        d = soup.find('ul', {'class': 'dp-faculty-list faculuty-list-type01'})
        if d == None:
            print("data not found")
            return False
        i = 0
        key_words = ['operating systems','Embedded System','embedded system', 'Operating Systems','operating system','Operating System','embedded systems',"Embedded Systems",'kernel','Microcontroller Systems','Integrated Systems','Embedded Computing','Embedded Software','Distributed Systems']

        while True:
            data_idx = str(i)
            i += 1
            dd = d.find('li',{'data-idx':data_idx})
            if dd == None:
                break
            name_div = dd.find('span',{'class':'faculty-name-eng'})
            if name_div == None:
                continue
            name = name_div.get_text().strip()
            li = dd.find('li',{'class':'desc-input-email desc-input'})
            email = "Not Found"
            if li != None:
                email = li.get_text().strip()
            a = dd.find('a')
            if a == None:
                continue
            link = "https://www.ajou.ac.kr/ict_en/faculty/faculty."+ a.get('href')
            print(name,link,email)
            research = dd.find('li',{'class':'desc-input-interests desc-input'})
            if research != None:
                research = research.get_text()
                for word in key_words:
                    if re.search(word,research,re.IGNORECASE):
                        print("matched_word: ",word)
                        csvwriter1.writerow([univ_name,country,name,email,link])
                        csvwriter2.writerow([univ_name,country,name,email,link])
                        break
            
            
            
            # get_email(variables,garbage_emails,name,link,email,prof_resp)

            # i += 1


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
    key_words = ['operating systems','Embedded System','embedded system', 'Operating Systems','operating system','Operating System','embedded systems',"Embedded Systems",'kernel','Microcontroller Systems','Integrated Systems','Embedded Computing','Embedded Software','Distributed Systems']
    # key_words_spanish = ['sistemas operativos', 'sistema embebido', 'sistema embebido', 'Sistemas Operativos', 'sistema operativo', 'Sistema Operativo', 'sistemas embebidos', 'Sistemas Embebidos']

    prof_text = prof_soup.text   # get the text from the page
    # print('enterd
    # ')
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
    ajou()



            







        