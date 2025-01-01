from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv
import re
from bs4 import BeautifulSoup

def thapar_faculty():
    # Set up Selenium WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    base_url = "https://csed.thapar.edu"
    faculty_directory_url = f"{base_url}/faculty"
    driver.get(faculty_directory_url)
    driver.implicitly_wait(10)

    # Parse the faculty page
    soup = BeautifulSoup(driver.page_source, "html.parser")
    faculty_sections = soup.select('.row .faculty-elem')

    # File setup for output
    # txt_filename = "thapar_faculty_filtered.txt"
    # csv_filename = "thapar_faculty_filtered.csv"

    # txt_file = open(txt_filename, "w", encoding="utf-8")
    # csv_file = open(csv_filename, "w", newline='', encoding="utf-8")
    # csvwriter = csv.writer(csv_file)

    # # Write CSV header
    # csvwriter.writerow(["University", "Country", "Name", "Email", "Website", "Research Areas"])

    # University and country information
    university = "Thapar Institute of Engineering and Technology, CS"
    country = "India"
    profs = []

    # Keywords for filtering relevant faculty
    keyword_list = [
        # Embedded Systems Keywords
        'embedded systems', 'Embedded System', 'embedded software', 'hardware systems',
        'system architecture', 'IoT', 'real-time systems',
        
        # Operating Systems Keywords
        'operating systems', 'Operating System', 'OS', 'system programming', 'system software',
        'distributed systems', 'kernel'
    ]

    # Process each professor's section
    for section in faculty_sections:
        try:
            # Extract professor's name
            name_tag = section.select_one(".faculty-design strong")
            name = name_tag.get_text(strip=True) if name_tag else "Not Found"

            # Extract professor's email
            email_tag = section.select_one(".faculty-acad p:nth-child(4)")
            email = email_tag.get_text(strip=True) if email_tag else "Not Found"

            # Extract research areas
            specialization_tag = section.select_one(".faculty-acad p:nth-child(2)")
            specialization = specialization_tag.get_text(strip=True) if specialization_tag else "Not Found"

            # Extract professor's website link
            website_tag = section.select_one("a[target='_blank']")
            website = base_url + website_tag['href'] if website_tag else "Not Found"

            # Check if research matches any keywords
            if any(re.search(keyword, specialization, re.IGNORECASE) for keyword in keyword_list):
                # Save the relevant professor's details
                # txt_file.write(f"Name: {name}\nEmail: {email}\nWebsite: {website}\nUniversity: {university}\nCountry: {country}\nResearch Areas: {specialization}\n\n")
                # csvwriter.writerow([university, country, name, email, website, specialization])
                profs.append([university, country, name, email, website])

        except Exception as e:
            print(f"Error processing a professor section: {e}")

    # Close files and driver
    # txt_file.close()
    # csv_file.close()
    driver.quit()

    print("thapar faculty extraction complete")
    return profs

if __name__ == "__main__":
    thapar_faculty()
