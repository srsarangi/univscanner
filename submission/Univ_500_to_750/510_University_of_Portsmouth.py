import requests
import urllib.request
import time
import urllib
import re
import csv
from bs4 import BeautifulSoup

def portsmouth(url):
    # url = "https://www.port.ac.uk/about-us/structure-and-governance/our-people/our-staff?page=1"
    response = requests.get(url)
    return
    if response.status_code == 200:
        # scrappable
        soup = BeautifulSoup(response.text, "html.parser")
        csv_filename = "University_of_Portsmouth.csv"
        final_csv = "combined.csv"
        
        f1 = open(csv_filename, "a") # write data to the csv
        csvwriter1 = csv.writer(f1)

        f2 = open(final_csv, "a") # append data to the combined csv
        csvwriter2 = csv.writer(f2)

        univ_name = "University of Portsmouth"
        country = "United States"

        garbage_emails = [] # add garbage emails to this list

        variables = [csvwriter1, csvwriter2, univ_name, country, garbage_emails]
        
        d = soup.find_all('div',{'class': 'search-results'})
        flag = False
        print(len(d))
        for div in d:
            dd = div.find_all('li')
            print(len(dd))
            if len(dd) != 0:
                flag = True
                for i in dd:
                    if i.find('h2') == None or i.find('a') == None:
                        continue
                    a = i.find('h2')
                    name = a.get_text()
                    a = i.find('a')
                    link = "https://www.port.ac.uk/"+a.get('href')
                    print(name, link)
                    email = "Not Found"
                    # check if link is valid or not
                    try:
                        prof_resp = requests.get(link)
                    except:
                        continue
                    get_email(variables,garbage_emails,name,link,email,prof_resp)
        if not flag:
            return False
        f1.close()
        f2.close()
        print("Finished")
        return True
    return False



def get_email(variables,garbage_emails,name,link,email,page_resp):
    csvwriter1, csvwriter2, univ_name, country, garbage_emails = variables
    if email != "Not Found": # if email is already found, no need to find it again (at line 50)
        # just write
        csvwriter1.writerow([univ_name,country,name,email,link])
        csvwriter2.writerow([univ_name,country,name,email,link])
        return
    prof_soup = BeautifulSoup(page_resp.text, "html.parser")
    key_words = ['BASE'] # base is used when there is no use of keywords
    # key_words = ['operating systems','Embedded System','embedded system', 'Operating Systems','operating system','Operating System','embedded systems','embedded','Embedded',"Embedded Systems"]
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
    main_url = "https://www.port.ac.uk/about-us/structure-and-governance/our-people/our-staff?page="
    i = 0
    while True:
        i += 1
        url = main_url+str(i)
        print("page: ",i)
        if not portsmouth(url):
            break

    # portsmouth()



            







        