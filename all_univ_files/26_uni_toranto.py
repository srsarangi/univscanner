import requests
import urllib.request
import time
import urllib
import re
import csv
from bs4 import BeautifulSoup

url = "https://web.cs.toronto.edu/contact-us/faculty-directory#teachingstream"   # homepage url
r = requests.get(url)                                        # request to url

# getting the soup by parsing the html parsel to text to request r
soup = BeautifulSoup(r.text, "html.parser")

# file initialization to write
filename = "uni_toranto.txt"
f = open(filename, "w")

excel_filename = "uni_toranto.csv"
f2 = open(excel_filename, "w")
csvwriter = csv.writer(f2)

overall_file = "all_emails.csv"
f3 = open(overall_file, "a")
csvwriter2 = csv.writer(f3)

u_name = "University of Totanto"
country = "Canada"

# using set() to store to remove duplicates emails
emails = set()

# d gives the array of all profs on the dept homepage
# d = soup.find('a', {'class':"accordian-title"})
d = soup.find_all('table', {'class':'blueTable'})
# dd = d.find_all('div', {'class': 'views-field views-field-title'})
# print(d)
#iterating for every prof
for i in d:
    dd = soup.find_all('tr')
    for ii in dd:
        if ii.find('a') == None:
            continue
        a = ii.find('a')                     # a contains the name and the homepage of prof
        link = a.get('href')                # extracting prof page link
        name = a.get_text()                 # extracting prof name
        if name == 'Stavros Tsogkasm':
            break
        # print(name, "\t", link)
        aa = a.find_next('a')
        mailto = aa['href']
        if mailto[0:6] == "mailto" :
            email = aa.get_text()
        else:
            email = "Not Found"

        print(name, '\t', email, '\t', link)
        try:
            prof_resp = requests.get(link)          # requesting prof homepgae
            prof_soup = BeautifulSoup(prof_resp.text, "html.parser") 
        except:
            continue

        keyword_list = ['Computer Architecture', 'computer architecture', 'Computer architecture', 'Embedded System', 'Embedded system', 'embedded system']
        flag = 1
        research_text = prof_soup.text
        for pattern in keyword_list:
            if re.search(pattern,research_text):
                flag = 0
                # f.write(link + '\n' + name + '\t\t' + email + '\n')
                # csvwriter.writerow([u_name, country, name, email, link])
                if email == "Not Found":
                    new_emails = set(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}", prof_resp.text))
                    if len(new_emails) == 0:
                        email = "Email Not Found"
                        f.write(link + '\n' + name + "\t"+ email + "\n")
                        csvwriter.writerow([u_name, country, name, email, link])
                        csvwriter2.writerow([u_name, country, name, email, link])
                    else:
                        for email in new_emails:
                            f.write(link + '\n' + name + '\t\t' + email + '\n')
                            csvwriter.writerow([u_name, country, name, email, link])
                            csvwriter2.writerow([u_name, country, name, email, link])
                else:
                    f.write(link + '\n' + name + '\t\t' + email + '\n')
                    csvwriter.writerow([u_name, country, name, email, link])
                    csvwriter2.writerow([u_name, country, name, email, link])

                f.write(pattern)
                f.write('\n\n')
                break
    else:
        continue  # only executed if the inner loop did NOT break
    break  # only executed if the inner loop DID break


f.close()
f2.close()
f3.close()
print("Finished")

