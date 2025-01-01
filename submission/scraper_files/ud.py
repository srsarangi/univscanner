from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv
import re
from bs4 import BeautifulSoup

def ud_faculty():
    # Set up Selenium WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    base_url = "https://ud.ac.ae"
    faculty_directory_url = f"{base_url}/academics/college-of-engineering-it/faculties/"
    driver.get(faculty_directory_url)
    driver.implicitly_wait(10)

    # Parse the main faculty directory page to extract sections for professors
    soup = BeautifulSoup(driver.page_source, "html.parser")
    professor_sections = soup.select('.owl-carousel343 .singlemember')

    # File setup for output
    # txt_filename = "ud_faculty.txt"
    # csv_filename = "ud_faculty.csv"

    # txt_file = open(txt_filename, "w", encoding="utf-8")
    # csv_file = open(csv_filename, "w", newline='', encoding="utf-8")
    # csvwriter = csv.writer(csv_file)

    # # Write CSV header
    # csvwriter.writerow(["University", "Country", "Name", "Email", "Website", "Research Areas"])

    # University and country information
    university = "University of Dubai, College of Engineering and Information Technology"
    country = "United Arab Emirates"
    profs = []

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
            profile_relative_url = section.find('div', class_='LinksinMember').find('a')['href']
            
            # Check if the profile URL is relative or absolute
            if profile_relative_url.startswith("http"):
                profile_url = profile_relative_url  # Absolute URL, no need to append base URL
            else:
                profile_url = base_url + profile_relative_url  # Relative URL, append base URL

            # Visit the professor's profile page
            driver.get(profile_url)
            driver.implicitly_wait(10)
            profile_soup = BeautifulSoup(driver.page_source, "html.parser")

            # Extract professor's name
            name_tag = profile_soup.find("p", class_="membername2")
            name = name_tag.get_text(strip=True) if name_tag else "Not Found"

            # Extract professor's email
            email_tag = profile_soup.find("p", class_="memberemail2").find('a')
            email = email_tag.get_text(strip=True) if email_tag else "Not Found"

            # Extract professor's website (profile link)
            website = profile_url

            # Extract research areas from 'Teaching Areas'
            research_tag = profile_soup.find("div", id="accordioninner3")
            research_text = research_tag.get_text(strip=True) if research_tag else "Not Found"

            # Check if research matches any keywords
            if any(re.search(keyword, research_text, re.IGNORECASE) for keyword in keyword_list):
                # Save the relevant professor's details
                # txt_file.write(f"Name: {name}\nEmail: {email}\nWebsite: {website}\nUniversity: {university}\nCountry: {country}\nResearch Areas: {research_text}\n\n")
                # csvwriter.writerow([university, country, name, email, website, research_text])
                profs.append([university, country, name, email, website])

        except Exception as e:
            print(f"Error processing a professor section: {e}")

    # Close files and driver
    # txt_file.close()
    # csv_file.close()
    driver.quit()

    print("University of Dubai faculty data extraction complete")
    return profs

if __name__ == "__main__":
    ud_faculty()
