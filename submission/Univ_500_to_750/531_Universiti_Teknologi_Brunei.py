import requests
import urllib.request
import time
import urllib
import re
import csv
from bs4 import BeautifulSoup

def burnei(url):
    # url = "https://www.seas.harvard.edu/computer-science/faculty-research"
    response = requests.get(url)
    if response.status_code == 200:
        # scrappable
        soup = BeautifulSoup(response.text, "html.parser")
        csv_filename = "Universiti_Teknologi_Brunei.csv"
        final_csv = "combined.csv"
        
        f1 = open(csv_filename, "a") # write data to the csv
        csvwriter1 = csv.writer(f1)

        f2 = open(final_csv, "a") # append data to the combined csv
        csvwriter2 = csv.writer(f2)

        univ_name = "Universiti Teknologi Brunei"
        country = "Brunei"

        garbage_emails = [] # add garbage emails to this list

        variables = [csvwriter1, csvwriter2, univ_name, country, garbage_emails]

    #     <div class="gdlr-core-personnel-list-content-wrap">
    #                                             <div class="gdlr-core-personnel-list-social">

    #                                             </div>
    #                                             <h3 class="gdlr-core-personnel-list-title" style="font-size: 23px ;font-weight: 700 ;letter-spacing: 0px ;text-transform: none ;"><a href="/academics/people/zulkefle-ismail/">ZULKEFLE ISMAIL</a></h3>
    #                                             <div class="gdlr-core-personnel-list-position gdlr-core-info-font gdlr-core-skin-caption" style="font-size: 16px ;font-weight: 500 ;font-style: normal ;letter-spacing: 0px ;">School of Design</div>
    #                                             <div class="gdlr-core-personnel-list-position gdlr-core-info-font gdlr-core-skin-caption" style="font-size: 16px ;font-weight: 500 ;font-style: normal ;letter-spacing: 0px ;">ASSISTANT PROFESSOR | ARCHITECTURE PROGRAMME LEADER</div>
    #                                             <div class="gdlr-core-personnel-info">
    #                                                         <span class="gdlr-core-blog-info gdlr-core-blog-info-font gdlr-core-skin-caption gdlr-core-blog-info-category">
    #                                                                 <a href="?tag=School of Design" rel="tag">School of Design</a>
    #                                                                 <a href="?tag=architecture" rel="tag">architecture</a>
    #                                                         </span>
    #                                             </div>
    #                                             <div class="gdlr-core-personnel-info">
    #                                                     <div class="kingster-personnel-info-list kingster-type-location"><i class="kingster-personnel-info-list-icon fa fa-location-arrow"></i>1A.15</div>
    #                                                                                                         <div class="kingster-personnel-info-list kingster-type-phone"><i class="kingster-personnel-info-list-icon fa fa-phone"></i>1238</div>
    #                                                                                                                                                             <div class="kingster-personnel-info-list kingster-type-email"><i class="kingster-personnel-info-list-icon fa fa-envelope-open"></i><a href="mailto:zulkefle.ismail@utb.edu.bn">zulkefle.ismail@utb.edu.bn</a></div>
    #                                             </div>
    #                                             <!--<div class="gdlr-core-personnel-list-content">
    #     <p>
    #         &#8211; PhD, Accounting, Finance minor, Texas A&#038;M University
    #         <br /> &#8211; BA, Business Administration, University of Washington
    #     </p>
    # </div>-->
    #                                             <a class="gdlr-core-personnel-list-button gdlr-core-button" href="/academics/people/zulkefle-ismail/">More Detail</a>
    #                                         </div>

        d = soup.find_all('div', {'class': 'gdlr-core-personnel-list-content-wrap'})
        print(len(d))
        if len(d) == 0:
            return False
        # get the name and email, link
        for i in d:
            name = i.find('h3').find('a').get_text()
            # print(name)
            email = "Not Found"
            a = i.find('div', {'class': 'kingster-personnel-info-list kingster-type-email'})
            if a != None:
                email = a.find('a').get_text()
            # print(email)
            link = "https://www.utb.edu.bn"+ i.find('h3').find('a').get('href')
            # print(link)
            print(name, email, link)
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
    main_url = "https://www.utb.edu.bn/academics/people/?page="
    i = 1
    while True:
        if not burnei(main_url + str(i)):
            break
        i += 1 
        
    



            







        