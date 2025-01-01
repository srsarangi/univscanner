import requests
import urllib.request
import time
import urllib
import re
import csv
from bs4 import BeautifulSoup

def bilkent(url):
    # url = "https://www.seas.harvard.edu/computer-science/faculty-research"
    response = requests.get(url)
    if response.status_code == 200:
        # scrappable
        soup = BeautifulSoup(response.text, "html.parser")
        csv_filename = "Bilkent University.csv"
        final_csv = "combined.csv"
        
        f1 = open(csv_filename, "a") # write data to the csv
        csvwriter1 = csv.writer(f1)

        f2 = open(final_csv, "a") # append data to the combined csv
        csvwriter2 = csv.writer(f2)

        univ_name = "Bilkent University"
        country = "Turkey"

        garbage_emails = [] # add garbage emails to this list

        variables = [csvwriter1, csvwriter2, univ_name, country, garbage_emails]
        # <p class="has-small-font-size"><a href="http://w3.cs.bilkent.edu.tr/en/wp-content/uploads/sites/3/2016/04/saksoy.jpg"></a>Prof. Dr. Selim Aksoy</p>
        # <p class="has-small-font-size">Email: <span class="e-mail" data-user="saksoy" data-website="cs.bilkent.edu.tr" style="text-decoration: none; color: black;"></span><br>Office: EA 422<br>Phone: (312) 290 3405<br><a href="http://www.cs.bilkent.edu.tr/~saksoy/">Homepage</a><br>Computer vision, statistical and structural pattern recognition, machine learning, data mining</p>

        # get the above html elements from soup
        d = soup.find_all('p', {'class': 'has-small-font-size'})
        # now get the elements two two at a time and deal both
        for i in range(0,len(d)-1,2):
            name = d[i].get_text().strip()
            #get link,email from d[i+1]\
            print(name)
            a = d[i+1].find('a')
            if a is None:
                break
            link = a.get('href')
            email = "Not Found"
            print(name, link)
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

    prof_soup = BeautifulSoup(page_resp.text, "html.parser")
    # key_words = ['BASE'] # base is used when there is no use of keywords
    key_words = ['operating systems','Embedded System','embedded system', 'Operating Systems','operating system','Operating System','embedded systems','embedded','Embedded',"Embedded Systems"]
    prof_text = prof_soup.text   # get the text from the page
    # print("prof_text: ",prof_text)

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
    url1 = "https://w3.cs.bilkent.edu.tr/faculty-members/"
    url2 = "https://w3.cs.bilkent.edu.tr/instructors/"
    url3 = "https://w3.cs.bilkent.edu.tr/part-time-instructors/"
    bilkent(url1)
    bilkent(url2)
    bilkent(url3)



            







        