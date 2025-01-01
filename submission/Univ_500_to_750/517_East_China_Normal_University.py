import requests
import urllib.request
import time
import urllib
import re
import csv
from bs4 import BeautifulSoup

def ecnu():
    url = "http://www.cs.ecnu.edu.cn/jzgml/list.htm"
    # covert the language to english
    headers = {
    "Accept-Language": "en-US,en;q=0.9"  # English (US) preferred, fallback to general English
    }
    response = requests.get(url,headers=headers)
    if response.status_code == 200:
        # scrappable
        soup = BeautifulSoup(response.text, "html.parser")
        csv_filename = "East China Normal University.csv"
        final_csv = "combined.csv"
        
        f1 = open(csv_filename, "w") # write data to the csv
        csvwriter1 = csv.writer(f1)

        f2 = open(final_csv, "a") # append data to the combined csv
        csvwriter2 = csv.writer(f2)

        univ_name = "East China Normal University"
        country = "China (Mainland)"

        garbage_emails = [] # add garbage emails to this list

        variables = [csvwriter1, csvwriter2, univ_name, country, garbage_emails]
#         <div class="li-text pull-right">
#                                             <p style="margin-bottom: 20px;font-size:16px;">
#                                                 <span style="font-size:16px;"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Name: </font></font></span><a href="https://faculty.ecnu.edu.cn/_s16/cq2_21262/main.psp" target="_blank" title="Chen Qin"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Chen Qin</font></font></a>
#                                             </p>
#                                             <div class="intro">
#                                                 <p><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">
#                                                     Title: Young Researcher </font></font><br><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">
# Office: Science Building 702B </font></font><br><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">
# Office Phone: </font></font><br><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">
# Email: qchen@cs.ecnu.edu.cn
#                                                 </font></font></p>
#                                             </div>
#                                         </div>
        # get the html element
        d = soup.find_all('div', {'class': 'li-text pull-right'})
        for i in d:
            if i.find('a') == None:
                continue
            a = i.find('a')
            name = a.get_text()
            link = a.get('href')
            div = i.find('div', {'class': 'intro'})
            # print(e_div)
            # Extract the email
            email = "Not Found"
            if div:
                text = div.get_text()  # Get all the text within the div
                for line in text.splitlines():  # Split the text by lines
                    if "Email:" in line:  # Check if the line contains "Email:"
                        email = line.split("Email:")[-1].strip()  # Extract and clean the email
                        break
            try:
        
                prof_resp = requests.get(link)
            except:
                continue
            print(name, link,email)
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
    ecnu()



            







        