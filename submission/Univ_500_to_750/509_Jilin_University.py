import requests
import urllib.request
import time
import urllib
import re
import csv
from bs4 import BeautifulSoup

def jilin():
    url = "https://cie.jlu.edu.cn/info/1235/2975.htm"
    response = requests.get(url)
    if response.status_code == 200:
        # scrappable
        soup = BeautifulSoup(response.text, "html.parser")
        csv_filename = "Jilin_University.csv"
        final_csv = "combined.csv"
        
        f1 = open(csv_filename, "w") # write data to the csv
        csvwriter1 = csv.writer(f1)

        f2 = open(final_csv, "a") # append data to the combined csv
        csvwriter2 = csv.writer(f2)

        univ_name = "Jilin University"
        country = "China (Mainland)"

        garbage_emails = [] # add garbage emails to this list

        variables = [csvwriter1, csvwriter2, univ_name, country, garbage_emails]
        #<p class="vsbcontent_start"><a href="../1233/2933.htm">ZHOU You</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <a href="../1233/2934.htm">LI Hongliang</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <a href="../1233/2936.htm">ZHANG Xiaoli</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <a href="../1233/2932.htm">ZHANG Hao</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <a href="../1233/2935.htm">ZHANG Meng</a></p>
        # get the html element from soup
        d = soup.find_all('p', {'class': 'vsbcontent_start'})
        for i in d:
            if i.find('a') == None:
                continue
            # get all the anchor elements
            dd = i.find_all('a')
            # iterate over the anchor elements
            for a in dd:
                name = a.get_text()
                link = "https://cie.jlu.edu.cn/info/"+a.get('href')

                print(name, link)
                email = "Not Found"
                # check if link is valid or not
                try:
                    # headers = {"Accept-Language": "en-US,en;q=0.9"}
                    # response = requests.get(url, headers=headers)
                    prof_resp = requests.get(link)
                except:
                    continue
                get_email(variables,garbage_emails,name,link,email,prof_resp)
        
        f1.close()
        f2.close()
        print("Finished")



def get_email(variables,garbage_emails,name,link,email,page_resp):
    csvwriter1, csvwriter2, univ_name, country, garbage_emails = variables
    print("Processing ",name)
    prof_soup = BeautifulSoup(page_resp.text, "html.parser")
    # key_words = ['BASE'] # base is used when there is no use of keywords
    key_words = ['operating systems','Embedded System','embedded system', 'Operating Systems','operating system','Operating System','embedded systems','embedded','Embedded',"Embedded Systems",'machine learning','Machine Learning']
    prof_text = prof_soup.text   # get the text from the page
    print("prof_text: ",prof_text)


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
    jilin()



            







        