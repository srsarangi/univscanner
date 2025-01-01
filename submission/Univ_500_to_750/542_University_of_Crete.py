import requests
import urllib.request
import time
import urllib
import re
import csv
from bs4 import BeautifulSoup

def crete():
    url = "https://www.csd.uoc.gr/CSD/index.jsp?content=academic_staff&lang=en"
    response = requests.get(url)
    if response.status_code == 200:
        # scrappable
        soup = BeautifulSoup(response.text, "html.parser")
        csv_filename = "University of Crete.csv"
        final_csv = "combined.csv"
        
        f1 = open(csv_filename, "w") # write data to the csv
        csvwriter1 = csv.writer(f1)

        f2 = open(final_csv, "a") # append data to the combined csv
        csvwriter2 = csv.writer(f2)

        univ_name = "University of Crete"
        country = "Greece"

        garbage_emails = [] # add garbage emails to this list

        variables = [csvwriter1, csvwriter2, univ_name, country, garbage_emails]
        d = soup.find('div', {'id': 'content'})
        if d == None:
            # print("Error")
            return
        dd = d.find_all('div', {'class': 'position-group'})
        # print(len(dd))
        # <div class="person" people_id="1">
        #         <div class="small_title">Antonis Argyros</div>
        #         <div class="person_text">
        #             <div class="person_image" style="background-image: url(uploaded_files/people/argyros.jpg);"></div>
        #             He received his PhD in 1996 from the Computer Science Department, University of Crete. He has been a postdoctoral research at the Royal Institute of Technology (KTH), in Stockholm, Sweden. His research interests include the areas of computer vision and pattern recognition with emphasis on 3D reconstruction, motion perception and tracking, analysis of the geometry and motion of the human body as well as human action and gesture recognition based on visual information.&nbsp; He is also interested in applications of computer vision in the fields of robotics and smart environments.
        #         </div>
        #         <div class="person_contact">
                    
                        
        #                 <div class="person_email_container"><img class="icon" src="images/at-icon.png" title="Email address"><span><a href="mailto:argyros@csd.uoc.gr">argyros@csd.uoc.gr</a></span></div>
                    
        #                 <div><img class="icon" src="images/link-icon.png" title="Personal Website"><a target="_blank" href="http://www.csd.uoc.gr/~argyros">Personal Website</a></div>
                    
        #         </div>
        #     </div>
        for i in dd:
            persons = i.find_all('div', {'class': 'person'})
            # print(len(persons))
            for person in persons:
                # get name ,link , email
                name = person.find('div', {'class': 'small_title'}).get_text().strip()
                info = person.find('div', {'class': 'person_contact'})
                email_div = info.find('div',{'class':'person_email_container'})
                # AT with @ and DOT with .
                email = "Not Found"
                if email_div.find('span') == None:
                    continue
                email = email_div.find('span').get_text().replace(' AT ','@').replace(' DOT ','.')
                if info.find('a') == None:
                    continue
                link = info.find('a').get('href')
                print(name,email,link)
                try:
                    prof_resp = requests.get(link)
                except:
                    print("prof website not reached")
                    continue
                # print(name,email,link)
                get_email(variables,garbage_emails,name,link,email,prof_resp)
                # check if link is valid or not

        # GET DATA
        
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
    crete()



            







        