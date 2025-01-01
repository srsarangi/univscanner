import requests
import urllib.request
import time
import urllib
import re
import csv
from bs4 import BeautifulSoup


# JUST TEMPLATE 
def zayed(url):
    # url = ""
    return
    response = requests.get(url)
    if response.status_code == 200:
        # scrappable
        soup = BeautifulSoup(response.text, "html.parser")
        csv_filename = "Zayed University.csv"
        final_csv = "combined.csv"
        
        f1 = open(csv_filename, "w") # write data to the csv
        csvwriter1 = csv.writer(f1)

        f2 = open(final_csv, "a") # append data to the combined csv
        csvwriter2 = csv.writer(f2)

        univ_name = "Zayed University"
        country = "United Arab Emirates"

        garbage_emails = [] # add garbage emails to this list

        variables = [csvwriter1, csvwriter2, univ_name, country, garbage_emails]

        a = soup.find_all('a',{'class':'inside-media-body inside-media-admin'})
        # for prof in a:
        for i in a:
            link = "https://www.zu.ac.ae/main/en/colleges/colleges/__college_of_technological_innovation/faculty_and_staff/"+ i.get('href')
            # name = i.get_text().strip()
            # name = i.find('h3').get_text().strip()
            h4 = i.find('h4')
            if h4 == None:
                continue
            name = h4.get_text().strip()
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

    url1 = "https://www.zu.ac.ae/main/en/colleges/colleges/__college_of_technological_innovation/faculty_and_staff/index"
    url2 = ""
    url3 = ""
    url4 = ""
    zayed(url1)



            







        