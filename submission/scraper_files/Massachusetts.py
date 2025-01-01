from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd

def massachusetts():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    url = "https://www.umb.edu/directory/ductran/"
    driver.get(url)
    driver.implicitly_wait(10)

    # Locate the email element using its XPath
    try:
        email_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/main/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/div[2]/div/div[4]/div[1]/div/a")
        email_href = email_element.get_attribute("href")

        # Extract the email from the href attribute
        if email_href.startswith("mailto:"):
            email = email_href.split(":")[1]
        else:
            email = None

        # print(f"Extracted email: {email}")
    except Exception as e:
        print(f"Error occurred: {e}")

    # Example of additional processing using BeautifulSoup
    keyword_list = [
        'embedded systems', 'Embedded System', 'embedded software', 'hardware systems',
        'system architecture', 'IoT', 'real-time systems',
        'operating systems', 'Operating System', 'OS', 'system programming', 'system software',
        'distributed systems', 'kernel', 'machine learning', 'data mining', 'information security'
    ]
    professors = []
    university_name = "University of Massachusetts Boston"
    country = "United States"
    professors.append([university_name, country, "Dr. Duc Tran", email, url])


    # Additional processing logic can go here

    driver.quit()

    # if professors:
    #     df = pd.DataFrame(professors)
    #     df.to_csv("massachusetts.csv", index=False)
    #     print("Data saved to CSV file.")
    # else:
    #     print("No data found.")
    print("Massachusetts faculty data extracted.")
    return professors

if __name__ == "__main__":
    massachusetts()
