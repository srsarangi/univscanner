from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv
import re
from bs4 import BeautifulSoup

def kpi_faculty():
    # Set up Selenium WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    faculty_directory_url = "https://web.kpi.kharkov.ua/asu/about-department/teaching-staff-2/"
    driver.get(faculty_directory_url)
    driver.implicitly_wait(10)

    # Parse the faculty page to extract sections for professors
    soup = BeautifulSoup(driver.page_source, "html.parser")
    professor_sections = soup.find_all("figure", {"class": "wp-caption"})

    # File setup for output
    # txt_filename = "kpi_faculty.txt"
    # csv_filename = "kpi_faculty.csv"

    # txt_file = open(txt_filename, "w", encoding="utf-8")
    # csv_file = open(csv_filename, "w", newline='', encoding="utf-8")
    # csvwriter = csv.writer(csv_file)

    # # Write CSV header
    # csvwriter.writerow(["University", "Country", "Name", "Email", "Website", "Research Areas"])

    # University and country information
    university = "Kharkiv Polytechnic Institute"
    country = "Ukraine"
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
            # Extract the professor's name
            name_tag = section.find("figcaption")
            name = name_tag.get_text(strip=True) if name_tag else "Not Found"

            # Extract research areas
            paragraph_tags = section.find_all("p")
            research_area = "Not Found"
            for paragraph in paragraph_tags:
                if "Research areas:" in paragraph.get_text():
                    research_area = paragraph.get_text(strip=True).split("Research areas:")[1].strip()

            # Check if research matches any keywords
            if any(re.search(keyword, research_area, re.IGNORECASE) for keyword in keyword_list):
                # Extract email (if present)
                email_tag = section.find("a", href=re.compile(r"mailto:"))
                email = email_tag.get_text(strip=True) if email_tag else "Not Found"

                # Extract website link (if present)
                website_tag = section.find("a", href=re.compile(r"http.*"))
                website = website_tag['href'] if website_tag else "Not Found"

                # Save the relevant professor's details
                # txt_file.write(f"Name: {name}\nEmail: {email}\nWebsite: {website}\nUniversity: {university}\nCountry: {country}\nResearch Areas: {research_area}\n\n")
                # csvwriter.writerow([university, country, name, email, website, research_area])
                profs.append([university, country, name, email, website])

        except Exception as e:
            print(f"Error processing a professor section: {e}")

    # Close files and driver
    # txt_file.close()
    # csv_file.close()
    driver.quit()

    print("Kharkiv Polytechnic Institute faculty data extraction complete")
    return profs

if __name__ == "__main__":
    kpi_faculty()
