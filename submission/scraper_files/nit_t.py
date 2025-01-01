from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import csv
import re

def nitt_faculty():
    # Set up Selenium WebDriver (using Chrome in this case)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    url = "https://www.nitt.edu/home/academics/departments/cse/faculty/"
    driver.get(url)  # Load the page
    
    # Give the page some time to load
    driver.implicitly_wait(10)
    
    # Parse the page content using BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    # File setup for output
    # filename = "nitt_faculty.txt"
    # f = open(filename, "w")
    
    # excel_filename = "nitt_faculty.csv"
    # f2 = open(excel_filename, "w", newline='', encoding="utf-8")
    # csvwriter = csv.writer(f2)
    
    # Set the university name and country
    u_name = "National Institute of Technology, Tiruchirappalli"
    country = "India"
    profs = []
    
    # Research keywords for embedded systems or operating systems
    keyword_list = [
        'embedded systems', 'Embedded System', 'embedded software', 'hardware systems',
        'system architecture', 'IoT', 'real-time systems',
        'operating systems', 'Operating System', 'OS', 'system programming', 'system software',
        'distributed systems', 'kernel'
    ]
    
    # Extracting all faculty profile links (with <a> tags inside <div> with class 'facitem left')
    faculty_profiles = soup.find_all('div', class_='facitem left')
    
    # Loop through each faculty profile to extract details
    for profile in faculty_profiles:
        # Extracting the link to the individual faculty page
        link_tag = profile.find('a', href=True)
        if link_tag:
            faculty_link = link_tag['href']
            
            # Visit the faculty's individual page
            driver.get(f"https://www.nitt.edu/home/academics/departments/cse/faculty/{faculty_link}")
            
            # Give time for the page to load
            driver.implicitly_wait(10)
            
            # Parse the individual faculty page content
            faculty_soup = BeautifulSoup(driver.page_source, "html.parser")
            
            # Try to locate the table containing the faculty's details
            table = faculty_soup.find('table', class_='nitttable')
            
            # If the table exists, process it
            if table:
                rows = table.find_all('tr')
                name, email, specialization = None, None, None
                
                # Loop through the rows to extract data
                for row in rows:
                    columns = row.find_all('td')
                    if len(columns) > 1:
                        header = columns[0].get_text(strip=True)
                        data = columns[1].get_text(strip=True)
                        
                        # Extract Name
                        if "Name" in header:
                            name = data
                        # Extract Email
                        elif "E-mail Id" in header:
                            email = data
                        # Extract Specialization
                        elif "Specialization" in header:
                            specialization = data
                
                # Check if any specialization matches the research keywords
                flag = False
                if specialization:
                    for keyword in keyword_list:
                        if re.search(keyword, specialization, re.IGNORECASE):
                            flag = True
                            break
                
                # If keyword matches, write to files
                if flag:
                    # f.write(f"Name: {name}\nEmail: {email}\nUniversity: {u_name}\nSpecialization: {specialization}\n\n")
                    # csvwriter.writerow([u_name, country, name, email, specialization])
                    profs.append([u_name, country, name, email, url])
    
    # Close the files
    # f.close()
    # f2.close()
    
    # Close the WebDriver
    driver.quit()

    print("NITT Data extraction complete")
    return profs

if __name__ == '__main__':
    nitt_faculty()
