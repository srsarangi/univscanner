import requests
import urllib.request
import time
import urllib
import re
import csv
from bs4 import BeautifulSoup

# JUST TEMPLATE
def pmu(url):
    url = "https://www.pmu.edu.sa/faculty_profile/_faculty_search?page=1"
    return
    response = requests.get(url)
    if response.status_code == 200:

        # scrappable
        soup = BeautifulSoup(response.text, "html.parser")
        csv_filename = "Prince Mohammad Bin Fahd university.csv"
        final_csv = "combined.csv"
        
        f1 = open(csv_filename, "w") # write data to the csv
        csvwriter1 = csv.writer(f1)

        f2 = open(final_csv, "a") # append data to the combined csv
        csvwriter2 = csv.writer(f2)

        univ_name = "Prince Mohammad Bin Fahd university"
        country = "Saudi Arabia"

        garbage_emails = [] # add garbage emails to this list

        variables = [csvwriter1, csvwriter2, univ_name, country, garbage_emails]
        # faculty_profile_t_brief
        d = soup.find_all('div', {'class': 'faculty_profile_t_brief'})
        if d == None:
            print("data not found")
            return False
        for prof in d:
            div = prof.find('span', {'class': 'faculty_name'})
            if div == None:
                continue
            name_div = div.find('a')
            if name_div == None:
                continue
            name = name_div.get_text().strip()



        
        
        f1.close()
        f2.close()
        print("Finished")
        return True
    else:
        #print status code
        print(response.status_code)
        print("Error")
        return False



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
    # key_words_spanish = ['sistemas operativos', 'sistema embebido', 'sistema embebido', 'Sistemas Operativos', 'sistema operativo', 'Sistema Operativo', 'sistemas embebidos', 'Sistemas Embebidos']

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
    # pmu("https://www.pmu.edu.sa/faculty_profile/_faculty_search?page=1")
    main_url = "https://www.pmu.edu.sa/faculty_profile/_faculty_search?page="
    i = 1
    while True:
        if not pmu(main_url + str(i)):
            break
        i += 1




            







        