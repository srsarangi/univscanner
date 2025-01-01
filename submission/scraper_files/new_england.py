from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd

def extract_une_professors():
    # Initialize the Selenium WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    url = "https://www.une.edu.au/about-une/faculty-of-science-agriculture-business-and-law/school-of-science-and-technology/our-staff"
    driver.get(url)
    driver.implicitly_wait(10)

    # Parse the page source using BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Locate the table by ID
    table = soup.find("table", id="table84122")

    if not table:
        print("Table not found.")
        driver.quit()
        return

    # Extract data from the table rows
    rows = table.find_all("tr")
    professors = []
    req_names = ['Associate Professor William Billingsley', 'Associate Professor Mitchell Welch', 'Dr Farshid Hajati', 'Associate Professor David Paul']

    for row in rows:
        cells = row.find_all("td")
        if len(cells) >= 4:
            name_cell = cells[0]
            name = name_cell.get_text(strip=True)
            website_link = name_cell.find("a")["href"] if name_cell.find("a") else None

            # Handle exceptions
            if name == "Professor Raymond Chiong":
                continue
            if name == "Associate Professor David Paul":
                website_link = "https://www.une.edu.au/staff-profiles/science-and-technology/david-j-paul"

            if name in req_names:
                professors.append({
                    "Name": name,
                    "Website": website_link
                })

    # Close the WebDriver
    driver.quit()

    # Keyword list for matching teaching areas
    keyword_list = [
        'embedded systems', 'Embedded System', 'embedded software', 'hardware systems',
        'system architecture', 'IoT', 'real-time systems',
        'operating systems', 'Operating System', 'OS', 'system programming', 'system software',
        'distributed systems', 'kernel', 'machine learning', 'data mining', 'information security'
    ]

    # Visit individual websites to extract email and teaching areas
    u_name = "University of New England"
    country = "Australia"
    extracted_data = []
    for professor in professors:
        if not professor["Website"]:
            continue

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get(professor["Website"])
        driver.implicitly_wait(10)

        page_soup = BeautifulSoup(driver.page_source, "html.parser")

        # Extract email
        # Extract email
        p_tags = page_soup.find_all("p", class_="detail-2") 
        email = None
        for p_tag in p_tags:
            if "Email" in p_tag.text:
                a_tag = p_tag.find("a", href=True)
                if a_tag:
                    email = a_tag.get_text(strip=True)
                    break

        # Store extracted information
        extracted_data.append([u_name, country, professor["Name"], email, professor["Website"]])

        driver.quit()

    # Save the data to a CSV file
    # if extracted_data:
    #     df = pd.DataFrame(extracted_data)
    #     df.to_csv("new_england.csv", index=False)
    #     print("Data extracted and saved to 'new_england.csv'.")
    # else:
    #     print("No data found.")
    print("New England data extraction complete")
    return extracted_data

if __name__ == "__main__":
    extract_une_professors()
