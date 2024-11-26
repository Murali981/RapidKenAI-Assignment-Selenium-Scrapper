from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import re

def get_youtube_info(url):
    # Configure Chrome options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')  # Set a specific window size
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36')
    
    driver = None
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        
        # Create WebDriverWait object
        wait = WebDriverWait(driver, 20)  # Increased timeout to 20 seconds
        
        print("Page loaded, looking for elements...")
        
        try:
            # First try to get initial description text
            description_container = wait.until(
                EC.presence_of_element_located((By.ID, "description-inline-expander"))
            )
            print("Found description container...")
            
            # Try to find the expand button
            expand_button = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "tp-yt-paper-button#expand"))
            )
            
            # Try to click using different methods
            try:
                print("Attempting to click expand button...")
                driver.execute_script("arguments[0].scrollIntoView(true);", expand_button)
                time.sleep(2)
                driver.execute_script("arguments[0].click();", expand_button)
            except Exception as click_error:
                print(f"Click error: {click_error}")
            
            time.sleep(3)  # Wait for expansion
            
            # Get the description text after expansion
            try:
                description = wait.until(
                    EC.presence_of_element_located((
                        By.CSS_SELECTOR, 
                        "ytd-text-inline-expander[id='description-inline-expander']"
                    ))
                ).text
                
                print(f"Description length: {len(description)}")
                
                # Extract timestamps using regex
                timestamps = re.findall(r'\b\d{2}:\d{2}\b', description)
                print(f"Found {len(timestamps)} timestamps")
                
                return description, timestamps
                
            except Exception as text_error:
                print(f"Error getting text: {text_error}")
                return None, []
                
        except TimeoutException:
            print("Timeout waiting for elements")
            return None, []
            
    except Exception as e:
        print(f"Main error: {str(e)}")
        return None, []
        
    finally:
        if driver:
            driver.quit()

def save_to_file(url, timestamps, filename="youtube_info.txt"):
    try:
        with open(filename, 'w') as f:
            f.write(f"URL: {url}\n")
            f.write(f"Timestamps: {', '.join(timestamps)}")
        print(f"Information saved to {filename}")
    except Exception as e:
        print(f"Error saving to file: {str(e)}")

def main():
    url = "https://youtu.be/iTmlw3vQPSs"
    
    print("Starting YouTube scraping...")
    description, timestamps = get_youtube_info(url)
    
    if description:
        print("\nDescription:")
        print(description)
        print("\nTimestamps found:")
        print(timestamps)
        
        save_to_file(url, timestamps)
    else:
        print("Failed to retrieve information")

if __name__ == "__main__":
    main()