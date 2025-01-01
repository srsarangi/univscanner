import requests
import urllib.request
import time
import urllib
import re
import csv
from bs4 import BeautifulSoup

def cuny(url):
    # url = ""
    response = requests.get(url)
    if response.status_code == 200:
        # scrappable
        soup = BeautifulSoup(response.text, "html.parser")
        csv_filename = "City University of New York.csv"
        final_csv = "combined.csv"
        
        f1 = open(csv_filename, "w") # write data to the csv
        csvwriter1 = csv.writer(f1)

        f2 = open(final_csv, "a") # append data to the combined csv
        csvwriter2 = csv.writer(f2)

        univ_name = "City University of New York"
        country = "United States"

        garbage_emails = [] # add garbage emails to this list

        variables = [csvwriter1, csvwriter2, univ_name, country, garbage_emails]
    #     <p class="module-listing_item-item module-listing_item-email">
    #     <i class="far fa-envelope"></i>
    #       <a href="mailto:sos.agaian@csi.cuny.edu" rel="noopener">sos.agaian@csi.cuny.edu</a>

    #   </p>

        d = soup.find_all('div', {'class': 'module-listing__body'})
        if len(d) == 0:
            print("No data found")
            return False
        for i in d:
            profs = i.find_all('article')
            for prof in profs:
                name_div = prof.find('div', {'class': 'module-listing__item-name'})
                if name_div == None:
                    continue
                name = name_div.find('a').text
                link ="https://www.gc.cuny.edu"+ name_div.find('a').get('href')
                email_div = i.find('p',{'class':'module-listing_item-item module-listing_item-email'})
                if email_div == None:
                    email = "Not Found"
                else:
                    email = email_div.find('a').get('href')[7:]
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
    # cuny("https://www.gc.cuny.edu/people?type=17&program=475")
    main_url = "https://www.gc.cuny.edu/people?department=&program=475&search=&type=All&viewsreference%5Bdata%5D%5Bargument%5D=&viewsreference%5Bdata%5D%5Blimit%5D=&viewsreference%5Bdata%5D%5Boffset%5D=&viewsreference%5Bdata%5D%5Bpager%5D=&viewsreference%5Bdata%5D%5Btitle%5D=&viewsreference%5Bparent_entity_id%5D=15&viewsreference%5Bparent_entity_type%5D=node&viewsreference%5Bparent_field_name%5D=field_view&page="
    i =0
    while True:
        print("Page: ", i)
        if not cuny(main_url+str(i)):
            break
        else:
            i += 1


            







        