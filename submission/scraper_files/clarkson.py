from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv
import re
from bs4 import BeautifulSoup

def clarkson_faculty():
    # Set up Selenium WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    base_url = "https://www.clarkson.edu"
    faculty_directory_url = f"{base_url}/academics/schools-colleges/arts-sciences/departments/computer-science/faculty-staff"
    driver.get(faculty_directory_url)
    driver.implicitly_wait(10)

    # Parse the faculty directory page
    soup = BeautifulSoup(driver.page_source, "html.parser")
    professor_sections = soup.select('.faculty-list__item')

    # File setup for output
    # txt_filename = "clarkson_faculty.txt"
    # csv_filename = "clarkson_faculty.csv"

    # txt_file = open(txt_filename, "w", encoding="utf-8")
    # csv_file = open(csv_filename, "w", newline='', encoding="utf-8")
    # csvwriter = csv.writer(csv_file)

    # Write CSV header
    # csvwriter.writerow(["University", "Country", "Name", "Email", "Website", "Research Areas"])

    # University and country information
    university = "Clarkson University"
    country = "USA"
    professors = []

    # Keywords for filtering relevant faculty
    keyword_list = [
        'embedded systems', 'embedded software', 'hardware systems',
        'system architecture', 'IoT', 'real-time systems',
        'operating systems', 'system programming', 'system software',
        'distributed systems', 'kernel', 'machine learning', 'deep learning', 'artificial intelligence'
    ]

    # Process each professor's section
    for section in professor_sections:
        try:
            # Extract the professor's profile link
            profile_relative_url = section.find('a', class_='link-u')['href']
            profile_url = base_url + profile_relative_url

            # Visit the professor's profile page
            driver.get(profile_url)
            driver.implicitly_wait(10)
            profile_soup = BeautifulSoup(driver.page_source, "html.parser")

            # Extract professor's name
            name_tag = profile_soup.find("h1", class_="h2")
            name = name_tag.get_text(strip=True) if name_tag else "Not Found"

            # Extract professor's email
            email_tag = profile_soup.find("a", href=re.compile(r"mailto:"))
            email = email_tag.get_text(strip=True) if email_tag else "Not Found"

            # Extract professor's website (profile link)
            website = profile_url

            # Extract research areas or areas of interest
            research_area_tag = profile_soup.find("div", class_="main__content")
            research_text = "Not Found"
            if research_area_tag:
                research_area_tag = research_area_tag.find("h2", string="Research Interests")
                if research_area_tag:
                    research_text = research_area_tag.find_next("p").get_text(strip=True)

            # Check if research matches any keywords
            if any(re.search(keyword, research_text, re.IGNORECASE) for keyword in keyword_list):
                # Save the relevant professor's details
                # txt_file.write(f"Name: {name}\nEmail: {email}\nWebsite: {website}\nUniversity: {university}\nCountry: {country}\nResearch Areas: {research_text}\n\n")
                # csvwriter.writerow([university, country, name, email, website, research_text])
                professors.append([university, country, name, email, website])

        except Exception as e:
            print(f"Error processing a professor section: {e}")

    # Close files and driver
    # txt_file.close()
    # csv_file.close()
    driver.quit()
    print('Clarkson faculty data extraction complete')
    return professors

if __name__ == "__main__":
    clarkson_faculty()
