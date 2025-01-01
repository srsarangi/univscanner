from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv
import re
from bs4 import BeautifulSoup

def wm_faculty():
    # Set up Selenium WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    base_url = "https://www.wm.edu/as/computerscience/people/"
    driver.get(base_url)
    driver.implicitly_wait(10)

    # Parse the main faculty directory page
    soup = BeautifulSoup(driver.page_source, "html.parser")
    faculty_sections = soup.select('article.item_listing.directory_listing')

    # File setup for output
    txt_filename = "wm_faculty.txt"
    csv_filename = "wm_faculty.csv"

    txt_file = open(txt_filename, "w", encoding="utf-8")
    csv_file = open(csv_filename, "w", newline='', encoding="utf-8")
    csvwriter = csv.writer(csv_file)

    # Write CSV header
    csvwriter.writerow(["University", "Country", "Name", "Email", "Website", "Research Areas"])

    # University and country information
    university = "William & Mary, Computer Science"
    country = "USA"

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
            # Extract the professor's profile link
            profile_relative_url = section.find('a', class_='person_name')['href']
            profile_url = base_url + profile_relative_url

            # Visit the professor's profile page
            driver.get(profile_url)
            driver.implicitly_wait(10)
            profile_soup = BeautifulSoup(driver.page_source, "html.parser")

            # Extract professor's name
            name_tag = profile_soup.find("h1", class_="m-title__main-title")
            name = name_tag.get_text(strip=True) if name_tag else "Not Found"

            # Extract professor's email
            email_tag = profile_soup.find("a", href=re.compile(r"mailto:"))
            email = email_tag.get_text(strip=True) if email_tag else "Not Found"

            # Extract professor's website
            website = profile_url

            # Extract research areas
            research_area_tag = profile_soup.find("span", text=re.compile(r"Areas of Specialization"))
            research_area = research_area_tag.find_next("span").get_text(strip=True) if research_area_tag else "Not Found"

            # Check if research matches any keywords
            if any(re.search(keyword, research_area, re.IGNORECASE) for keyword in keyword_list):
                # Save the relevant professor's details
                txt_file.write(f"Name: {name}\nEmail: {email}\nWebsite: {website}\nUniversity: {university}\nCountry: {country}\nResearch Areas: {research_area}\n\n")
                csvwriter.writerow([university, country, name, email, website, research_area])

        except Exception as e:
            print(f"Error processing a faculty section: {e}")

    # Close files and driver
    txt_file.close()
    csv_file.close()
    driver.quit()

    print("Data extraction complete")

if __name__ == "__main__":
    wm_faculty()
