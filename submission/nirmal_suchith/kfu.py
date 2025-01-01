from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import csv
import re
import time

def kfu():
    # Set up Selenium WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    
    # Navigate to the page
    url = "https://www.kfu.edu.sa/en/Colleges/business-administration/CollegeDepartments/Pages/informationdep5.aspx"
    driver.get(url)
    
    # Allow the page to load fully
    time.sleep(5)  # Adjust the sleep time based on your internet speed and page load time

    # File setup for output
    filename = "kfu_faculty.txt"
    f = open(filename, "w", encoding="utf-8")
    
    excel_filename = "kfu_faculty.csv"
    f2 = open(excel_filename, "w", newline='', encoding="utf-8")
    csvwriter = csv.writer(f2)
    
    # Write header for CSV
    csvwriter.writerow(["University", "Country", "Name", "Email", "Research Area"])
    
    # University details
    u_name = "King Faisal University"
    country = "Saudi Arabia"
    
    # Research keywords
    keyword_list = [
        'embedded systems', 'Embedded System', 'embedded software', 'hardware systems',
        'system architecture', 'IoT', 'real-time systems',
        'operating systems', 'Operating System', 'OS', 'system programming', 'system software',
        'distributed systems', 'kernel'
    ]
    
    # Extract faculty cards (each card contains a faculty member's info)
    faculty_cards = driver.find_elements(By.CSS_SELECTOR, "div.cards")
    
    for card in faculty_cards:
        # Extract name
        try:
            name_tag = card.find_element(By.CLASS_NAME, 'fname')
            name = name_tag.text.strip() if name_tag else "Not Found"
        except:
            name = "Not Found"
        
        # Extract email
        try:
            email_tag = card.find_element(By.XPATH, ".//a[starts-with(@href, 'mailto:')]")
            email = email_tag.text.strip() if email_tag else "Not Found"
        except:
            email = "Not Found"
        
        # Extract research or position info (inside <p> tag)
        try:
            detail_tag = card.find_element(By.XPATH, ".//p")
            research_area = detail_tag.text.strip() if detail_tag else "Not Available"
        except:
            research_area = "Not Available"
        
        # Check if research area matches keywords
        flag = False
        for keyword in keyword_list:
            if re.search(keyword, research_area, re.IGNORECASE):
                flag = True
                break
        
        # If there's a match, write data to text and CSV files
        if flag:
            f.write(f"Name: {name}\nEmail: {email}\nResearch Area: {research_area}\nUniversity: {u_name}\n\n")
            csvwriter.writerow([u_name, country, name, email, research_area])
    
    # Close the files and quit the driver
    f.close()
    f2.close()
    driver.quit()
    print("Data extraction complete")

if __name__ == '__main__':
    kfu()
