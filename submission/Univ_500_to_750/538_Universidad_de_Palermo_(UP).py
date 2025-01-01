import requests
import urllib.request
import time
import urllib
import re
import csv
from bs4 import BeautifulSoup

def harvard():
    url = "https://www.unipa.it/dipartimenti/matematicaeinformatica/?pagina=personale&ruolo=docenti"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        csv_filename = "harvard.csv"
        final_csv = "combined.csv"
        
        f1 = open(csv_filename, "w") # write data to the csv
        csvwriter1 = csv.writer(f1)

        f2 = open(final_csv, "a") # append data to the combined csv
        csvwriter2 = csv.writer(f2)

        univ_name = "Harvard University"
        country = "United States"

        garbage_emails = ['urp@unipa.it','webmaster@unipa.it','pec@cert.unipa.it'] # add garbage emails to this list

        variables = [csvwriter1, csvwriter2, univ_name, country, garbage_emails]
        d = soup.find('div',{'class':'page-row'})
        dd = d.find_all('div',{'class':'row equal'})
#         <div class="col-md-4 col-xs-12">
# <div class="panel panel-default panel-equal">
# <div class="panel-body">
# <div>
# <h3>
# <a href="/persone/docenti/a/domenico.amato01">DOMENICO&nbsp;AMATO</a>
# </h3>
# <p>RICERCATORE&nbsp;(INFO-01/A)</p>
# <div class="result_data">
# <em class="fa fa-phone"></em> <a href="tel:+3909123891125">+3909123891125</a></div>
# <div class="result_data">
# <em class="fa fa-envelope-o"></em> <a href="mailto:domenico.amato01@unipa.it">domenico.amato01@unipa.it</a>
# </div>
# </div>
# </div>
# </div>
# </div>
        for i in dd:
            div = i.find_all('div',{'class':'col-md-4 col-xs-12'})
            if len(div) == 0:
                continue
            for info in div:
                info_div = info.find('div',{'class':'panel-body'})
                if info_div == None:
                    continue
                name = info_div.find('h3').find('a').get_text()
                email = "Not Found"
                # get the correct name from the name
                link = "https://www.unipa.it"+info_div.find('h3').find('a').get('href')
                # get email
                email_div = info_div.find_all('div',{'class':'result_data'})
                if len(email_div) == 2:
                    email = email_div[1].find('a').get('href')[7:]
                print(name, link,email)
                try:
                    prof_resp = requests.get(link)
                except:
                    print("prof website not reached on time")
                    continue
                get_email(variables,garbage_emails,name,link,email,prof_resp)
        f1.close()
        f2.close()
        print("Finished")
    else:
        print("Error")



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
    harvard()



            







        