from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import csv
import re

def hacettepe():
    # Set up Selenium WebDriver (using Chrome in this case)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    url = "https://www.cs.hacettepe.edu.tr/#faculty_members"  # Faculty page URL
    driver.get(url)  # Load the page

    # Give the page some time to load the JavaScript content
    driver.implicitly_wait(10)

    # Parse the page content using BeautifulSoup
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # File setup for output
    # filename = "hacettepe_faculty.txt"
    # f = open(filename, "w")
    
    # excel_filename = "hacettepe_faculty.csv"
    # f2 = open(excel_filename, "w", newline='', encoding="utf-8")
    # csvwriter = csv.writer(f2)

    # Set the university name and country
    u_name = "Hacettepe University"
    country = "Turkey"
    
    # Research keywords for embedded systems or operating systems
    keyword_list = [
        'embedded systems', 'Embedded System', 'embedded software', 'hardware systems',
        'system architecture', 'IoT', 'real-time systems',
        'operating systems', 'Operating System', 'OS', 'system programming', 'system software',
        'distributed systems', 'kernel'
    ]
    
    # Extracting all faculty profiles (divs with the class 'people-main')
    faculty_profiles = soup.find_all('div', class_='people-main')
    
    professors = []
    for profile in faculty_profiles:
        # Extracting name
        name_tag = profile.find('div', class_='people-name')
        name = name_tag.get_text(strip=True) if name_tag else "Not Found"
        
        # Extracting email
        email_label = profile.find('div', class_='people-label', string=re.compile('Mail :'))
        email_tag = email_label.find_next('div') if email_label else None
        email = email_tag.get_text(strip=True).replace('[at]', '@') if email_tag else "Not Found"
        
        # Extracting research areas
        research_label = profile.find('div', class_='people-label', string=re.compile('Research Areas :'))
        research_tag = research_label.find_next('div') if research_label else None
        research_interests = research_tag.get_text(strip=True) if research_tag else ""
        
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
            professors.append([u_name, country, name, email, url])
    
    # Close the files
    # f.close()
    # f2.close()

    # Close the WebDriver
    driver.quit()
    print("Hacettepe University done")
    return professors

if __name__ == '__main__':
    hacettepe()
