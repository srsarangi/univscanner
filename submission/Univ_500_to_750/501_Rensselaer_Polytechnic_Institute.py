import requests
import urllib.request
import time
import urllib
import re
import csv
from bs4 import BeautifulSoup

def rpi(url):
    # url = "https://faculty.rpi.edu/departments/computer-science?page=1"
    response = requests.get(url)
    if response.status_code == 200:
        # scrappable
        soup = BeautifulSoup(response.text, "html.parser")
        csv_filename = "Rensselaer_Polytechnic_Institute.csv"
        final_csv = "combined.csv"
        
        f1 = open(csv_filename, "a") # write data to the csv
        csvwriter1 = csv.writer(f1)

        f2 = open(final_csv, "a") # append data to the combined csv
        csvwriter2 = csv.writer(f2)

        univ_name = "Rensselaer Polytechnic Institute"
        country = "United States"

        garbage_emails = [] # add garbage emails to this list

        variables = [csvwriter1, csvwriter2, univ_name, country, garbage_emails]

        # <div class="views-field views-field-title"><span class="field-content sans-alt red text-uppercase"><a href="/alex-gittens" hreflang="en">Alex Gittens</a></span></div>
        # get the above html element from soup
        d = soup.find_all('div', {'class': 'views-field views-field-title'})
        if len(d) == 0:
            return False
        for i in d:
            if i.find('a') == None:
                continue
            a = i.find('a')
            link = "https://faculty.rpi.edu"+ a.get('href')
            name = a.get_text()
            try:
                prof_resp = requests.get(link)
            except:
                continue
            email = "Not Found"
            print(name, link)
            get_email(variables,garbage_emails,name,link,email,prof_resp)

        # # GET DATA
        # d = soup.find('a', text="Computer Engineering and Architecture").find_next('div')
        # dd = d.find_all('div', {'class': 'views-field views-field-title'})

        #interating 0ver data
        
        f1.close()
        f2.close()
        print("Finished")
        return True
    
    return False



def get_email(variables,garbage_emails,name,link,email,page_resp):
    csvwriter1, csvwriter2, univ_name, country, garbage_emails = variables
    
    prof_soup = BeautifulSoup(page_resp.text, "html.parser")
    
    key_words = ['operating systems','Embedded System','embedded system', 'Operating Systems','operating system','Operating System','embedded systems','embedded','Embedded',"Embedded Systems"] # base is used when there is no use of keywords
    prof_text = prof_soup.text   # get the text from the page

    for word in key_words:
        if re.search(word,prof_text,re.IGNORECASE) or word == 'BASE':
            print("matched_word: ",word)
            if email != "Not Found": # if email is already found, no need to find it again (at line 50)
                # just write
                csvwriter1.writerow([univ_name,country,name,email,link])
                csvwriter2.writerow([univ_name,country,name,email,link])
            else:
                new_emails = list(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}", prof_text))
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
    url="https://faculty.rpi.edu/departments/computer-science?page="
    # go from page 0 in url till it is valid
    i=0
    while True:
        url_link = url+str(i)
        # check if the url is valid
        # response = requests.get(url_link)
        
        if not rpi(url_link):
            break
        print("Finished ", i)
        i += 1

    # rpi()



            







        