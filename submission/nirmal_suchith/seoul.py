from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import csv
import re
from bs4 import BeautifulSoup
import time

def is_there_a_match(content, keyword_list):
        pattern = r'\b(?:' + '|'.join(map(re.escape, keyword_list)) + r')\b'

        # Search for any match
        flag = False
        if re.search(pattern, content, flags=re.IGNORECASE):
            flag = True
        return flag
    # https://www.uos.ac.kr/en/professor/list.do?code=20020#
def seoul_faculty():
    # Set up Selenium WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    base_url = "https://www.uos.ac.kr/en/professor"  # Base URL for faculty links
    url = f"{base_url}/list.do?code=20020#"  # Faculty listing page
    driver.get(url)
    driver.implicitly_wait(15)
    
    excel_filename = "seoul.csv"
    f = open(excel_filename, "w", newline="", encoding="utf-8")
    csvwriter = csv.writer(f)

    # Set the university name and country
    u_name = "University of Seoul"
    country = "South Korea"
    
    # Research keywords for filtering
    keyword_list = [
    'embedded systems', 'Embedded System', 'embedded software', 'hardware systems',
    'system architecture', 'IoT', 'real-time systems',
    'operating systems', 'Operating System', 'OS', 'system programming', 'system software',
    'distributed systems', 'kernel'
]
    soup = BeautifulSoup(driver.page_source, "html.parser")
    # Locate all faculty profile links
    #do work here
    for i in range (1, 10+1):
        full_x_path = f'/html/body/div[2]/div[2]/div/div[2]/form/ul/li[{i}]/div[2]/p[1]/a'
        faculty_button = driver.find_element(By.XPATH, full_x_path)
        faculty_button.click()
        time.sleep(2)
        faculty_soup = BeautifulSoup(driver.page_source, "html.parser")
        
        #i want to find div tag with class = 'tabList2Cont'
        content_tag = faculty_soup.find('div', class_ = 'tabList2Cont', id = 'tabCont1') 
        content = content_tag.get_text(strip=True) if content_tag else "Not Found"
        # Create a single regex pattern to match any keyword
        flag = is_there_a_match(content, keyword_list)
        if flag:
            prof_name = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/div[1]/div[2]/div[1]/p[1]').text
            email = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/div[1]/div[2]/div[2]/p[3]').text
            #get the current url
            website_link = driver.current_url
            # print(prof_name, email, website_link)
            csvwriter.writerow([u_name, country, prof_name, email, website_link])
        driver.back()

    f.close()
    driver.quit()
    print("Data extraction complete")
    
if __name__ == '__main__':
    seoul_faculty()
        
    
        
        
        


