from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv
import re
from bs4 import BeautifulSoup

def uab_faculty():
    # Set up Selenium WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    base_url = "https://www.uab.edu"
    faculty_directory_url = f"{base_url}/cas/computerscience/people/faculty-directory"
    driver.get(faculty_directory_url)
    driver.implicitly_wait(10)

    # Parse the main faculty directory page
    soup = BeautifulSoup(driver.page_source, "html.parser")
    faculty_sections = soup.select('#wk-grid89b .uk-panel .uk-margin')

    # File setup for output
    txt_filename = "uab_faculty.txt"
    csv_filename = "uab_faculty.csv"

    txt_file = open(txt_filename, "w", encoding="utf-8")
    csv_file = open(csv_filename, "w", newline='', encoding="utf-8")
    csvwriter = csv.writer(csv_file)

    # Write CSV header
    csvwriter.writerow(["University", "Country", "Name", "Email", "Website", "Research Areas"])

    # University and country information
    university = "University of Alabama at Birmingham, CS"
    country = "United States"

    # Keywords for filtering relevant faculty
    keyword_list = [
        'embedded systems', 'embedded software', 'hardware systems',
        'system architecture', 'IoT', 'real-time systems',
        'operating systems', 'system programming', 'system software',
        'distributed systems', 'kernel', 'machine learning', 'deep learning', 'artificial intelligence'
    ]

    # Process each faculty section
    for section in faculty_sections:
        try:
            # Extract name
            name_tag = section.find("h1")
            name = name_tag.get_text(strip=True) if name_tag else "Not Found"

            # Extract email
            email_tag = section.find("span")
            email = email_tag.get_text(strip=True) if email_tag else "Not Found"

            # Extract research areas
            research_tag = section.find("p", string=re.compile(r"Research and Teaching Interests"))
            research_text = research_tag.get_text(strip=True).replace("Research and Teaching Interests:", "").strip() if research_tag else "Not Found"

            # Extract website link
            website_tag = section.find("a", class_="uk-button")
            website = base_url + website_tag['href'] if website_tag else "Not Found"

            # Check if research matches any keywords
            if any(re.search(keyword, research_text, re.IGNORECASE) for keyword in keyword_list):
                # Save the relevant faculty's details
                txt_file.write(f"Name: {name}\nEmail: {email}\nWebsite: {website}\nUniversity: {university}\nCountry: {country}\nResearch Areas: {research_text}\n\n")
                csvwriter.writerow([university, country, name, email, website, research_text])

        except Exception as e:
            print(f"Error processing a faculty section: {e}")

    # Close files and driver
    txt_file.close()
    csv_file.close()
    driver.quit()

    print("Data extraction complete")

if __name__ == "__main__":
    uab_faculty()
