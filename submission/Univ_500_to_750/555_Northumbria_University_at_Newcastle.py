import requests
import urllib.request
import time
import urllib
import re
import csv
from bs4 import BeautifulSoup

def northumbria(url):
    # url = ""
    response = requests.get(url)
    if response.status_code == 200:
        # scrappable
        soup = BeautifulSoup(response.text, "html.parser")
        csv_filename = "Northumbria University at Newcastle.csv"
        final_csv = "combined.csv"
        
        f1 = open(csv_filename, "a") # write data to the csv
        csvwriter1 = csv.writer(f1)

        f2 = open(final_csv, "a") # append data to the combined csv
        csvwriter2 = csv.writer(f2)

        univ_name = "Northumbria University at Newcastle"
        country = "United Kingdom"

        garbage_emails = [] # add garbage emails to this list

        variables = [csvwriter1, csvwriter2, univ_name, country, garbage_emails]
        d = soup.find('div', {'class': 'row people-grid'})
        if d == None:
            print("No data found")
            return False
        dd = d.find_all('div',{'class':'span3'})
        if len(dd) == 0:
            print("No data found")
            return False
        for i in dd:
            prof = i.find('article',{'class':'rich-text'})
            if prof == None:
                continue
            name_div = prof.find('h2')
            if name_div == None:
                continue
            name = name_div.get_text()
            link = "https://www.northumbria.ac.uk"+name_div.find('a').get('href')
            email = "Not Found"
            email_p = prof.find('p',{'class':'email'})
            if email_p != None:
                email_a = email_p.find('a')
                if email_a != None:
                    email = email_a.get('href')[7:]
            print(name, link,email)
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
    prof_d = prof_soup.find('div',{'class':'component-container content'})
    prof_text = "empty"
    if prof_d != None:
        prof_text = prof_d.text  # get the text from the page

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
    # northumbria()
    # https://www.northumbria.ac.uk/about-us/our-staff/?sec=computer%20and%20information%20sciences&page=1#result-listing"
    prefix = "https://www.northumbria.ac.uk/about-us/our-staff/?sec=computer%20and%20information%20sciences&page="
    sufix = "#result-listing"

    i = 1
    while True:
        if not northumbria(prefix+str(i)+sufix):
            break
        else:
            print("Page :",i)
            i += 1




            







        