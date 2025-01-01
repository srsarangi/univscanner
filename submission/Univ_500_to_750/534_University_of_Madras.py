import requests
import urllib.request
import time
import urllib
import re
import csv
from bs4 import BeautifulSoup

def madras():
    return 
    url = "https://www.unom.ac.in/index.php?route=department/department/deptpage&deptid=21"
    response = requests.get(url)
    if response.status_code == 200:
        # scrappable
        soup = BeautifulSoup(response.text, "html.parser")
        csv_filename = "University of Madras.csv"
        final_csv = "combined.csv"
        
        f1 = open(csv_filename, "w") # write data to the csv
        csvwriter1 = csv.writer(f1)

        f2 = open(final_csv, "a") # append data to the combined csv
        csvwriter2 = csv.writer(f2)

        univ_name = "University of Madras"
        country = "India"

        garbage_emails = [] # add garbage emails to this list

        variables = [csvwriter1, csvwriter2, univ_name, country, garbage_emails]
        # <div role="tabpanel" class="tab-pane fade active in" id="faculty">
        # get the above html element from soup
        d = soup.find('div', {'role': 'tabpanel', 'class': 'tab-pane fade active in', 'id': 'faculty'})
        # <div class="row faculty-border">
        #                              <div class="col-lg-2 col-md-2 col-sm-2">
        #                                 <div class="our-team">
        #                                     <div class="pic">
        #                                                                                              <img alt="" src="https://www.unom.ac.in/webportal/uploads/faculty/20472.png">
        #                                     </div>

        #                                 </div>
        #                             </div>
        #                             <div class="col-lg-10 col-md-10 col-sm-10">
        #                                 <div class="faculty-detail">
        #                                     <h5 class="post mt-0 mb-5 pl-0">Professor and Head</h5>
        #                                     <h3 class="name pl-0">Dr. S. Gopinathan</h3>
        #                                     <h6 class="qualification mt-0 mb-5"> M.Sc., Ph.D.,</h6>
        #                                     <p><i class="fa fa-envelope" style="color: #063a7e;"></i>&nbsp;&nbsp;gnathans2002@unom.ac.in&nbsp;&nbsp;<i class="fa fa-phone-square ml-20" style="color: #063a7e;"></i>&nbsp;&nbsp;044-22202905</p>
        #                                     <p class="mt-10"><a href="https://www.unom.ac.in/index.php?route=department/department/profile&amp;deptid=21&amp;facultyid=70">Read Profile</a><i class="fa fa-angle-double-right ml-10" style="font-size:20px; font-weight: bold; color:#FF540C;"></i></p>
                                            
        #                                 </div>
        #                             </div>
                                    
                                    
        #                             </div>
        # get the above html element from d
        dd = d.find_all('div', {'class': 'row faculty-border'})
        # find name, email, link
        for i in dd:
            # get name, link, email
            div = i.find('div', {'class': 'faculty-detail'})
            if div == None:
                continue
            name = div.find('h3').get_text()
            email = "Not Found"
            email_p = div.find_all('p')
            if len(email_p) != 2:
                continue
            email = email_p[0].get_text()
            email = email.split('\xa0\xa0')[1].strip()
            link = email_p[1].find('a').get('href')
            print(name, link, email)
            # check if link is valid or not
            try:
                prof_resp = requests.get(link)
            except:
                continue
            get_email(variables,garbage_emails,name,link,email,prof_resp)



        f1.close()
        f2.close()
        print("Finished")



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
    madras()



            







        