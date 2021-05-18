import requests
import urllib.request
import time
import urllib
import re
import csv
import sys
from bs4 import BeautifulSoup

def uni_berlin():
    url = "https://www.informatik.hu-berlin.de/de/org/mitarbeiter"
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    file_name = sys.argv[0]
    # file_name = file_name[4:]

    txt_file = file_name.replace(".py", ".txt")
    f = open(txt_file, "w")

    csv_file = file_name.replace(".py", ".csv")
    f2 = open(csv_file, "w")
    csvwriter = csv.writer(f2)

    overall_file = "all_emails.csv"
    f3 = open(overall_file, "a")
    csvwriter2 = csv.writer(f3)

    u_name = "University of Berlin"
    country = "Germany"

    grabage_emails = []

    var = [f, csvwriter, csvwriter2, u_name, country, grabage_emails]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('dl', {'class':'letterDL'})
    d = dd.find_all('dd', {'class':'view_content'})

    #iterating for every prof
    for i in d:
        a = i.find('a')
        if a == None:
            continue
        link = a.get('href')
        name = a.get_text()

        # print(name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link)
        except:
            continue

        # get prof homepage from dept profile page
        prof_soup = BeautifulSoup(prof_resp.text, "html.parser")
        a = prof_soup.find('a',{'class':'url'})
        if a == None:
            continue

        link =  a.get('href')
        try:    
            prof_resp = requests.get(link)
        except:
            continue

        email = "Not Found"
        print(name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)


    f.close()
    f2.close()
    f3.close()
    print("Finished")



def filterandgetEmail(var, grabage_emails, name, link, email, prof_resp):
    f = var[0]
    csvwriter = var[1]
    csvwriter2 = var[2]

    u_name = var[3]
    country = var[4]

    keyword_list = ['Computer Architecture','hardware and system architecture', 'hardware and architecture', 'embedded system', 'computer organization','VLSI Design', 'Computer and System',
                    'multiprocessor architecture']
    flag = 1
    prof_soup = BeautifulSoup(prof_resp.text, "html.parser")
    research_text = prof_soup.text
    for pattern in keyword_list:
        if re.search(pattern, research_text, re.IGNORECASE):
            flag = 0
            if email != 'Not Found':
                f.write(link + '\n' + name + "\t"+ email + "\n")
                csvwriter.writerow([u_name, country, name, email, link])
                csvwriter2.writerow([u_name, country, name, email, link])
            else:
                new_emails = set(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}", prof_resp.text))
                for eemail in grabage_emails:
                    if eemail in new_emails:
                        new_emails.remove(eemail)
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

if __name__ == '__main__':
    uni_berlin()
     