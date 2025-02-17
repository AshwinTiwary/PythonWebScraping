from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time

# Configuring the chromium 👇
# Setup Selenium
options = Options()
ua = UserAgent()
options.add_argument(f"user-agent={ua.random}") 
options.add_argument("--headless")  # Uncomment to run in headless mode
options.add_argument("--disable-gpu") 
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Open the homepage
home_url = "https://flippa.com/"  # Enter website url in here
driver.get(home_url) # Setting the driver to open the home page

# Waiting for the page to load using WebDriverWait
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "a")))  # Waiting until <a> tags are loaded

# Find all navbar links from homepage
try:
    nav_links = driver.find_elements(By.TAG_NAME, "a")  # Find all <a> tags for navigating purpose

    visited_links = set() # Container to store the previously visited <a> tag and to prevent from visiting again
    hrefs = [link.get_attribute("href") for link in nav_links if link.get_attribute("href")] # Fetching the actual link from <a> tag

    for link in hrefs:
        print("👀 Looking into : ", link)
        href = link
        
        if href and href.startswith(home_url) and href not in visited_links: # check if if the link is correct and not visited
            print("🔍 Scraping into : ", href)
            visited_links.add(href)  # Store visited links to prevent from repeated visiting
            try:
                driver.get(href)  # Make driver visit the new link
                
                # Waiting for the page content to load
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

                # Get page content
                html = driver.page_source
                soup = BeautifulSoup(html, "html.parser") 

                # Extract text from relevant tags ( Have to make it dynamic )
                tags = soup.find_all(["p", "span", "h1", "h2", "h3", "h4", "h5", "h6"])
                for tag in tags:
                    print(f"👉 {tag.name.upper()}: {tag.get_text(strip=True)}")

            except Exception as e:
                print(f"🔒 Error navigating to {href}: {e}")

            time.sleep(3)

except Exception as e:
    print(f"🔒 Error in Router: {e}")

finally:
    driver.quit()  # Closing the browser
