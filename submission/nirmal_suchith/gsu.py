import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import csv
import re

def gsu_faculty():
    # Set up Chrome options for headless browsing (avoids opening a browser window)
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    
    # Set up Selenium WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    base_url = "https://cas.gsu.edu/profile-directory/?wpv-department=computer-science&wpv_aux_current_post_id=13610&wpv_view_count=13592-TCPID13610&wpv_paged="
    current_page = 1
    txt_filename = "gsu_faculty.txt"
    csv_filename = "gsu_faculty.csv"

    # File setup for output
    txt_file = open(txt_filename, "w", encoding="utf-8")
    csv_file = open(csv_filename, "w", newline='', encoding="utf-8")
    csvwriter = csv.writer(csv_file)

    # Write CSV header
    csvwriter.writerow(["University", "Country", "Name", "Email", "Website", "Research Areas"])

    # University and country information
    university = "Georgia State University, CS"
    country = "USA"

    # Keywords for filtering relevant faculty
    keyword_list = [
        'embedded systems', 'embedded software', 'hardware systems',
        'system architecture', 'IoT', 'real-time systems',
        'operating systems', 'system programming', 'system software',
        'distributed systems', 'kernel', 'machine learning', 'deep learning', 'artificial intelligence'
    ]
    
    while True:
        # Open the faculty directory page for the current page number
        driver.get(f"{base_url}{current_page}")
        driver.implicitly_wait(10)
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Find all professor profile links in the current page
        professor_sections = soup.select('#wpv-view-layout-13592-TCPID13610 #profile_row a[href]')
        if not professor_sections:
            print("No more professor links found. Exiting.")
            break

        # Process each professor's profile
        for section in professor_sections:
            try:
                profile_url = section['href']
                print(f"Processing {profile_url}")
                
                # Visit the professor's profile page
                driver.get(profile_url)
                driver.implicitly_wait(10)
                profile_soup = BeautifulSoup(driver.page_source, "html.parser")
                
                # Extract professor's name
                name_tag = profile_soup.find("h3")
                name = name_tag.get_text(strip=True) if name_tag else "Not Found"
                
                # Extract professor's email
                email_tag = profile_soup.find("a", href=re.compile(r"mailto:"))
                email = email_tag.get_text(strip=True) if email_tag else "Not Found"
                
                # Extract professor's website (profile link)
                website = profile_url
                
                # Extract research areas from "Specializations"
                research_tags = profile_soup.select('.vc_tta-panel-body dl dd')
                research_list = [tag.get_text(strip=True) for tag in research_tags]
                research_text = ", ".join(research_list) if research_list else "Not Found"

                # Check if research matches any keywords
                if any(re.search(keyword, research_text, re.IGNORECASE) for keyword in keyword_list):
                    # Save the relevant professor's details
                    txt_file.write(f"Name: {name}\nEmail: {email}\nWebsite: {website}\nUniversity: {university}\nCountry: {country}\nResearch Areas: {research_text}\n\n")
                    csvwriter.writerow([university, country, name, email, website, research_text])

            except Exception as e:
                print(f"Error processing a professor section: {e}")

            # Add a random delay between requests to avoid detection
            time.sleep(random.uniform(2, 5))  # Random delay between 2 and 5 seconds

        # Check if there's a next page to move to
        next_page_button = driver.find_elements_by_xpath("//a[contains(text(),'Next')]")
        if next_page_button:
            current_page += 1
            time.sleep(random.uniform(3, 5))  # Random delay before loading the next page
        else:
            print("No more pages. Exiting.")
            break

    # Close files and driver
    txt_file.close()
    csv_file.close()
    driver.quit()

    print("Data extraction complete")

if __name__ == "__main__":
    gsu_faculty()
