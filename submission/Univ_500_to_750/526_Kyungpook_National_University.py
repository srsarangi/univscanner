import requests
import urllib.request
import time
import urllib
import re
import csv
from bs4 import BeautifulSoup

def kyungpook(url):
    # url = "https://www.seas.harvard.edu/computer-science/faculty-research"
    response = requests.get(url)
    if response.status_code == 200:
        # scrappable
        soup = BeautifulSoup(response.text, "html.parser")
        csv_filename = "Kyungpook National University.csv"
        final_csv = "combined.csv"
        
        f1 = open(csv_filename, "a") # write data to the csv
        csvwriter1 = csv.writer(f1)

        f2 = open(final_csv, "a") # append data to the combined csv
        csvwriter2 = csv.writer(f2)

        univ_name = "Kyungpook National University"
        country = "South Korea"

        garbage_emails = [] # add garbage emails to this list

        variables = [csvwriter1, csvwriter2, univ_name, country, garbage_emails]
        d = soup.find('div', {'class': 'professorAlbumList'})
        if len(d) == 0:
            return 
        dd = d.find_all('li')
        if len(dd) == 0:
            return 
        key_words = ['operating systems','Embedded System','embedded system', 'Operating Systems','operating system','Operating System','embedded systems',"Embedded Systems"]
        for i in dd:
            table = i.find('table')
            if table == None:
                continue
            info = table.find_all('td')
            email = "Not Found"
            if len(info) != 5:
                continue
            name = info[0].get_text()
            email = "Not Found"
            email_a = info[2].find('a')
            if email_a != None:
                email = email_a.get('href')
            #remove mailto:
            email = email[7:]
            research = "none"
            if info[4] != None:
                research = info[4].get_text()
            print(name, email)
            for word in key_words:
                
                if re.search(word,research,re.IGNORECASE):
                    print("matched_word: ",word)
                    csvwriter1.writerow([univ_name,country,name,email,url])
                    csvwriter2.writerow([univ_name,country,name,email,url])
                    break
        
        f1.close()
        f2.close()
        print("Finished")



def get_email(variables,garbage_emails,name,link,email,page_resp):
    csvwriter1, csvwriter2, univ_name, country, garbage_emails = variables
    if email != "Not Found": # if email is already found, no need to find it again (at line 50)
        # just write
        csvwriter1.writerow([univ_name,country,name,email,link])
        csvwriter2.writerow([univ_name,country,name,email,link])
        return
    prof_soup = BeautifulSoup(page_resp.text, "html.parser")
    key_words = ['BASE'] # base is used when there is no use of keywords
    # key_words = ['operating systems','Embedded System','embedded system', 'Operating Systems','operating system','Operating System','embedded systems',"Embedded Systems"]
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
    main_url = "https://see.knu.ac.kr/eng/content/member/professorAlbum.html?idx="
    s = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for i in range(26):
        kyungpook(main_url + s[i])
    



            







        