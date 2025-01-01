import requests
import urllib.request
import time
import urllib
import re
import csv
from bs4 import BeautifulSoup

def thessaloniki():
    return 
    url = "https://ece.auth.gr/en/academic/"
    response = requests.get(url)
    if response.status_code == 200:
        # scrappable
        soup = BeautifulSoup(response.text, "html.parser")
        csv_filename = "Aristotle University of Thessaloniki.csv"
        final_csv = "combined.csv"
        
        f1 = open(csv_filename, "w") # write data to the csv
        csvwriter1 = csv.writer(f1)

        f2 = open(final_csv, "a") # append data to the combined csv
        csvwriter2 = csv.writer(f2)

        univ_name = "Aristotle University of Thessaloniki"
        country = "Greece"

        garbage_emails = ['info@ece.auth.gr'] # add garbage emails to this list

        variables = [csvwriter1, csvwriter2, univ_name, country, garbage_emails]
        #<div class="uc_post_grid_style_one_wrap ue_post_grid uc-items-wrapper"><div class="uc_post_grid_style_one_item ue_post_grid_item ue-item ">
        # get the html element from the soup
        d = soup.find('div', {'class': 'uc_post_grid_style_one_wrap ue_post_grid uc-items-wrapper'})
        dd = d.find_all('div', {'class': 'uc_post_grid_style_one_item ue_post_grid_item ue-item '})
        print(len(dd))
        for i in dd:
            email = "Not Found"
            #<div class="uc_post_title"><a href="https://ece.auth.gr/en/staff/minas-alexiadis/" target="_self"><div>Minas Alexiadis</div></a></div>
            div = i.find('div', {'class': 'uc_post_title'})
            a = div.find('a')
            name = a.get_text()
            link = a.get('href')
            print(name, link)
            try:
                prof_resp = requests.get(link)
            except:
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
    key_words = ['operating systems','Embedded System','embedded system', 'Operating Systems','operating system','Operating System','embedded systems',"Embedded Systems"]
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
    thessaloniki()



            







        