from urllib import request
import bs4
import uuid

# Function to get the HTML content from the webpage
def get_webpage_content(url):
    response = request.urlopen(url)
    html_content = response.read()
    return html_content

content = get_webpage_content("https://www.qdesq.com/")

# Parse the HTML content with BeautifulSoup
soup = bs4.BeautifulSoup(content, 'html.parser')

# Find all the links on the webpage
links = soup.find_all('a')

# Save the links to a file in CSV format
scrapable_links = []
with open("links.csv", "w", encoding="utf-8") as file:
    file.write("Links\n")
    for link in links:
        li = link.get('href')
        if li and li.startswith("https://www.qdesq.com/"):
            file.write(f"{li}\n")
            scrapable_links.append(li)

# Scrape all the links and save to a file in CSV format
with open(f"scraped_data{uuid.uuid4()}.csv", "w", encoding="utf-8") as file:
    file.write("Link,Name,Location,Price\n")
    for base_link in scrapable_links:
        print(f"Scraping {base_link}...")
        page_number = 1

        if "co-living" not in link and "brand" not in link:
            while True:
                # Append page number to the URL
                link = f"{base_link}?page={page_number}"
                
                # Skip links that do not contain certain keywords
                content = get_webpage_content(link)
                
                # Parse the HTML content with BeautifulSoup
                soup = bs4.BeautifulSoup(content, 'html.parser')
                
                # Determine the target class based on the link content
                target = 'space_card'
                if 'virtual' in link:
                    target = 'card_box'
                # Find all spaces on the page
                spaces = soup.find_all('div', class_=target)
                
                # Break the loop if no spaces are found
                if not spaces:
                    break
                # Process each space found on the page
                for space in spaces:
                    # Extract name, location, and price
                    name_text = ""
                    location_text = ""
                    price_text = ""
                    
                    title_container = space.find('div', class_='space_title')
                    if title_container:
                        name = title_container.find('h4')
                        if name:
                            name_text = name.text.strip().replace(',', '')
                    location = space.find('p', class_="address")
                    if location:
                        location_text = location.text.strip().replace(',', ' -')
                    price = space.find('div', class_='price')
                    if price:
                        price_text = price.text.strip().replace(',', '').replace('₹', '')
                    
                    # Write data to CSV
                    file.write(f"{link}, {name_text}, {location_text}, {price_text}\n")

                # Increment page number for the next iteration
                page_number += 1
        else:
            continue
