import requests
from bs4 import BeautifulSoup
import csv

# Keywords to filter faculty members
KEYWORDS = [
    "embedded systems", "operating systems", "computer science education",
    "eye tracking", "accessibility", "digital watermarking", 
    "chaos theory", "mobile application development", "image processing"
]

# Function to get the profile URLs of faculty members
def get_faculty_profile_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Print the raw HTML to debug the page structure
    print(soup.prettify())  # This will print the HTML content for debugging

    profile_links = []
    faculty_blocks = soup.find_all("div", class_="views-row")  # Adjust this as needed for the actual class

    for block in faculty_blocks:
        link_tag = block.find("h3", class_="views-field-title").find("a")
        if link_tag:
            profile_url = link_tag['href']
            # Make sure the URL is fully qualified
            if not profile_url.startswith("http"):
                profile_url = "https://www.maynoothuniversity.ie" + profile_url
            profile_links.append(profile_url)
    
    print(f"Found {len(profile_links)} profile links.")
    return profile_links

# Function to extract faculty details from their profile
def get_faculty_data(profile_url):
    response = requests.get(profile_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract Name
    name_tag = soup.find("h1", class_="page-title")
    name = name_tag.text.strip() if name_tag else "Not available"

    # Extract Email
    email_tag = soup.find("a", href=lambda href: href and "mailto:" in href)
    email = email_tag.text.strip() if email_tag else "Not available"
    
    # Extract Research Interests (if available)
    research_section = soup.find("div", class_="field-name-field-research-interests")
    research_areas = (
        research_section.get_text(strip=True) if research_section else "Not available"
    )

    print(f"Extracted data for {name}.")
    return name, email, research_areas

# Function to filter faculty members based on keywords
def filter_faculty_by_keywords(faculty_data):
    filtered_faculty = []
    for name, email, research_areas, profile_url in faculty_data:
        if any(keyword.lower() in research_areas.lower() for keyword in KEYWORDS):
            filtered_faculty.append({
                "Name": name,
                "Email": email,
                "Research Areas": research_areas,
                "Profile URL": profile_url
            })
    print(f"Filtered {len(filtered_faculty)} faculty members based on keywords.")
    return filtered_faculty

# Main function to scrape the faculty information
def scrape_faculty_data(base_url):
    faculty_data = []
    profile_links = get_faculty_profile_links(base_url)
    
    for profile_url in profile_links:
        name, email, research_areas = get_faculty_data(profile_url)
        faculty_data.append((name, email, research_areas, profile_url))

    # Filter faculty based on keywords
    filtered_faculty_data = filter_faculty_by_keywords(faculty_data)
    
    return filtered_faculty_data

# Save data to CSV
def save_to_csv(data, filename):
    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["Name", "Email", "Research Areas", "Profile URL"])
            writer.writeheader()
            writer.writerows(data)
        print(f"Scraped data saved to {filename}")
    except PermissionError as e:
        print(f"Permission error: {e}. Please close the file if it is open elsewhere or check the directory permissions.")

# URL to the faculty listing page
base_url = "https://www.maynoothuniversity.ie/computer-science/our-people"
faculty_data = scrape_faculty_data(base_url)

# Save filtered data to CSV
output_file = "maynooth_faculty.csv"
save_to_csv(faculty_data, output_file)
