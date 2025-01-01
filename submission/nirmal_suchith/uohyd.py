import requests
import csv
import re
from bs4 import BeautifulSoup

def uohyd():
    url = "https://scis.uohyd.ac.in/faculty_scis.php"  # Faculty page URL
    r = requests.get(url)  # Send GET request to the page
    
    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(r.text, "html.parser")
    
    # File setup for output
    filename = "uohyd_faculty.txt"
    f = open(filename, "w")
    
    excel_filename = "uohyd_faculty.csv"
    f2 = open(excel_filename, "w", newline='', encoding="utf-8")
    csvwriter = csv.writer(f2)
    
    # Set the university name and country
    u_name = "University of Hyderabad"
    country = "India"
    
    # Research keywords for embedded systems or operating systems
    keyword_list = [
        'embedded systems', 'Embedded System', 'embedded software', 'hardware systems',
        'system architecture', 'IoT', 'real-time systems',
        'operating systems', 'Operating System', 'OS', 'system programming', 'system software',
        'distributed systems', 'kernel'
    ]
    
    # Extract faculty rows
    faculty_rows = soup.find_all('tr', class_='td_faculty')

    # Loop through faculty rows to extract information
    for i in range(0, len(faculty_rows), 2):  # Every two rows represent a faculty member
        name_tag = faculty_rows[i].find('b')
        name = name_tag.get_text(strip=True) if name_tag else "Not Found"
        
        # Extracting the email from the next row
        email = "Not Found"
        email_tag = faculty_rows[i+1].find('font', color='F14E23')
        
        if email_tag:
            email = email_tag.get_text(strip=True)
        
        # Extracting the research interests after "Areas of Interest:"
        research_interests = ""
        areas_tag = faculty_rows[i+1].find('b', string=re.compile(r'Areas of Interest'))
        
        if areas_tag:
            # Extract everything after "Areas of Interest"
            research_interests_tag = areas_tag.find_next('font')
            if research_interests_tag:
                research_interests = research_interests_tag.get_text(strip=True)
        
        # Debugging output for the extracted values
        print(f"Name: {name}, Email: {email}, Research Interests: {research_interests}")
        
        # Check if any research interest matches our criteria
        flag = False
        for keyword in keyword_list:
            if re.search(keyword, research_interests, re.IGNORECASE):
                flag = True
                break
        
        # If keyword matches, write to output files
        if flag:
            f.write(f"Name: {name}\nEmail: {email}\nUniversity: {u_name}\nResearch Interests: {research_interests}\n\n")
            csvwriter.writerow([u_name, country, name, email, research_interests])
    
    # Close the output files
    f.close()
    f2.close()
    print("Data extraction complete")

if __name__ == '__main__':
    uohyd()
