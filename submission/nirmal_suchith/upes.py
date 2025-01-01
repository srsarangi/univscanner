from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import csv
import time

def upes_faculty_scraper():
    # Set up Selenium WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    base_url = "https://www.upes.ac.in/faculty"
    driver.get(base_url)
    driver.maximize_window()

    wait = WebDriverWait(driver, 15)

    # Select "School of Computer Science" from the dropdown
    try:
        dropdown_container = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".selectBox .selectedValue"))
        )
        dropdown_container.click()  # Open the dropdown
        time.sleep(1)  # Give the dropdown menu time to render
        
        # Select the "School of Computer Science" option
        school_option = driver.find_element(By.XPATH, "//option[@value='School of Computer Science']")
        driver.execute_script("arguments[0].selected = true;", school_option)
        driver.execute_script("arguments[0].click();", school_option)
        time.sleep(3)
    except Exception as e:
        print(f"Error selecting dropdown option: {e}")
        driver.quit()
        return

    # Prepare files for output
    txt_filename = "upes_faculty.txt"
    csv_filename = "upes_faculty.csv"

    txt_file = open(txt_filename, "w", encoding="utf-8")
    csv_file = open(csv_filename, "w", newline='', encoding="utf-8")
    csvwriter = csv.writer(csv_file)
    csvwriter.writerow(["University", "Country", "Name", "Email", "Website", "Research Areas"])

    # University and country information
    university = "UPES"
    country = "India"

    # Keywords for filtering relevant faculty
    keyword_list = [
        'embedded systems', 'embedded software', 'hardware systems',
        'system architecture', 'IoT', 'real-time systems',
        'operating systems', 'system programming', 'system software',
        'distributed systems', 'kernel', 'machine learning', 'deep learning', 'artificial intelligence'
    ]

    def extract_faculty_details(profile_url):
        driver.get(profile_url)
        time.sleep(2)

        profile_soup = BeautifulSoup(driver.page_source, "html.parser")

        # Extract name and designation
        name_tag = profile_soup.select_one(".leader-name")
        name = name_tag.get_text(strip=True) if name_tag else "Not Found"

        # Extract email
        email = "Not Found"
        try:
            contact_button = driver.find_element(By.XPATH, "//p[text()='Contact']")
            driver.execute_script("arguments[0].click();", contact_button)
            time.sleep(1)
            email_tag = profile_soup.select_one("a[href^='mailto:']")
            email = email_tag.get_text(strip=True) if email_tag else "Not Found"
        except Exception:
            pass

        # Extract research areas
        research_areas = "Not Found"
        try:
            research_button = driver.find_element(By.XPATH, "//p[text()='Research']")
            driver.execute_script("arguments[0].click();", research_button)
            time.sleep(1)
            research_tag = profile_soup.select_one(".commonAccordian_content p")
            research_areas = research_tag.get_text(strip=True) if research_tag else "Not Found"
        except Exception:
            pass

        # Filter by research keywords
        if any(keyword.lower() in research_areas.lower() for keyword in keyword_list):
            txt_file.write(f"Name: {name}\nEmail: {email}\nWebsite: {profile_url}\nUniversity: {university}\nCountry: {country}\nResearch Areas: {research_areas}\n\n")
            csvwriter.writerow([university, country, name, email, profile_url, research_areas])

    # Loop through all faculty profiles
    while True:
        soup = BeautifulSoup(driver.page_source, "html.parser")
        faculty_cards = soup.select("#facultyDataLoad .inner-icon-cards a.arrow-button")

        for card in faculty_cards:
            profile_url = "https://www.upes.ac.in" + card.get("href")
            extract_faculty_details(profile_url)

        # Check if "Load More" button is available
        try:
            load_more_button = driver.find_element(By.ID, "loadMoreDataAPI")
            driver.execute_script("arguments[0].click();", load_more_button)
            time.sleep(3)  # Wait for new profiles to load
        except Exception:
            break  # No more profiles to load

    # Close files and driver
    txt_file.close()
    csv_file.close()
    driver.quit()

    print("Data extraction complete")

if __name__ == "__main__":
    upes_faculty_scraper()
