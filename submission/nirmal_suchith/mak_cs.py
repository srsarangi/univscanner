from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import csv
from bs4 import BeautifulSoup
import re

def mak_cs_faculty():
    # Setup Selenium WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    base_url = "https://cs.mak.ac.ug"
    faculty_directory_url = f"{base_url}/people/faculty"
    driver.get(faculty_directory_url)
    driver.implicitly_wait(10)

    # File setup for output
    txt_filename = "mak_cs_faculty.txt"
    csv_filename = "mak_cs_faculty.csv"
    txt_file = open(txt_filename, "w", encoding="utf-8")
    csv_file = open(csv_filename, "w", newline='', encoding="utf-8")
    csvwriter = csv.writer(csv_file)
    csvwriter.writerow(["University", "Country", "Name", "Email", "Website", "Research Areas"])

    # University and country information
    university = "Makerere University, CS"
    country = "Uganda"
    keyword_list = [
        'embedded systems', 'embedded software', 'hardware systems',
        'system architecture', 'IoT', 'real-time systems',
        'operating systems', 'system programming', 'system software',
        'distributed systems', 'kernel', 'machine learning', 'deep learning', 'artificial intelligence'
    ]

    def extract_email(script_tags):
        """Decodes dynamically rendered email."""
        for script in script_tags:
            email_match = re.search(r'window\.open\(&quot;mailto:(.*?)&quot;', script.string)
            if email_match:
                return email_match.group(1)
        return "Not Found"

    # Loop through paginated pages
    while True:
        soup = BeautifulSoup(driver.page_source, "html.parser")
        faculty_sections = soup.select("div.col-lg-8.col-md-8.col-sm-12.col-xs-12.person-details")

        for section in faculty_sections:
            try:
                # Extract profile link
                profile_link_tag = section.find("a", class_="btn btn-xs btn-default")
                profile_url = profile_link_tag['href'] if profile_link_tag else None
                if profile_url:
                    driver.get(profile_url)
                    driver.implicitly_wait(10)
                    profile_soup = BeautifulSoup(driver.page_source, "html.parser")

                    # Extract name
                    name_tag = profile_soup.find("h1", class_="person-name")
                    name = name_tag.get_text(strip=True) if name_tag else "Not Found"

                    # Extract email
                    email_script_tags = profile_soup.find_all("script", string=re.compile(r'mailto'))
                    email = extract_email(email_script_tags)

                    # Extract research areas
                    research_tag = profile_soup.find("div", class_="person-details-row")
                    if research_tag and "Research/Teaching Interests" in research_tag.get_text():
                        research_text = research_tag.find_next("p").get_text(strip=True)
                    else:
                        research_text = "Not Found"

                    # Filter by keywords
                    if any(keyword.lower() in research_text.lower() for keyword in keyword_list):
                        txt_file.write(f"Name: {name}\nEmail: {email}\nWebsite: {profile_url}\nUniversity: {university}\nCountry: {country}\nResearch Areas: {research_text}\n\n")
                        csvwriter.writerow([university, country, name, email, profile_url, research_text])
            except Exception as e:
                print(f"Error processing faculty profile: {e}")

        # Navigate to the next page if available
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, "li.cs-pagination-circle.next")
            if next_button.get_attribute("data-faculty-enabled") == "true":
                next_button.click()
                driver.implicitly_wait(10)
            else:
                break
        except Exception:
            break

    # Close files and driver
    txt_file.close()
    csv_file.close()
    driver.quit()
    print("Data extraction complete")

if __name__ == "__main__":
    mak_cs_faculty()
