from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import csv
import re
from bs4 import BeautifulSoup
import time

def bits_pilani_faculty():
    # Set up Selenium WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    base_url = "https://www.bits-pilani.ac.in"  # Base URL for faculty links
    url = "https://www.bits-pilani.ac.in/faculty/?campus=hyderabad&department=computer-science-information-systems"  # Faculty listing page
    driver.get(url)
    driver.implicitly_wait(10)

    # File setup for output
    filename = "bits_pilani_faculty.txt"
    f = open(filename, "w", encoding="utf-8")

    excel_filename = "bits_pilani_faculty.csv"
    f2 = open(excel_filename, "w", newline='', encoding="utf-8")
    csvwriter = csv.writer(f2)

    # Set the university name and country
    u_name = "BITS Pilani, Hyderabad Campus"
    country = "India"
    
    # Research keywords for filtering
    keyword_list = [
        'embedded systems', 'Embedded System', 'embedded software', 'hardware systems',
        'system architecture', 'IoT', 'real-time systems',
        'operating systems', 'Operating System', 'OS', 'system programming', 'system software',
        'distributed systems', 'kernel'
    ]
    
    # Loop through the pages
    page_number = 1
    while True:
        # Parse the faculty listing page
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Locate all faculty profile links on the current page
        faculty_links = soup.find_all('a', href=re.compile(r'^/hyderabad/'))
        faculty_urls = [base_url + link['href'] for link in faculty_links]

        # Loop through each faculty profile page
        for profile_url in faculty_urls:
            driver.get(profile_url)
            time.sleep(2)  # Give some time for the page to load
            profile_soup = BeautifulSoup(driver.page_source, "html.parser")
            
            # Extract Name
            name_tag = profile_soup.find('h2')
            name = name_tag.get_text(strip=True) if name_tag else "Not Found"
            
            # Extract Email
            email_tag = profile_soup.find('a', href=re.compile(r'^mailto:'))
            email = email_tag.get_text(strip=True) if email_tag else "Not Found"
            
            # Extract Research Interests
            research_tag = profile_soup.find('h2', string=re.compile(r"Research Interests", re.IGNORECASE))
            research_paragraph = research_tag.find_next('p') if research_tag else None
            research_interests = research_paragraph.get_text(strip=True) if research_paragraph else ""
            
            # Check if any research interest matches our criteria
            flag = False
            for keyword in keyword_list:
                if re.search(keyword, research_interests, re.IGNORECASE):
                    flag = True
                    break
            
            # If keyword matches, write to files
            if flag:
                f.write(f"Name: {name}\nEmail: {email}\nUniversity: {u_name}\nResearch Areas: {research_interests}\n\n")
                csvwriter.writerow([u_name, country, name, email, research_interests])
        
        # After processing all faculty profiles, check for the next page link
        next_button = soup.find('a', class_='next page-numbers')
        if next_button and 'href' in next_button.attrs:
            next_page_url = next_button['href']
            driver.get(next_page_url)
            page_number += 1
            time.sleep(3)  # Wait before processing the next page
        else:
            break  # No next page, exit the loop
    
    # Close the files
    f.close()
    f2.close()

    # Close the WebDriver
    driver.quit()

    print("Data extraction complete")

if __name__ == '__main__':
    bits_pilani_faculty()
