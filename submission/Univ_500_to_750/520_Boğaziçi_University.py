import requests
import urllib.request
import time
import urllib
import re
import csv
from bs4 import BeautifulSoup

def bogazici():
    return 
    url = ""
    response = requests.get(url)
    if response.status_code == 200:
        # scrappable
        soup = BeautifulSoup(response.text, "html.parser")
        csv_filename = "Boğaziçi University.csv"
        final_csv = "combined.csv"
        
        f1 = open(csv_filename, "w") # write data to the csv
        csvwriter1 = csv.writer(f1)

        f2 = open(final_csv, "a") # append data to the combined csv
        csvwriter2 = csv.writer(f2)

        univ_name = "Boğaziçi University"
        country = "Turkey"

        garbage_emails = [] # add garbage emails to this list

        variables = [csvwriter1, csvwriter2, univ_name, country, garbage_emails]
        # <div class="row row-cols-1 row-cols-xl-2 g-2 my-4

        # get the html element from soup
        d = soup.find_all('div',{'class':'row row-cols-1 row-cols-xl-2 g-2 my-4'})
#         <div class="col"><div class="card mb-3 border-0 h-100" style="max-width:540px"><div class="row g-0"><div class="col-4 mb-0 d d-none d-xl-block"><img src="/images/people/akarun_lale_hu4028428556839514370.webp" alt="lale-akarun-thumbnail" class="img-fluid rounded-5 shadow" style="width:100%;max-height:145px;object-fit:cover;object-position:center"></div><div class="col-8 align-middle" style="overflow-x:scroll;white-space:nowrap"><div class="card-body align-middle"><h5 class="my-2">Lale Akarun</h5><p class="mb-1">Professor</p><p class="d-block"><a href="mailto:akarun@bogazici.edu.tr" class="text-muted"><img src="/icons/envelope-fill.svg" alt="" width="24" height="24">
# </a><a href="/u/lale.akarun" class="text-muted"><img src="/icons/globe2.svg" alt="" width="24" height="24"></a></p></div></div></div></div></div>
        for i in d:
            dd = i.find_all('div',{'class':'col'})
            for j in dd:
                if j.find('h5',{'class':'my-2'}) == None:
                    continue
                h5 = j.find('h5',{'class':'my-2'})
                name = h5.get_text()
                a = j.find_all('a')
                if len(a) < 2:
                    continue
                email = a[0].get('href')
                # remove the prefix (mailto:)
                email = email.split(':')[-1].strip()

                link = a[1].get('href')
                
                link = "https://www.seas.harvard.edu"+ a.get('href')
                print(name, link)
                email = "Not Found"
                # check if link is valid or not
                try:
                    prof_resp = requests.get(link)
                except:
                    continue
                get_email(variables,garbage_emails,name,link,email,prof_resp)

        # GET DATA
        d = soup.find('a', text="Computer Engineering and Architecture").find_next('div')
        dd = d.find_all('div', {'class': 'views-field views-field-title'})

        #interating 0ver data

        for i in dd:
            if i.find('a') == None:
                continue
            a = i.find('a')
            link = "https://www.seas.harvard.edu"+ a.get('href')
            name = a.get_text()

            # check if link is valid or not
            try:
                prof_resp = requests.get(link)
            except:
                continue
            # start email as not found, if found keep the email
            email = "Not Found"
            print(name, link)
            get_email(variables,garbage_emails,name,link,email,prof_resp)
        
        f1.close()
        f2.close()
        print("Finished")



def get_email(variables,garbage_emails,name,link,email,page_resp):
    csvwriter1, csvwriter2, univ_name, country, garbage_emails = variables
    # if email != "Not Found": # if email is already found, no need to find it again (at line 50)
    #     # just write
    #     csvwriter1.writerow([univ_name,country,name,email,link])
    #     csvwriter2.writerow([univ_name,country,name,email,link])
    #     return
    prof_soup = BeautifulSoup(page_resp.text, "html.parser")
    # key_words = ['BASE'] # base is used when there is no use of keywords
    key_words = ['operating systems','Embedded System','embedded system', 'Operating Systems','operating system','Operating System','embedded systems','embedded','Embedded',"Embedded Systems"]
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
    bogazici()



            







        