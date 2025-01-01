import requests
import urllib.request
import time
import urllib
import re
import csv
from bs4 import BeautifulSoup

def sabanci():
    url = "https://fens.sabanciuniv.edu/en/faculty-members"
    
    response = requests.get(url)
    if response.status_code == 200:
        # scrappable
        soup = BeautifulSoup(response.text, "html.parser")
        csv_filename = "Sabanci University.csv"
        final_csv = "combined.csv"
        
        f1 = open(csv_filename, "w") # write data to the csv
        csvwriter1 = csv.writer(f1)

        f2 = open(final_csv, "a") # append data to the combined csv
        csvwriter2 = csv.writer(f2)

        univ_name = "Sabanci University"
        country = "Turkey"

        garbage_emails = [] # add garbage emails to this list

        variables = [csvwriter1, csvwriter2, univ_name, country, garbage_emails]

        d = soup.find('div', {'class': 'container'})

        # <div class="col-xl-3 col-lg-4 col-md-6 col-12">
        #                                 <div class="card-wrapper">
        #                 <a href="https://fens.sabanciuniv.edu/en/faculty-members/detail/552">
        #                     <figure class="card-picture" style="background-image:url('//www.sabanciuniv.edu/rehber/fotograflar/other/552.jpg')"></figure>
        #                     <div class="card-body">
        #                         <span class="card-title"> Erkay  Savaş</span>
        #                         <span class="card-job">Dean</span>
        #                         <span class="card-phone"><i class="fas fa-phone-alt"></i>(216) 483 9501</span>
        #                         <span class="card-mail"><i class="fas fa-envelope"></i>erkay<span class="dot"></span>savas<span class="at"></span>sabanciuniv<span class="dot"></span>edu</span>
        #                         <div class="card-research">
        #                                                                     <span>Research Area</span>
        #                                 <p>Cryptography and Security, Computer Aritmetic, High Perfomance Computing,Distributed Computing.</p>
        #                                                             </div>
        #                     </div>
        #                 </a>
        #             </div>
        #         </div>
        # get the html element from d 
        dd = d.find_all('div', {'class': 'col-xl-3 col-lg-4 col-md-6 col-12'})
        print(len(dd))
        if len(dd) == 0:
            return 
        for i in dd:
            #get name, link, email
            a = i.find('a')
            if a == None:
                continue
            link = a.get('href')
            name = a.find('span', {'class': 'card-title'}).get_text()
            email = "Not Found"
            # get the email
            email_span = a.find('span', {'class': 'card-mail'})
            if email_span != None:
                # email = email_span.text
                # Regular expression to find non-empty text between > and <
                pattern = r'>([^<>]+)<'

                # Find all matches
                matches = re.findall(pattern, str(email_span))
                # last two are domain and tds
                if len(matches) > 2:
                    # prefix except the last two add the remaining with "."
                    prefix = matches[0]
                    for i in range(1,len(matches)-2):
                        prefix += "." + matches[i]
                    email = prefix + "@" + matches[-2] + "." + matches[-1]
                
                    
            print(name, link, email)
            # return 
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
    sabanci()



            







        