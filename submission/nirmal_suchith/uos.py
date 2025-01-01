import requests
import csv
from bs4 import BeautifulSoup

def uos_ac_kr():
    url = "https://www.uos.ac.kr/en/professor/list.do?code=20020#"
    r = requests.get(url)  # Send GET request to the page
    
    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(r.text, "html.parser")
    
    # File setup for output
    filename = "uos_ac_kr_faculty.txt"
    f = open(filename, "w", encoding="utf-8")
    
    excel_filename = "uos_ac_kr_faculty.csv"
    f2 = open(excel_filename, "w", newline='', encoding="utf-8")
    csvwriter = csv.writer(f2)
    
    # Write headers to CSV
    csvwriter.writerow(["Name", "Email", "Research", "Website Link", "University", "Country"])
    
    # Set the university name and country
    u_name = "University of Seoul"
    country = "South Korea"
    
    # Research keywords for embedded systems or operating systems
    keyword_list = [
        'embedded systems', 'Embedded System', 'embedded software', 'hardware systems',
        'system architecture', 'IoT', 'real-time systems',
        'operating systems', 'Operating System', 'OS', 'system programming', 'system software',
        'distributed systems', 'kernel'
    ]
    
    # Find all faculty members listed under the section with the class "profile-queue list"
    faculty_sections = soup.find_all("div", class_="person animated animatedFadeInUp InViewport")
    print(faculty_sections)
    
    for section in faculty_sections:
        # Extracting the name
        name_tag = section.find("p", class_="profile-name").find("a")
        name = name_tag.get_text(strip=True) if name_tag else "N/A"
        
        # Extracting the email
        email_tag = section.find("a", class_="profile-email")
        email = email_tag.get_text(strip=True) if email_tag else "N/A"
        
        # Extracting the research information
        research_tag = section.find("p", class_="profile-expertise")
        research = research_tag.get_text(strip=True) if research_tag else "N/A"
        
        # Extracting the website link
        website_link_tag = section.find("p", class_="profile-name").find("a")
        website_link = "https://www.uos.ac.kr" + website_link_tag['href'] if website_link_tag else "N/A"
        
        # Check if research matches any of the keywords
        if any(keyword.lower() in research.lower() for keyword in keyword_list):
            # Write to text file
            f.write(f"Name: {name}\nEmail: {email}\nResearch: {research}\nWebsite: {website_link}\n\n")
            
            # Write to CSV
            csvwriter.writerow([name, email, research, website_link, u_name, country])
    
    # Close files
    f.close()
    f2.close()
    
# Call the function to scrape the data
uos_ac_kr()
