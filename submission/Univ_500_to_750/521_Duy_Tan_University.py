import requests
import urllib.request
import time
import urllib
import re
import csv
from bs4 import BeautifulSoup

def duytan(url):
    # url = "https://is.duytan.edu.vn/en/faculty-directory?page=0"
    response = requests.get(url)
    if response.status_code == 200:
        # scrappable
        soup = BeautifulSoup(response.text, "html.parser")
        csv_filename = "Duy_Tan_University.csv"
        final_csv = "combined.csv"
        
        f1 = open(csv_filename, "a") # write data to the csv
        csvwriter1 = csv.writer(f1)

        f2 = open(final_csv, "a") # append data to the combined csv
        csvwriter2 = csv.writer(f2)

        univ_name = "Duy Tan University"
        country = "Vietnam"

        garbage_emails = [] # add garbage emails to this list

        variables = [csvwriter1, csvwriter2, univ_name, country, garbage_emails]

        d = soup.find('ol', {'class': 'results no-bullet'})
        if len(d)== 0:
            return False
        dd = d.find_all('li')
        if len(dd) == 0:
            return False
        # <li class="results__list-item">
        #         <article class="listing clearfix" role="article">
        #                 <figure class="listing__image">
        #                     <a href="/en/faculty/1"><img src="https://files01.duytan.edu.vn/svruploads/is-en-duytan/upload/images/Man-NGUYEN-65-32-47.jpg" alt="Nguyen-Duc Man" height="500" width="500"></a>
        #                 </figure>
        #             <div class="user-markup">
        #                 <h2 class="listing__heading"><a href="/en/faculty/1" style="text-decoration: none">Nguyen-Duc Man</a></h2>
        #                 <p>Vice-dean, International School </p>
        #                 <p>
        #                     <a href="/en/faculty/1" class="button">Read More<svg class="icon icon-triangle"><use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="#icon-triangle"></use></svg></a>
        #                 </p>
        #             </div>
        #         </article>
        #     </li>
        for i in dd:
            if i.find('h2') == None:
                continue
            h2  = i.find('h2')
            a = h2.find('a')
            name = a.get_text()
            link = "https://is.duytan.edu.vn"+ a.get('href')
            print(name, link)
            email = "Not Found"
            # check if link is valid or not
            try:
                prof_resp = requests.get(link)
            except:
                continue
            get_email(variables,garbage_emails,name,link,email,prof_resp)

        f1.close()
        f2.close()
        print("Finished")
        return True
    return False



def get_email(variables,garbage_emails,name,link,email,page_resp):
    csvwriter1, csvwriter2, univ_name, country, garbage_emails = variables
    if email != "Not Found": # if email is already found, no need to find it again (at line 50)
        # just write
        csvwriter1.writerow([univ_name,country,name,email,link])
        csvwriter2.writerow([univ_name,country,name,email,link])
        return
    prof_soup = BeautifulSoup(page_resp.text, "html.parser")
    # key_words = ['BASE'] # base is used when there is no use of keywords
    key_words = ['operating systems','Embedded System','embedded system', 'Operating Systems','operating system','Operating System','embedded systems','embedded','Embedded',"Embedded Systems"]
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
    main_url = "https://is.duytan.edu.vn/en/faculty-directory?page="
    i =1
    while True:
        if not duytan(main_url+str(i)):
            break
        print("Page: ",i)
        i += 1



            







        