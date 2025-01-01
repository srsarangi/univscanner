from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv
import re
from bs4 import BeautifulSoup

def scrape_sfedu_faculty():
    # Set up Selenium WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    base_url = "https://msrn.sfedu.ru/rc/facultyresearchers"
    driver.get(base_url)
    driver.implicitly_wait(10)

    # Parse the main faculty directory page
    soup = BeautifulSoup(driver.page_source, "html.parser")
    faculty_sections = soup.find_all("div", class_="t526__itemwrapper")

    # File setup for output
    txt_filename = "sfedu_faculty.txt"
    csv_filename = "sfedu_faculty.csv"

    txt_file = open(txt_filename, "w", encoding="utf-8")
    csv_file = open(csv_filename, "w", newline='', encoding="utf-8")
    csvwriter = csv.writer(csv_file)

    # Write CSV header
    csvwriter.writerow(["University", "Country", "Name", "Email", "Website", "Research Areas"])

    # University and country information
    university = "Southern Federal University (SFedU), Regional Mathematical Center"
    country = "Russia"

    # Keywords for filtering relevant faculty
    keyword_list = [
        'embedded systems', 'embedded software', 'hardware systems',
        'system architecture', 'IoT', 'real-time systems',
        'operating systems', 'system programming', 'system software',
        'distributed systems', 'kernel', 'machine learning', 'deep learning', 'artificial intelligence'
    ]

    # Process each professor's section
    for section in faculty_sections:
        try:
            # Extract professor's name
            name_tag = section.find("div", class_="t526__persname")
            name = name_tag.get_text(strip=True) if name_tag else "Not Found"

            # Extract research interests
            research_text = "Not Found"
            research_tag = section.find("div", class_="t526__perstext")
            if research_tag:
                research_content = research_tag.get_text(strip=True)
                match = re.search(r"(?i)Research interests: (.+?)(\n|<br>|$)", research_content)
                if match:
                    research_text = match.group(1)

            # Extract links
            links = section.find_all("a", href=True)
            email = "Not Found"
            website = "Not Found"
            for link in links:
                href = link["href"]
                if "mailto:" in href:
                    email = href.replace("mailto:", "")
                elif "http" in href and website == "Not Found":
                    website = href

            # Check if research matches any keywords
            if any(re.search(keyword, research_text, re.IGNORECASE) for keyword in keyword_list):
                # Save the relevant professor's details
                txt_file.write(f"Name: {name}\nEmail: {email}\nWebsite: {website}\nUniversity: {university}\nCountry: {country}\nResearch Areas: {research_text}\n\n")
                csvwriter.writerow([university, country, name, email, website, research_text])

        except Exception as e:
            print(f"Error processing a professor section: {e}")

    # Close files and driver
    txt_file.close()
    csv_file.close()
    driver.quit()

    print("Data extraction complete")

if __name__ == "__main__":
    scrape_sfedu_faculty()
