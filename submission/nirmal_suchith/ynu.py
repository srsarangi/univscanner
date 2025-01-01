import requests
import csv
import re
from bs4 import BeautifulSoup


def extract_ynu_faculty():
    base_url = "https://cse.ynu.ac.jp/staff.html"  # Main faculty page
    university_name = "Yokohama National University"
    country = "Japan"

    # Keywords to search in research interests
    keyword_list = [
        'embedded systems', 'Embedded System', 'embedded software', 'hardware systems',
        'system architecture', 'IoT', 'real-time systems',
        'operating systems', 'Operating System', 'OS', 'system programming', 'system software',
        'distributed systems', 'kernel', 'cryptography', 'information security',
        'theoretical computer science', 'information theory'
    ]

    # File setup
    filename_txt = "ynu_faculty.txt"
    filename_csv = "ynu_faculty.csv"

    with open(filename_txt, "w", encoding="utf-8") as f_txt, open(filename_csv, "w", newline='', encoding="utf-8") as f_csv:
        csv_writer = csv.writer(f_csv)
        csv_writer.writerow(["University", "Country", "Name", "Email", "Website Link"])  # CSV header

        # Get the faculty list page
        response = requests.get(base_url)
        soup = BeautifulSoup(response.text, "html.parser")

        # Locate all faculty sections
        faculty_sections = soup.find_all("div", class_="row mb-5")
        print( faculty_sections)

        for section in faculty_sections:
            try:
                # Extract name
                name = section.find("h4").get_text(strip=True)

                # Extract profile link
                profile_link_tag = section.find("a", href=True, string=re.compile("Researcher Directory"))
                profile_link = profile_link_tag["href"] if profile_link_tag else "Not Found"

                # Extract homepage link
                homepage_link_tag = section.find("a", href=True, string=re.compile("Laboratory Websites"))
                homepage_link = homepage_link_tag["href"] if homepage_link_tag else "Not Found"

                # Visit profile page to extract more details
                if profile_link != "Not Found":
                    profile_response = requests.get(profile_link)
                    profile_soup = BeautifulSoup(profile_response.text, "html.parser")

                    # Extract email address
                    email_img = profile_soup.find("img", alt="email address")
                    email = "Not Found"
                    if email_img:
                        email = f"{profile_link.rsplit('/', 1)[0]}/{email_img['src']}"

                    # Extract research keywords
                    research_keywords_tag = profile_soup.find("td", string=re.compile("Research Keywords"))
                    research_keywords = research_keywords_tag.find_next_sibling("td").get_text(strip=True) if research_keywords_tag else ""

                    # Check if keywords match
                    if any(re.search(keyword, research_keywords, re.IGNORECASE) for keyword in keyword_list):
                        # Write to files
                        f_txt.write(
                            f"Name: {name}\nEmail: {email}\nUniversity: {university_name}\nWebsite: {homepage_link}\n\n"
                        )
                        csv_writer.writerow([university_name, country, name, email, homepage_link])

            except Exception as e:
                print(f"Error processing a faculty section: {e}")

    print("Data extraction complete.")


if __name__ == "__main__":
    extract_ynu_faculty()
