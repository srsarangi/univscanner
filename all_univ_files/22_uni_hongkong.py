import requests
import urllib.request
import time
import urllib
import re
import csv
from bs4 import BeautifulSoup

url = "https://www.cs.hku.hk/people/academic-staff"   # homepage url
r = requests.get(url)                                        # request to url

# getting the soup by parsing the html parsel to text to request r
soup = BeautifulSoup(r.text, "html.parser")

# file initialization to write
filename = "uni_hongkong.txt"
f = open(filename, "w")

excel_filename = "uni_hongkong.csv"
f2 = open(excel_filename, "w")
csvwriter = csv.writer(f2)

overall_file = "all_emails.csv"
f3 = open(overall_file, "a")
csvwriter2 = csv.writer(f3)

u_name = "University of Hong Kong"
country = "Hong Kong"

# using set() to store to remove duplicates emails
emails = set()

# d gives the array of all profs on the dept homepage
# dd = soup.find('div', {'class':"row"})
d = soup.find_all('tr')
# print(d)

#iterating for every prof
for i in d:
    a = i.find('a')                     # a contains the name and the homepage of prof
    link = a.get('href')
    if link[0] == '/':
        link = 'https://www.cs.hku.hk'+link
    name = a.get_text()                 # extracting prof name

    print(link, "\t", name)
    try:
        prof_resp = requests.get(link)          # requesting prof homepgae
        prof_soup = BeautifulSoup(prof_resp.text, "html.parser") 
    except:
        continue

    keyword_list = ['Computer architecture','computer architecture','Computer Architecture', 'Hardware And System Architecture', 'hardware and system architecture', 
                'Hardware and Architecture', 'hardware and architecture', 'embedded system', 'Processor Architecture', 'processor architecture', 'Processor architecture', 'Distributed System']
    flag = 1
    research_text = prof_soup.text
    for pattern in keyword_list:
        if re.search(pattern,research_text):
            flag = 0
            new_emails = set(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}", prof_resp.text))
            # new_emails2 = set(re.findall(r"[A-Za-z0-9._%+-]+&nbsp;&nbsp;(&commat;[A-Za-z0-9.-]+\.[A-Za-z]{2,4}", prof_resp.text))
            # new_emails = new_emails + new_emails2
            grabage_emails = []
            for eemail in grabage_emails:
                if eemail in new_emails:
                    new_emails.remove(eemail)

            # f.write(link + '\n' + name)
            if len(new_emails) == 0:
                email = "Email Not Found"
                f.write(link + '\n' + name + "\t"+ email + "\n")
                csvwriter.writerow([u_name, country, name, email, link])
                csvwriter2.writerow([u_name, country, name, email, link])
            else:
                # f.write(link + '\n' + name)
                for email in new_emails:
                    f.write(link + '\n' + name + '\t\t' + email + '\n')
                    csvwriter.writerow([u_name, country, name, email, link])
                    csvwriter2.writerow([u_name, country, name, email, link])
                # f.write("\n") 

            f.write(pattern)
            f.write('\n\n')
            break


f.close()
f2.close()
f3.close()
print("Finished")

