import requests
import urllib.request
import time
import urllib
import re
import csv
from bs4 import BeautifulSoup

url = "https://www.cs.mcgill.ca/people/faculty/"   # homepage url
r = requests.get(url)                                        # request to url

# getting the soup by parsing the html parsel to text to request r
soup = BeautifulSoup(r.text, "html.parser")

# file initialization to write
filename = "mcgill_university.txt"
f = open(filename, "w")

excel_filename = "mcgill_university.csv"
f2 = open(excel_filename, "w")
csvwriter = csv.writer(f2)

overall_file = "all_emails.csv"
f3 = open(overall_file, "a")
csvwriter2 = csv.writer(f3)

u_name = "McGill University"
country = "Canada"

# using set() to store to remove duplicates emails
emails = set()

# d gives the array of all profs on the dept homepage
# d = soup.find('a', {'class':"accordian-title"})
# dd = soup.find('div', {'class':'panel-body'})
d = soup.find_all('div', {'class':'col-md-6'})

# print(d)  

#iterating for every prof
for i in d:
    h = i.find('h4')                     # a contains the name and the homepage of prof
    name = h.get_text()

    a = i.find('a', text='Website')
    link = a.get('href')
    name = name.replace("\t", "")
    name = name.replace("\n", "")
    try:
        prof_resp = requests.get(link)          # requesting prof homepgae
        prof_soup = BeautifulSoup(prof_resp.text, "html.parser") 
    except:
        continue

    print(name, link)

    keyword_list = ['Computer architecture','computer architecture','Computer Architecture', 'Hardware And System Architecture', 'hardware and system architecture', 
                'Hardware and Architecture', 'hardware and architecture', 'embedded system', 'Embedded System','Computer Organization','VLSI', 'Computer and System']
    flag = 1
    research_text = prof_soup.text
    for pattern in keyword_list:
        if re.search(pattern,research_text):
            flag = 0
            new_emails = set(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}", prof_resp.text))
            grabage_emails = ['hv@cs.mcgill.ca']
            for eemail in grabage_emails:
                if eemail in new_emails:
                    new_emails.remove(eemail)
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
                f.write("\n") 

            f.write(pattern)
            f.write('\n\n')
            break


f.close()
f2.close()
f3.close()
print("Finished")

