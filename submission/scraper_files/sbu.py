from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv
import re
from bs4 import BeautifulSoup

def sbu_faculty():
    # Set up Selenium WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    base_url = "https://en.sbu.ac.ir"
    faculty_directory_url = f"{base_url}/cv?p_p_id=ir_sain_university_people_UniversityFacultyListPortlet&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_ir_sain_university_people_UniversityFacultyListPortlet_universityDepartmentId=6516245"
    driver.get(faculty_directory_url)
    driver.implicitly_wait(10)

    # Parse the main faculty directory page
    soup = BeautifulSoup(driver.page_source, "html.parser")
    faculty_sections = soup.select('.row.users .col-md-6.col-xl-4 .item a')

    # File setup for output
    # txt_filename = "sbu_faculty.txt"
    # csv_filename = "sbu_faculty.csv"

    # txt_file = open(txt_filename, "w", encoding="utf-8")
    # csv_file = open(csv_filename, "w", newline='', encoding="utf-8")
    # csvwriter = csv.writer(csv_file)

    # # Write CSV header
    # csvwriter.writerow(["University", "Country", "Name", "Email", "Website", "Research Areas"])

    # University and country information
    university = "Shahid Beheshti University"
    country = "Iran"
    profs = []

    # Keywords for filtering relevant faculty
    keyword_list = [
        'embedded systems', 'embedded software', 'hardware systems',
        'system architecture', 'IoT', 'real-time systems',
        'operating systems', 'system programming', 'system software',
        'distributed systems', 'kernel', 'machine learning', 'deep learning', 'artificial intelligence'
    ]

    # Process each faculty section
    for faculty in faculty_sections:
        try:
            # Extract profile link
            profile_relative_url = faculty['href']
            profile_url = base_url + profile_relative_url

            # Visit the profile page
            driver.get(profile_url)
            driver.implicitly_wait(10)
            profile_soup = BeautifulSoup(driver.page_source, "html.parser")

            # Extract professor's name
            name_tag = profile_soup.find("h1", class_="title")
            if not name_tag:
                name_tag = profile_soup.find("img", alt=True)  # Fallback to image alt attribute
                name = name_tag["alt"] if name_tag else "Not Found"
            else:
                name = name_tag.get_text(strip=True)

            # Extract professor's email
            email_tag = profile_soup.find("div", string=re.compile("email", re.IGNORECASE))
            if email_tag:
                email_span = email_tag.find_next("span")
                email = email_span.get_text(strip=True).replace("[at]", "@") if email_span else "Not Found"
            else:
                email = "Not Found"

            # Extract professor's website
            website_tag = profile_soup.find("a", href=re.compile(r"http.*"))
            website = website_tag['href'] if website_tag else "Not Found"

            # Extract research areas
            research_tags = profile_soup.select('.tags .tag')
            research_list = [tag.get_text(strip=True) for tag in research_tags]
            research_text = ", ".join(research_list) if research_list else "Not Found"

            # Check if research matches any keywords
            if any(re.search(keyword, research_text, re.IGNORECASE) for keyword in keyword_list):
                # Save the relevant professor's details
                # txt_file.write(f"Name: {name}\nEmail: {email}\nWebsite: {website}\nUniversity: {university}\nCountry: {country}\nResearch Areas: {research_text}\n\n")
                # csvwriter.writerow([university, country, name, email, website, research_text])
                profs.append([university, country, name, email, website])

        except Exception as e:
            print(f"Error processing a faculty section: {e}")

    # Close files and driver
    # txt_file.close()
    # csv_file.close()
    driver.quit()

    print("sbu_faculty complete")
    return profs

if __name__ == "__main__":
    sbu_faculty()
