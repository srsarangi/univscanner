import requests
import urllib.request
import time
import urllib
import re
import csv
from bs4 import BeautifulSoup

def ulster():
    url = "https://www.ulster.ac.uk/research/topic/computer-science/people"
    response = requests.get(url)
    if response.status_code == 200:
        # scrappable
        soup = BeautifulSoup(response.text, "html.parser")
        csv_filename = "Ulster_University.csv"
        final_csv = "combined.csv"
        
        f1 = open(csv_filename, "w") # write data to the csv
        csvwriter1 = csv.writer(f1)

        f2 = open(final_csv, "a") # append data to the combined csv
        csvwriter2 = csv.writer(f2)

        univ_name = "Ulster University"
        country = "United Kingdom"

        garbage_emails = [] # add garbage emails to this list

        variables = [csvwriter1, csvwriter2, univ_name, country, garbage_emails]
    #     <a href="https://ulster-search.clients.uk.funnelback.com/s/redirect?collection=ulster-people&amp;url=https%3A%2F%2Fwww.ulster.ac.uk%2Fstaff%2Fa-adebayo&amp;auth=oniep0sxXtHRcYYK22F%2FZg&amp;profile=_default&amp;rank=2&amp;query=researchorgcode%3A+%22RI_CS%22" class="title-container">
    #       <h3> Abiodun Adebayo</h3>
    #           <span class="job-title">Research Associate in Data Science</span>
    #       <div class="hide-for-small-only">
    #           <p><span><span class="fa-building fa-thin" aria-hidden="true"></span></span> School of Computing, Eng &amp; Intel. Sys</p>
    #           <p><span><span class="fa-map-marker fa-thin" aria-hidden="true"></span></span> Magee</p>
    #           <p><span><span class="fa-search fa-thin" aria-hidden="true"></span></span> MS020</p>
    #       </div>
    #    </a>
        # get the above html element from soup
        d = soup.find_all('a', {'class': 'title-container'})
        print(len(d))
        for i in d:
            if i.find('h3') == None:
                continue
            a = i.find('h3')
            name = a.get_text().strip
            link = i.get('href')
            print(name, link)
            email = "Not Found"
            # check if link is valid or not
            try:
                prof_resp = requests.get(link)
            except:
                continue
            get_email(variables,garbage_emails,name,link,email,prof_resp)
        # GET DATA
        
        
        f1.close()
        f2.close()
        print("Finished")



def get_email(variables,garbage_emails,name,link,email,page_resp):
    csvwriter1, csvwriter2, univ_name, country, garbage_emails = variables
    
    prof_soup = BeautifulSoup(page_resp.text, "html.parser")
    # key_words = ['BASE'] # base is used when there is no use of keywords
    key_words = ['operating systems','Embedded System','embedded system', 'Operating Systems','operating system','Operating System','embedded systems','embedded','Embedded',"Embedded Systems"]
    prof_text = prof_soup.text   # get the text from the page

    for word in key_words:
        if re.search(word,prof_text) or word == 'BASE':
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
    ulster()



            







        