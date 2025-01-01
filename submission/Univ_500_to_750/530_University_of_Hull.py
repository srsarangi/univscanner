import requests
import urllib.request
import time
import urllib
import re
import csv
from bs4 import BeautifulSoup

def hull():
    url = "https://www.hull.ac.uk/faculties/departments/school-of-computer-science#top"
    response = requests.get(url)
    if response.status_code == 200:
        # scrappable
        soup = BeautifulSoup(response.text, "html.parser")
        csv_filename = "University of Hull.csv"
        final_csv = "combined.csv"
        
        f1 = open(csv_filename, "w") # write data to the csv
        csvwriter1 = csv.writer(f1)

        f2 = open(final_csv, "a") # append data to the combined csv
        csvwriter2 = csv.writer(f2)

        univ_name = "University of Hull"
        country = "United Kingdom"

        garbage_emails = [] # add garbage emails to this list

        variables = [csvwriter1, csvwriter2, univ_name, country, garbage_emails]
                # <a href="/staff-directory/baseer-ahmad" class="person" tabindex="0">
        #             <picture>
        #                 <source media="(max-width: 767px)" type="image/webp" src="/staff-directory/images/baseer-ahmad.jpg?w=50&amp;h=50&amp;fit=crop&amp;format=webp">
        #                 <source media="(max-width: 767px)" src="/staff-directory/images/baseer-ahmad.jpg?w=50&amp;h=50&amp;fit=crop">
        #                 <source type="image/webp" src="/staff-directory/images/baseer-ahmad.jpg?w=70&amp;h=70&amp;fit=crop&amp;format=webp">
        #                 <img alt="Baseer Ahmad" class="entered exited" role="presentation" loading="lazy" src="/staff-directory/images/baseer-ahmad.jpg?w=70&amp;h=70&amp;fit=crop">
        #             </picture>

        #             <div>
        #                 <h3 class="heading-4">
        #                     Baseer Ahmad
        #                 </h3>
        #                 <p></p>
        #             </div>
        #         </a>
        # 
        d = soup.find('div',{'class': 'staff-container'})
        if len(d) == 0:
            return 
        # get the above html element from d
        dd = d.find_all('a', {'class': 'person'})
        for i in dd:
            name = i.find('h3').get_text().strip()
            link = "https://www.hull.ac.uk"+ i.get('href')
            print(name, link)
            email = "Not Found"
            # check if link is valid or not
            try:
                prof_resp = requests.get(link)
            except:
                continue
            get_email(variables,garbage_emails,name,link,email,prof_resp)

                
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
    hull()



            







        