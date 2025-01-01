import requests
import urllib.request
import time
import urllib
import re
import csv
from bs4 import BeautifulSoup

def uit(url):
    # url = ""
    response = requests.get(url)
    if response.status_code == 200:
        # scrappable

        soup = BeautifulSoup(response.text, "html.parser")
        csv_filename = "University of Tromsø The Arctic University of Norway.csv"
        final_csv = "combined.csv"
        
        f1 = open(csv_filename, "a") # write data to the csv
        csvwriter1 = csv.writer(f1)

        f2 = open(final_csv, "a") # append data to the combined csv
        csvwriter2 = csv.writer(f2)

        univ_name = "University of Tromsø The Arctic University of Norway"
        country = "Norway"

        garbage_emails = [] # add garbage emails to this list

        variables = [csvwriter1, csvwriter2, univ_name, country, garbage_emails]

        d = soup.find('div', {'class': 'container divide30'})
        if d == None:
            print("data not found")
            return False
        
        dd = d.find_all('div', {'class': 'col-md-12'})
        if len(dd) <= 1:
            return False
        for i in dd:
            div = i.find('div', {'class': 'col-md-3 col-xs-12'})
            if div == None:
                continue
            h3 = div.find('h3')
            if h3 == None:
                continue
            name = h3.get_text().strip()
            a = h3.find('a')
            if a == None:
                continue
            link = "https://en.uit.no"+a.get('href')
            email = "Not Found"
            email_div = i.find('div', {'style':'margin-bottom:10px;'})
            if email_div == None:
                continue
            email_a = email_div.find('a')
            if email_a != None:
                email = email_a.get_text().strip()
            print(name,link,email)
            # return 
            try:
                prof_resp = requests.get(link)
            except:
                print("prof website not reached on time")
                continue
            get_email(variables,garbage_emails,name,link,email,prof_resp)





        f1.close()
        f2.close()
        print("Finished")
        return True
    else:
        #print status code
        print(response.status_code)
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
    main_url = "https://en.uit.no/enhet/ifi/ansatte?p_dimension_id=88138&ikbAction=ikb4&ikb4.startrow="
    i = 1
    # uit(main_url+str(i))
    while True:
        print("page: ",i)
        if not uit(main_url+str(i)):
            break
        else:
            i += 10



            







        