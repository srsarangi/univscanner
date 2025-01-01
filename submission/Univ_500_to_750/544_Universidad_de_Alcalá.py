import requests
import urllib.request
import time
import urllib
import re
import csv
from bs4 import BeautifulSoup

def alcala():
    url = "https://www.uah.es/en/conoce-la-uah/campus-centros-y-departamentos/departamentos/Computer-Science/"
    response = requests.get(url)
    if response.status_code == 200:
        # scrappable
        soup = BeautifulSoup(response.text, "html.parser")
        csv_filename = "Universidad de Alcalá.csv"
        final_csv = "combined.csv"
        
        f1 = open(csv_filename, "w") # write data to the csv
        csvwriter1 = csv.writer(f1)

        f2 = open(final_csv, "a") # append data to the combined csv
        csvwriter2 = csv.writer(f2)

        univ_name = "Universidad de Alcalá"
        country = "Spain"

        garbage_emails = ['info@uah.es'] # add garbage emails to this list

        variables = [csvwriter1, csvwriter2, univ_name, country, garbage_emails]
        id = ['af','gl','ms','tz']
        d = []
        for i in id:
            e = soup.find('div',{'id':i})
            if e:
                d.append(e)
        # <div class="col-md-6">
		# <p><a href="/en/estudios/profesor/Javier-Albert-Segui/">Albert Segui, Javier</a></p>
		#</div>
        for i in d:

            dd = i.find_all('div', {'class': 'col-md-6'})
            for j in dd:
                a = j.find('a')
                if a == None:
                    continue
                name = a.get_text()
                link = "https://www.uah.es"+ a.get('href')
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
    # key_words = ['operating systems','Embedded System','embedded system', 'Operating Systems','operating system','Operating System','embedded systems',"Embedded Systems"]
    key_words_spanish = ['sistemas operativos', 'sistema embebido', 'sistema embebido', 'Sistemas Operativos', 'sistema operativo', 'Sistema Operativo', 'sistemas embebidos', 'Sistemas Embebidos']

    prof_text = prof_soup.text   # get the text from the page
    # print(prof_text)
    for word in key_words_spanish:
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
    alcala()



            







        