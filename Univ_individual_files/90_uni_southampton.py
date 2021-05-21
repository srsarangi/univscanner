import requests
import urllib.request
import time
import urllib
import re
import csv
from bs4 import BeautifulSoup

def uni_southampton():
    url = "https://www.ecs.soton.ac.uk/people"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")
    # print(soup.prettify)

    # file initialization to write
    filename = "uni_southampton.txt"
    f = open(filename, "w")

    excel_filename = "uni_southampton.csv"
    f2 = open(excel_filename, "w")
    csvwriter = csv.writer(f2)

    overall_file = "all_emails.csv"
    f3 = open(overall_file, "a")
    csvwriter2 = csv.writer(f3)

    u_name = "University of Southampton"
    country = "UK"

    grabage_emails = []

    var = [f, csvwriter, csvwriter2, u_name, country, grabage_emails]

    # d gives the array of all profs on the dept homepage
    # d = soup.find('a', {'class':"accordian-title"})
    dd = soup.find('tbody', {'class':'list'})
    d = dd.find_all('tr')

    #iterating for every prof
    for i in d:
        td1 = i.find('td')
        a = td1.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        # break loop on professor as list is very long
        if name == 'Dr Chris Adetunji':
            break

        link = 'https://www.ecs.soton.ac.uk'+a.get('href')
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link)        
        except:
            continue

        # remove research sudents from list
        td2_text = (td1.find_next('td')).get_text()
        if ('student' in td2_text) or ('Visitor' in td2_text) :
            continue

        td4 = (((td1.find_next('td')).find_next('td')).find_next('td'))
        a_mail = td4.find('a')
        if a_mail != None:
            email = a_mail.get('href')
            email = email[7:]
        else:
            email = "Not Found"

        print(name, email, link)
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

    keyword_list = ['Computer architecture','computer architecture','Computer Architecture', 'Hardware And System Architecture', 'hardware and system architecture', 
                'Hardware and Architecture', 'hardware and architecture', 'embedded system', 'Embedded System','Computer Organization', 'Computer and System']
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
    uni_southampton()
    