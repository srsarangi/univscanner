import requests
import urllib.request
import time
import urllib
import re
import csv
from bs4 import BeautifulSoup

def delaware():
    url = "https://www.cis.udel.edu/people/faculty/"
    response = requests.get(url)
    if response.status_code == 200:
        # scrappable
        soup = BeautifulSoup(response.text, "html.parser")
        csv_filename = "University_of_Delaware.csv"
        final_csv = "combined.csv"
        
        f1 = open(csv_filename, "w") # write data to the csv
        csvwriter1 = csv.writer(f1)

        f2 = open(final_csv, "a") # append data to the combined csv
        csvwriter2 = csv.writer(f2)

        univ_name = "University of Delaware"
        country = "United States"

        garbage_emails = [] # add garbage emails to this list

        variables = [csvwriter1, csvwriter2, univ_name, country, garbage_emails]
        # <div class="et_pb_text_inner" id="directory">
								
		# 						<a class="entry-featured-image-url" href="https://www.cis.udel.edu/people/faculty/john-aromando/" role="link">
		# 														<img src="https://i0.wp.com/www.cis.udel.edu/wp-content/uploads/2023/08/Aromando_John-sq.jpg?fit=400%2C400&amp;ssl=1" width="265" height="265" alt="John Aromando" class="dir-thumb"></a>
		# 					    <h2><a href="https://www.cis.udel.edu/people/faculty/john-aromando/" role="link">John Aromando</a></h2>
		# 						<p class="d-title">Instructor</p>
		# 						<p class="d-title">408 Smith Hall</p>
		# 						<p class="d-title">302-831-4802</p>				
		# 						<p><a href="mailto:jaro@udel.edu" role="link">jaro@udel.edu</a></p>
		# 					</div>

        # get the above html element from soup
        d = soup.find_all('div', {'class': 'et_pb_text_inner'})
        for i in d:
            if i.find('h2') == None:
                continue
            a = i.find('h2')
            name = a.get_text()
            a = i.find('a')
            link = a.get('href')
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



def get_email(variables,garbage_emails,name,link,email,page_resp):
    csvwriter1, csvwriter2, univ_name, country, garbage_emails = variables
    
    prof_soup = BeautifulSoup(page_resp.text, "html.parser")
    # key_words = ['BASE'] # base is used when there is no use of keywords
    key_words = ['operating systems','Embedded System','embedded system', 'Operating Systems','operating system','Operating System','embedded systems','embedded','Embedded',"Embedded Systems"]
    #<div id="et-main-area">
    # get the above html element from prof_soup
    prof_text = prof_soup.find('div', {'id': 'et-main-area'})
    prof_text = prof_text.text
    # prof_text = prof_soup.text   # get the text from the page

    for word in key_words:
        if re.search(word,prof_text,re.IGNORECASE) or word == 'BASE':
            print("matched_word: ",word)
            if email != "Not Found": # if email is already found, no need to find it again (at line 50)
                # just write
                csvwriter1.writerow([univ_name,country,name,email,link])
                csvwriter2.writerow([univ_name,country,name,email,link])
            else:
                new_emails = list(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}", prof_text))
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
    delaware()



            







        