# from selenium import webdriver
# from selenium.common import exceptions
# import sys
# import time




# # function that is actually scrapping the details from the youtube video

# def scrape(url):
#     driver = webdriver.Chrome()

#     driver.get(url)  # open the url automatically

#     driver.maximize_window()

#     time.sleep(5)

   
#     title = driver.find_element_by_xpath( 
#             # Every element inside the webpage has it's own X-Path , selector and all the stuff
#            '//*[@id="title"]/h1/yt-formatted-string'
#         ).text # To get the text that is present inside this tag (or) element
#     print("Title of the video is" + title)

   

        


# if __name__ == "__main__":
#     scrape(sys.argv[1])


from selenium import webdriver
# from grpc import Channel
from selenium.webdriver.common.by import By
import sys
import time
import csv
import io
# import panda as pd


# function that scrapes the details from the YouTube video
def scrape(url):
    driver = webdriver.Chrome()  # Automatically finds ChromeDriver in PATH
    driver.get(url)  # Open the URL
    driver.maximize_window()
    time.sleep(5)  # Wait for the page to load completely

    # Update this with the new syntax for locating elements
    title = driver.find_element(By.XPATH, 
            '//*[@id="title"]/h1/yt-formatted-string').text  # Locate and extract the video title
    
    views = driver.find_element(By.XPATH,'//*[@id="info"]/span[1]').text

    driver.find_element(By.ID,'description-inline-expander').click()

    description = driver.find_element(By.CSS_SELECTOR, '#description-inline-expander .ytd-text-inline-expander span') .text

    print("Title of the video is: " + title)
    print("Views of the video is: " + views)
    print("Description of the video is: " + description)

    # Write the data to a CSV file (or) save this data into a csv file
    with io.open("scrapped_data.csv", "w", newline="", encoding="utf-16") as file:

        writer = csv.writer(file,delimiter = ",",quoting=csv.QUOTE_ALL)

        writer.writerow(["Title","Views"])

        writer.writerow([title,views])

    driver.quit()  # Close the browser when done


if __name__ == "__main__":
    scrape(sys.argv[1])

