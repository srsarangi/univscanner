from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import csv
import re
from bs4 import BeautifulSoup
import time

def wayne_state_faculty():
    # Set up Selenium WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    base_url = "https://engineering.wayne.edu"  # Base URL for faculty links
    url = f"{base_url}/computer-science/faculty"  # Faculty listing page
    driver.get(url)
    driver.implicitly_wait(10)

    # Parse the main faculty page
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # File setup for output
    # filename = "wayne_state_faculty.txt"
    # f = open(filename, "w", encoding="utf-8")

    # excel_filename = "wayne_state_faculty.csv"
    # f2 = open(excel_filename, "w", newline='', encoding="utf-8")
    # csvwriter = csv.writer(f2)

    # Set the university name and country
    u_name = "Wayne State University"
    country = "USA"
    profs = []
    
    # Research keywords for filtering
    keyword_list = [
        'embedded systems', 'Embedded System', 'embedded software', 'hardware systems',
        'system architecture', 'IoT', 'real-time systems',
        'operating systems', 'Operating System', 'OS', 'system programming', 'system software',
        'distributed systems', 'kernel'
    ]
    
    # Locate all faculty profile links
    faculty_links = soup.find_all('a', href=re.compile(r'^/profile/'))
    faculty_urls = [base_url + link['href'] for link in faculty_links]

    # Loop through each faculty profile page
    for profile_url in faculty_urls:
        driver.get(profile_url)
        time.sleep(2)  # Give some time for the page to load
        profile_soup = BeautifulSoup(driver.page_source, "html.parser")
        
        # Extract Name
        name_tag = profile_soup.find('h1', class_='mt-4 block lg:hidden')
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
            # f.write(f"Name: {name}\nEmail: {email}\nUniversity: {u_name}\nResearch Areas: {research_interests}\n\n")
            # csvwriter.writerow([u_name, country, name, email, research_interests])
            profs.append([u_name, country, name, email, profile_url])
    
    # Close the files
    # f.close()
    # f2.close()

    # Close the WebDriver
    driver.quit()
    print("Wayne State Faculty scraped successfully")
    return profs

if __name__ == '__main__':
    wayne_state_faculty()
