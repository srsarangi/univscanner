from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd

import re

def vermont():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    base_0 = "https://www.uvm.edu/"
    base_url = "https://www.uvm.edu/cems/cs/faculty"
    driver.get(base_url)
    driver.implicitly_wait(10)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Research keywords
    keyword_list = [
        'embedded systems', 'Embedded System', 'embedded software', 'hardware systems',
        'system architecture', 'IoT', 'real-time systems',
        'operating systems', 'Operating System', 'OS', 'system programming', 'system software',
        'distributed systems', 'kernel', 'machine learning', 'data mining', 'information security'
    ]

    xpaths = [
        "/html/body/div[2]/main/div/div[5]/article/div/div[2]/div[1]",
        "/html/body/div[2]/main/div/div[5]/article/div/div[2]/div[2]",
        "/html/body/div[2]/main/div/div[5]/article/div/div[2]/div[3]",
        "/html/body/div[2]/main/div/div[5]/article/div/div[2]/div[4]",
        "/html/body/div[2]/main/div/div[5]/article/div/div[2]/div[5]"
    ]

    # if we find the keyword in interest , we need to store name, email, href link from name,


    unviersty_name = "University of Vermont"
    country = "USA"

    fields = []
    for i, xpath in enumerate(xpaths, start=1):
        try:
            parent_div = driver.find_element(By.XPATH, xpath)
            section = parent_div.find_element(By.CSS_SELECTOR, "section.profile-queue.list")
            nested_divs = section.find_elements(By.CSS_SELECTOR, "div.person.animated.animatedFadeInUp.InViewport")

            for j, div in enumerate(nested_divs, start=1):
                name_tag = div.find_element(By.CSS_SELECTOR, "p.profile-name a")
                name = name_tag.text.strip()
                rel_link = name_tag.get_attribute("href")
                profile_link = base_0 + rel_link if rel_link.startswith("/") else rel_link

                email_tag = div.find_element(By.CSS_SELECTOR, "a.profile-email")
                email = email_tag.get_attribute("innerText")

                expertise_tag = div.find_elements(By.CSS_SELECTOR, "p")[-2]
                interests = expertise_tag.get_attribute("innerText")

                if any(keyword.lower() in interests.lower() for keyword in keyword_list):
                    fields.append([unviersty_name, country, name, email, profile_link])

        except:
            pass
    driver.quit()

    # if fields:
    #     df = pd.DataFrame(fields)
    #     df.to_csv("vermont.csv", index=False)
    #     print("Data extracted successfully")
    print("Vermont data extracted successfully")
    return fields




if __name__ == "__main__":
    vermont()