from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
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
        
        description_elements = wait.until(
            EC.presence_of_all_elements_located((
                By.CSS_SELECTOR, 
                "span.yt-core-attributed-string--link-inherit-color"
            ))
        )
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

def send_email_notification(url, timestamps):
    """
    Send email using SendGrid after file save
    """
    # SendGrid credentials
    SENDGRID_API_KEY = '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'
    FROM_EMAIL = 'muraliju981@gmail.com'
    TO_EMAIL = 'josephstalin981@gmail.com' 

    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=TO_EMAIL,
        subject='YouTube Video Information',
        plain_text_content=f"URL: {url}\nTimestamps: {', '.join(timestamps)}"
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        if response.status_code == 202:
            print("Email sent successfully!")
        else:
            print(f"Error sending email. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending email: {str(e)}")

def save_to_file(url, timestamps, filename="youtube_info.txt"):
    """
    Task 3: Store url and timestamps in text file, then send email
    """
    try:
        # Save to file
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(f"URL: {url}\n")
            file.write(f"Timestamps: {', '.join(timestamps)}")
        print(f"\nTask 3 - Data saved to {filename}")
        
        # After successful file save, send email
        print("\nTask 4 - Sending email notification...")
        send_email_notification(url, timestamps)
        
    except Exception as e:
        print(f"Error in save_to_file: {str(e)}")

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
    
    # Task 3 & 4: Save to file and send email
    save_to_file(url, timestamps)

if __name__ == "__main__":
    main()