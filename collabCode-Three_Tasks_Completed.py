from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

def get_youtube_description(url):
    """
    Task 1: Retrieve the description text from YouTube video using Selenium
    """
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36')
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        wait = WebDriverWait(driver, 20)

          # Click expand button
        expand_button = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "tp-yt-paper-button#expand"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", expand_button)
        time.sleep(2)
        driver.execute_script("arguments[0].click();", expand_button)
        time.sleep(2)
        
        # Get all spans containing description and timestamps
        description_elements = wait.until(
            EC.presence_of_all_elements_located((
                By.CSS_SELECTOR, 
                "span.yt-core-attributed-string--link-inherit-color"
            ))
        )
        
        # Combine text from all elements
        description = " ".join(element.text for element in description_elements)
        return description
        
    finally:
        if driver:
            driver.quit()

def extract_timestamps(description):
    """
    Task 2: Extract timestamps (mm:ss format) from description and save in list
    """
    if description:
        timestamps = re.findall(r'\b\d{2}:\d{2}\b', description)
        return timestamps
    return []

def save_to_file(url, timestamps, filename="youtube_info.txt"):

    """
    Task 3: Store url and timestamps in text file
    """
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(f"URL: {url}\n")
            file.write(f"Timestamps: {', '.join(timestamps)}")
        print(f"\nTask 3 - Data saved to {filename}")
        # For Colab: Display where the file is saved
        # print("File location in Colab:", !pwd)
    except:
        print(f"Error saving to file")

def main():
    url = "https://youtu.be/iTmlw3vQPSs"
    
    # Task 1: Get video description
    print("\nTask 1 - Getting Description:")
    description = get_youtube_description(url)
    print(description)
    
    # Task 2: Extract timestamps
    print("\nTask 2 - Extracting Timestamps:")
    timestamps = extract_timestamps(description)
    print(timestamps)
    
    # Task 3: Save to file
    save_to_file(url, timestamps)

if __name__ == "__main__":
    main()