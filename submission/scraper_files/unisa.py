from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def unisa_faculty():
    # Set up Selenium WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    base_url = "https://osprey.unisa.ac.za"
    faculty_directory_url = f"{base_url}/index_cs.html"
    driver.get(faculty_directory_url)
    driver.implicitly_wait(10)

    # Parse the main faculty directory page to extract sections for professors
    soup = BeautifulSoup(driver.page_source, "html.parser")
    faculty_links = soup.find_all("a", href=re.compile(r"staff/staff.htm\?qemail="))

    # File setup for output
    # txt_filename = "unisa_faculty.txt"
    # csv_filename = "unisa_faculty.csv"

    # txt_file = open(txt_filename, "w", encoding="utf-8")
    # csv_file = open(csv_filename, "w", newline='', encoding="utf-8")
    # csvwriter = csv.writer(csv_file)

    # Write CSV header
    # csvwriter.writerow(["University", "Country", "Name", "Email", "Website", "Research Areas"])

    # University and country information
    university = "University of South Africa, CS"
    country = "South Africa"
    profs = []

    # Keywords for filtering relevant faculty
    keyword_list = [
        'embedded systems', 'embedded software', 'hardware systems',
        'system architecture', 'IoT', 'real-time systems',
        'operating systems', 'system programming', 'system software',
        'distributed systems', 'kernel', 'machine learning', 'deep learning', 'artificial intelligence'
    ]

    # Process each professor's profile link
    for link in faculty_links:
        try:
            # Extract the professor's profile link (ensure correct URL handling)
            profile_url = link['href']
            full_profile_url = urljoin(base_url, profile_url)  # Use urljoin to fix relative URLs
            driver.get(full_profile_url)
            driver.implicitly_wait(10)
            profile_soup = BeautifulSoup(driver.page_source, "html.parser")

            # Extract professor's name
            name_tag = profile_soup.find("strong")
            name = name_tag.get_text(strip=True) if name_tag else "Not Found"

            # Extract email from the email section (JavaScript part)
            email_tag = profile_soup.find("td", text=re.compile(r"eMail"))
            email = "Not Found"
            if email_tag:
                email_parts = email_tag.find_next("td").get_text(strip=True)
                # Handle email construction from parts
                if "at" in email_parts:
                    email = email_parts.replace("at", "@") + ".ac.za"

            # Extract professor's website (Personal Profile Page link)
            website_tag = profile_soup.find("a", href=re.compile(r"https://osprey.unisa.ac.za/research/profile2.htm"))
            website = website_tag['href'] if website_tag else "Not Found"

            # Extract research areas (Modules)
            modules_tag = profile_soup.find("td", text="Modules")
            modules = modules_tag.find_next("td").get_text(strip=True) if modules_tag else "Not Found"

            # Check if research matches any keywords
            if any(re.search(keyword, modules, re.IGNORECASE) for keyword in keyword_list):
                # Save the relevant professor's details
                # txt_file.write(f"Name: {name}\nEmail: {email}\nWebsite: {website}\nUniversity: {university}\nCountry: {country}\nResearch Areas: {modules}\n\n")
                # csvwriter.writerow([university, country, name, email, website, modules])
                profs.append([university, country, name, email, website])

        except Exception as e:
            print(f"Error processing a professor section: {e}")

    # Close files and driver
    # txt_file.close()
    # csv_file.close()
    driver.quit()

    print("unisa faculty extraction complete")
    return profs

if __name__ == "__main__":
    unisa_faculty()
