import requests
import urllib.request
import time
import urllib
import re
from bs4 import BeautifulSoup

url = "https://cms.caltech.edu/people"   # homepage url
r = requests.get(url)                                        # request to url

# getting the soup by parsing the html parsel to text to request r
soup = BeautifulSoup(r.text, "html.parser")

# file initialization to write
filename = "caltech.txt"
f = open(filename, "w")

excel_filename = "caltech.csv"
f2 = open(excel_filename, "w")
csvwriter = csv.writer(f2)

overall_file = "all_emails.csv"
f3 = open(overall_file, "a")
csvwriter2 = csv.writer(f3)

u_name = "Caltech"
country = "USA"

# using set() to store to remove duplicates emails
emails = set()

# d gives the array of all profs on the dept homepage
# d = soup.find('a', {'class':"accordian-title"})
d = soup.find_all('strong', {'class':'name'})
# dd = d.find_all('div', {'class': 'views-field views-field-title'})
# print(d)
#iterating for every prof
for i in d:
    a = i.find('a')                     # a contains the name and the homepage of prof
    # print(a.get('href'))
    link = "https://cms.caltech.edu" + a.get('href')                # extracting prof page link
    # print(link)
    name = a.get_text()                 # extracting prof name
    prof_resp = requests.get(link)      # requesting prof homepgae
    prof_soup = BeautifulSoup(prof_resp.text, "html.parser")                    # passing the text to soup

    keyword_list = ['Computer Architecture', 'computer architecture', 'Computer architecture', 'Embedded System', 'Embedded system', 'embedded system', 'VLSI']
    flag = 1
    research_text = prof_soup.text
    for pattern in keyword_list:
        if re.search(pattern,research_text):
            flag = 0
            new_emails = set(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}", prof_resp.text))
            new_emails.remove('commofc@caltech.edu')
            # f.write(link + '\n' + name)
            if len(new_emails) == 0:
                # f.write(link + '\n' + name + "\t\t Email Not Found \n")
                email = "Email Not Found"
                f.write(link + '\n' + name + "\t"+ email + "\n")
                csvwriter.writerow([u_name, country, name, email, link])
                csvwriter2.writerow([u_name, country, name, email, link])
            else:
                for email in new_emails:
                    f.write(link + '\n' + name + '\t\t' + email + '\n')
                    csvwriter.writerow([u_name, country, name, email, link])
                    csvwriter2.writerow([u_name, country, name, email, link])

            f.write(pattern)
            f.write('\n\n')
            break
            
    # if flag:
    #     new_emails = set(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}", prof_resp.text))
    #     new_emails.remove('commofc@caltech.edu')
    #     # f.write(link + '\n' + name)
    #     f.write('\n ========================= NOT ==================================\n')
    #     if len(new_emails) == 0:
    #         f.write(link + '\n' + name + "\t\t Email Not Found \n")
    #     else:
    #         for email in new_emails:

    #             f.write(link + '\n' + name + '\t\t' + email + '\n')
    #     f.write('====================================================================\n')

f.close()
f2.close()
f3.close()
print("Finished")

