import requests
import urllib.request
import time
import urllib
import re
import csv
from bs4 import BeautifulSoup

def oregon(url):
    # url = "https://www.seas.harvard.edu/computer-science/faculty-research"
    response = requests.get(url)
    if response.status_code == 200:
        # scrappable
        soup = BeautifulSoup(response.text, "html.parser")
        csv_filename = "Oregon State University.csv"
        final_csv = "combined.csv"
        
        f1 = open(csv_filename, "a") # write data to the csv
        csvwriter1 = csv.writer(f1)

        f2 = open(final_csv, "a") # append data to the combined csv
        csvwriter2 = csv.writer(f2)

        univ_name = "Oregon State University"
        country = "United States"

        garbage_emails = [] # add garbage emails to this list

        variables = [csvwriter1, csvwriter2, univ_name, country, garbage_emails]
#         <div class="views-field views-field-nothing h-100"><span class="field-content"><div class="osu-bg-page-alt-1 osu-shadow h-100 rounded-bottom">
#   <a href="/people/julie-adams" hreflang="en"><img src="/sites/engineering.oregonstate.edu/files/styles/profile_image/public/2024-10/Julie%20A.%20Adams_00061%281%29.jpg?itok=dtMax1Cn" width="400" height="350" alt="Portrait of Julie Adams." loading="lazy" class="image-style-profile-image img-fluid">

# </a>

# <div class="p-3">
#   <h2 class="fw-bolder text-break">
#     <a href="/people/julie-adams" hreflang="en">Julie A. Adams</a>
#   </h2>
#   <p>Professor | CoRIS Associate Director for Research </p>
#    <p class="text-truncate"><a href="mailto:julie.a.adams@oregonstate.edu">julie.a.adams@oregonstate.edu</a></p>
#   <p>Collaborative Robotics and Intelligent Systems Institute | Electrical Engineering and Computer Science</p>
# </div>
# </div></span></div>
        # get the above html element from soup
        d = soup.find_all('div', {'class': 'views-field views-field-nothing h-100'})
        if len(d) == 0:
            return False
        for i in d:
            if i.find('h2') == None:
                continue
            h2  = i.find('h2')
            a = h2.find('a')
            name = a.get_text()
            link = "https://engineering.oregonstate.edu"+ a.get('href')
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
    url = "https://engineering.oregonstate.edu/people?title=&field_osu_organizations_target_id=All&term_node_tid_depth=All&field_c_engr_discipline_target_id=7&items_per_page=40&page="
    i = 0
    while True:

        if not oregon(url+str(i)):
            break
        print("page: ",i)
        i += 1
    # oregon()



