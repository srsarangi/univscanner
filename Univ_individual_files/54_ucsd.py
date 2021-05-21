import requests
import urllib.request
import time
import urllib
import re
import csv
from bs4 import BeautifulSoup

def ucsd():
    url = "https://cse.ucsd.edu/people/faculty-profiles/faculty"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")

    # file initialization to write
    filename = "ucsd.txt"
    f = open(filename, "w")

    excel_filename = "ucsd.csv"
    f2 = open(excel_filename, "w")
    csvwriter = csv.writer(f2)

    overall_file = "all_emails.csv"
    f3 = open(overall_file, "a")
    csvwriter2 = csv.writer(f3)

    u_name = "University of California SD"
    country = "USA"

    grabage_emails = []

    var = [f, csvwriter, csvwriter2, u_name, country, grabage_emails]

    # d gives the array of all profs on the dept homepage
    # d = soup.find('a', {'class':"accordian-title"})
    dd = soup.find('div', {'class':'view-content'})
    d = dd.find_all('div', {'class':"col col-xs-6 col-sm-6 col-md-4 col-lg-3 "})

    #iterating for every prof
    for i in d:
        # print(i)
        a = (i.find('a')).find_next('a')
        name = (a.get_text()).strip()
        link = 'https://cse.ucsd.edu'+ a.get('href')

        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link)  
            prof_soup = BeautifulSoup(prof_resp.text, "html.parser")   
        except:
            continue

        aa = prof_soup.find('a', text='Website')
        if aa == None:
            continue
        link2 = aa.get('href')
        try:    
            prof_resp2 = requests.get(link2)  
            prof_soup2 = BeautifulSoup(prof_resp2.text, "html.parser")   
        except:
            continue
            
        email = "Not Found"
        print(name, link2)
        filterandgetEmail(var, grabage_emails, name, link2, email, prof_resp2)

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

    keyword_list = ['Computer architecture','computer architecture','Computer Architecture', 'Hardware And System Architecture', 'hardware and system architecture', 
                'Hardware and Architecture', 'hardware and architecture', 'embedded system', 'Embedded System','Computer Organization','VLSI', 'Computer and System']
    flag = 1
    prof_soup = BeautifulSoup(prof_resp.text, "html.parser") 
    research_text = prof_soup.text
    for pattern in keyword_list:
        if re.search(pattern,research_text):
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
    ucsd()
    