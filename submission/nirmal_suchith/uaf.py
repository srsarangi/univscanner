import requests
import csv
import re
from bs4 import BeautifulSoup

def uaf():
    url = "https://www.uaf.edu/cem/people/cs.php"  # Faculty page URL
    r = requests.get(url)  # Send GET request to the page
    
    # Check the status code and the content of the page
    if r.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {r.status_code}")
        return
    
    # Print the first 500 characters of the page to check if it's being fetched correctly
    print(r.text[:500])  # You can remove this print statement after debugging
    
    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(r.text, "html.parser")
    
    # File setup for output
    filename = "uaf_faculty.txt"
    f = open(filename, "w")
    
    excel_filename = "uaf_faculty.csv"
    f2 = open(excel_filename, "w", newline='', encoding="utf-8")
    csvwriter = csv.writer(f2)
    
    # Set the university name and country
    u_name = "University of Alaska Fairbanks"
    country = "USA"
    
    # Expanded research keywords for embedded systems and operating systems
    keyword_list = [
        'embedded systems', 'Embedded System', 'embedded software', 'hardware systems',
        'system architecture', 'IoT', 'real-time systems',
        'operating systems', 'Operating System', 'OS', 'system programming', 'system software',
        'distributed systems', 'kernel'
    ]

    # Extracting all professor profiles
    faculty_profiles = soup.find_all('div', class_='ou-component-person-profile')
    
    # Debugging: Print how many profiles were found
    print(f"Found {len(faculty_profiles)} faculty profiles.")
    
    for profile in faculty_profiles:
        # Extracting name
        name_tag = profile.find('p', class_='h4 mb-2')
        name = name_tag.get_text(strip=True) if name_tag else "Not Found"
        
        # Extracting email
        email_tag = profile.find('a', href=re.compile('mailto:'))
        email = email_tag.get_text(strip=True) if email_tag else "Not Found"
        
        # Extracting research interests
        research_tag = profile.find('p', class_='card-text')
        research_interests = research_tag.get_text(strip=True) if research_tag else ""
        
        # Debugging: Print the extracted research interests
        print(f"Research interests for {name}: {research_interests}")
        
        # Check if any research interest matches our criteria
        flag = False
        for keyword in keyword_list:
            if re.search(keyword, research_interests, re.IGNORECASE):
                flag = True
                break
        
        # If keyword matches, write to files
        if flag:
            f.write(f"Name: {name}\nEmail: {email}\nUniversity: {u_name}\n\n")
            csvwriter.writerow([u_name, country, name, email])
    
    f.close()
    f2.close()
    print("Data extraction complete")

if __name__ == '__main__':
    uaf()
