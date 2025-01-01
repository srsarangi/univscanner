import requests
import csv
from bs4 import BeautifulSoup

def wvu_faculty_scraper():
    url = "https://directory.statler.wvu.edu/faculty-directory"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    
    # Output files
    text_filename = "wvu_faculty.txt"
    csv_filename = "wvu_faculty.csv"
    
    # Open files for writing
    with open(text_filename, "w", encoding="utf-8") as txt_file, \
         open(csv_filename, "w", newline='', encoding="utf-8") as csv_file:
        
        csvwriter = csv.writer(csv_file)
        csvwriter.writerow(["University", "Country", "Professor Name", "Email", "Website Link"])
        
        university_name = "West Virginia University"
        country = "USA"
        
        # Extract faculty sections
        faculty_sections = soup.find_all("div", class_="person animated animatedFadeInUp InViewport")
        
        
        for faculty in faculty_sections:
            # Extract professor's name
            name_tag = faculty.find("p", class_="profile-name").find("a")
            print( "niirmal"+name_tag)
            name = name_tag.get_text(strip=True) if name_tag else "Not Found"
            
            # Extract email
            email_tag = faculty.find("a", class_="profile-email")
            email = email_tag.get("href", "").replace("mailto:", "").strip() if email_tag else "Not Found"
            
            # Extract website link
            website_tag = faculty.find("p", class_="profile-name").find("a")
            website_link = "https://directory.statler.wvu.edu" + website_tag.get("href", "").strip() if website_tag else "Not Found"
            
            # Extract research area
            research_tag = faculty.find("p", class_="profile-expertise")
            research_area = research_tag.get_text(strip=True) if research_tag else "Not Found"
            
            # Debug output
            print(f"Name: {name}, Email: {email}, Website: {website_link}, Research: {research_area}")
            
            # Write data to text and CSV files
            txt_file.write(f"Name: {name}\nEmail: {email}\nUniversity: {university_name}\nWebsite: {website_link}\nResearch: {research_area}\n\n")
            csvwriter.writerow([university_name, country, name, email, website_link])
    
    print("Data extraction completed.")

if __name__ == "__main__":
    wvu_faculty_scraper()
