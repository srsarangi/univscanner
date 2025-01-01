import requests
import urllib.request
import time
import urllib
import re
import csv
from bs4 import BeautifulSoup

def sunway(url):
    # url = "https://tpu.ru/en/about/department_links_and_administration/department/?q=&type=1"
    response = requests.get(url)
    if response.status_code == 200:
        # print("scrappable")
        # return
        # scrappable
        soup = BeautifulSoup(response.text, "html.parser")
        csv_filename = "Sunway University.csv"
        final_csv = "combined.csv"
        
        f1 = open(csv_filename, "a") # write data to the csv
        csvwriter1 = csv.writer(f1)

        f2 = open(final_csv, "a") # append data to the combined csv
        csvwriter2 = csv.writer(f2)

        univ_name = "Sunway University"
        country = "Malaysia"

        garbage_emails = ['info@sunway.edu.my'] # add garbage emails to this list

        variables = [csvwriter1, csvwriter2, univ_name, country, garbage_emails]
        d = soup.find('div', {'class': 'main-page-content'})
        if d == None:
            print("data not found")
            return False
        dd = d.find('div', {'class': 'view-content'})
        if dd == None:
            return False
        profs = dd.find_all('div', {'class': 'views-row'})
        if len(profs) == 0:
            return False
        for prof in profs:
            name_div = prof.find('div', {'class': 'hpfboxbody'})
            if name_div == None:
                continue
            h3 = name_div.find('h3')
            if h3 == None:
                continue
            a = h3.find('a')
            if a == None:
                continue
            name = a.get_text().strip()
            link = "https://sunwayuniversity.edu.my"+a.get('href')
            email = "Not Found"
            print(name,link)
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
    main_url = "https://sunwayuniversity.edu.my/staff-profiles/school/School%20of%20Engineering%20and%20Technology?page="

    # sunway()
    i =0
    while True:
        print("page: ",i)
        if not sunway(main_url+str(i)):
            break
        else:
            i+=1




            







        