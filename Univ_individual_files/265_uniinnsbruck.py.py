import requests
import urllib.request
import time
import urllib
import re
import csv
from bs4 import BeautifulSoup

def innsbruck():
    url = "https://dps.uibk.ac.at/staff/"
    r = requests.get(url, verify=False)
    soup = BeautifulSoup(r.text, "html.parser")
    #print(r.text)
    #print(soup.get_text())
    
    # file initialization to write
    filename = "innsbruck.txt"
    f = open(filename, "w", encoding='utf-8')

    excel_filename = "innsbruck.csv"
    f2 = open(excel_filename, "w", encoding='utf-8')
    csvwriter = csv.writer(f2)

    overall_file = "all_emails.csv"
    f3 = open(overall_file, "a", encoding='utf-8')
    csvwriter2 = csv.writer(f3)
    
    u_name = "University of Innsbruck"
    country = "Austria"
    garbage_emails = ['peter@ph3.at']
    var = [f, csvwriter, csvwriter2, u_name, country]

    
    d = soup.find_all('div',{'class':'entry-content'})
    d = d[0].find_all('tbody')
    x = d[0]
    x.extend(d[1])
    d = x.find_all('tr')
    
    
    #print(type(d))
    #print(d)
    #print(len(d))
    
    b=0
    for i in d:
        
        #print(z)
        #print(a,z)
        name = i.find_all('strong')                                     # extracting prof name
        if(len(name)>1):
            name=name[1].get_text()
        else:
            name = name[0].get_text()
        link = i.find('a', text = 'Website')          # extracting prof page link
        link = link.get('href')
        name=name.strip()
        
        #print(a.find('a'))
        
        
        b=b+1
        
        #print(b)
        #print(link)
        try:
            prof_resp = requests.get(link)      # requesting prof homepgae
        except:
            continue
        email = "Not Found"
        b=b+1
        #print(b)
        print(name, email, link)
        filterandgetEmail(var, garbage_emails, name, link, email, prof_resp)



def filterandgetEmail(var, garbage_emails, name, link, email, prof_resp):
    f = var[0]
    csvwriter = var[1]
    csvwriter2 = var[2]

    u_name = var[3]
    country = var[4]

    keyword_list = ['Parallel Systems','parallel systems','parallel system','Parallel System','Computer architecture','computer architecture','Computer Architecture', 'Hardware And System Architecture', 'hardware and system architecture', 'Hardware and Architecture', 'hardware and architecture', 'embedded system', 'Embedded System','Computer Organization','VLSI', 'Computer and System','Distributed System', 'distributed system', 'Distributed system' ]
    #keyword_list = ['computer architecture', 'Computer architecture', 'Embedded System', 'Embedded system', 'embedded system']   # 'Computer Architecture',
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
                #print(new_emails)
                for eemail in garbage_emails:
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
    #print("aa")
    innsbruck()
    print("finish")