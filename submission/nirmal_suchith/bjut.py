from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
import csv
import re
from bs4 import BeautifulSoup
import time

def bjut_faculty():
    # Set up Selenium WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    base_url = "https://english.bjut.edu.cn/advisorlist.jsp?urltype=tree.TreeTempUrl&wbtreeid=1308"
    driver.get(base_url)
    driver.implicitly_wait(10)

    # Select "Faculty of Science" from the dropdown
    select_elem = driver.find_element(By.NAME, "dsjs_ext6")
    select = Select(select_elem)
    select.select_by_visible_text("Faculty of Science")
    time.sleep(2)  # Wait for the page to load after selecting the option

    # Prepare files for output
    filename = "bjut_faculty.txt"
    f = open(filename, "w", encoding="utf-8")

    excel_filename = "bjut_faculty.csv"
    f2 = open(excel_filename, "w", newline='', encoding="utf-8")
    csvwriter = csv.writer(f2)

    # Set the university name and country
    u_name = "Beijing University of Technology"
    country = "China"

    # Research keywords for filtering
    keyword_list = [
        'embedded systems', 'Embedded System', 'embedded software', 'hardware systems',
        'system architecture', 'IoT', 'real-time systems',
        'operating systems', 'Operating System', 'OS', 'system programming', 'system software',
        'distributed systems', 'kernel'
    ]

    # Start pagination and scrape data from each page
    while True:
        # Get the faculty list from the current page
        soup = BeautifulSoup(driver.page_source, "html.parser")
        
        # Find the specific section containing the faculty list
        faculty_list_div = soup.find('div', class_='list_nr')
        if faculty_list_div:
            faculty_list = faculty_list_div.find_all('li')  # Find each faculty member within the list_nr div
            
            # Loop through each faculty member and extract data
            for faculty in faculty_list:
                profile_link = faculty.find('a')['href']
                full_profile_url = base_url.split('advisorlist.jsp')[0] + profile_link
                
                # Open individual profile page
                driver.get(full_profile_url)
                time.sleep(2)  # Wait for the profile page to load
                profile_soup = BeautifulSoup(driver.page_source, "html.parser")

                # Extract Name
                name_tag = profile_soup.find('p', text=re.compile(r"Name:"))
                name = name_tag.find_next('p').get_text(strip=True) if name_tag else "Not Found"
                
                # Extract Email
                email_tag = profile_soup.find('p', text=re.compile(r"E-mail :"))
                email = email_tag.get_text(strip=True).replace("E-mail : ", "") if email_tag else "Not Found"
                
                # Extract Research Areas
                research_tag = profile_soup.find('ol', class_="list-paddingleft-2")
                research_areas = [item.get_text(strip=True) for item in research_tag.find_all('li')] if research_tag else []
                
                # Check if any research area matches the predefined keywords
                flag = False
                for keyword in keyword_list:
                    if any(re.search(keyword, area, re.IGNORECASE) for area in research_areas):
                        flag = True
                        break
                
                # If keyword matches, write to files
                if flag:
                    f.write(f"Name: {name}\nEmail: {email}\nUniversity: {u_name}\nResearch Areas: {', '.join(research_areas)}\n\n")
                    csvwriter.writerow([u_name, country, name, email, ', '.join(research_areas)])

        # Find 'Next' button and go to next page, if exists
        next_button = driver.find_elements(By.XPATH, "//a[text()='Next']")
        if next_button:
            next_button[0].click()  # Click the 'Next' button
            time.sleep(2)  # Wait for the page to load
        else:
            break  # Exit the loop if no next button is found

    # Close the files
    f.close()
    f2.close()

    # Close the WebDriver
    driver.quit()

    print("Data extraction complete")

if __name__ == '__main__':
    bjut_faculty()
