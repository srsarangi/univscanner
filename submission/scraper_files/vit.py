from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import csv
import re
from bs4 import BeautifulSoup
import time

def vit_chennai():
    # Set up Selenium WebDriver (Chrome)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    base_url = "https://chennai.vit.ac.in/computer-science-engineering-chennai/faculty/"
    driver.get(base_url)
    driver.implicitly_wait(10)
    
    # Parse the main page
    soup = BeautifulSoup(driver.page_source, "html.parser")
    profile_links = [
        a['href'] for a in soup.find_all('a', href=True) 
        if "/member/" in a['href']
    ]
    
    # File setup for output
    # filename = "vit_chennai_faculty.txt"
    # f = open(filename, "w", encoding="utf-8")
    
    # excel_filename = "vit_chennai_faculty.csv"
    # f2 = open(excel_filename, "w", newline='', encoding="utf-8")
    # csvwriter = csv.writer(f2)
    # csvwriter.writerow(["University", "Country", "Name", "Email", "Research Areas"])
    
    # Set the university name and country
    u_name = "VIT Chennai"
    country = "India"
    profs = []
    
    # Research keywords
    keyword_list = [
        'embedded systems', 'Embedded System', 'embedded software', 'hardware systems',
        'system architecture', 'IoT', 'real-time systems',
        'operating systems', 'Operating System', 'OS', 'system programming', 'system software',
        'distributed systems', 'kernel', 'machine learning', 'data mining', 'information security'
    ]
    
    # Process each profile
    for link in profile_links:
        driver.get(link)
        time.sleep(2)  # Give time for the page to load
        profile_soup = BeautifulSoup(driver.page_source, "html.parser")
        
        # Extract name
        name_tag = profile_soup.find("h3", class_="item-title")
        name = name_tag.get_text(strip=True) if name_tag else "Not Found"
        
        # Extract email
        email_tag = profile_soup.find("p", text=re.compile("Email:"))
        email = email_tag.get_text(strip=True).replace("Email: ", "") if email_tag else "Not Found"
        
        # Extract research areas
        research_tag = profile_soup.find("p", text=re.compile("Research Area:"))
        research_interests = research_tag.get_text(strip=True).replace("Research Area: ", "") if research_tag else "Not Found"
        
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
            profs.append([u_name, country, name, email, link])
    
    # Close files and browser
    # f.close()
    # f2.close()
    driver.quit()

    print("VIT Chennai extracted faculty")
    return profs

if __name__ == '__main__':
    vit_chennai()
