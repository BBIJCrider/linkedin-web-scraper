import time
from urllib.parse import urlparse
from selenium import webdriver
from bs4 import BeautifulSoup

browser = webdriver.Chrome('driver/chromedriver.exe')
browser.get('https://www.linkedin.com/uas/login')

file = open('config.txt')
lines = file.readlines()
username = lines[0]
password = lines[1]

elementID = browser.find_element_by_id('username')
elementID.send_keys(username)

elementID = browser.find_element_by_id('password')
elementID.send_keys(password)

elementID.submit()

link = 'https://www.linkedin.com/in/jacob-crider/'
browser.get(link)

SCROLL_PAUSE_TIME = 5

# Get scroll height
last_height = browser.execute_script("return document.body.scrollHeight")

for i in range(3):
    # Scroll down to bottom
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)
    # Calculate new scroll height and compare with last scroll height
    new_height = browser.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

src = browser.page_source
# Set soup object to BeautifulSoup object (html of src page)
soup = BeautifulSoup(src, 'lxml')

name = soup.find(
    'h1', {'class': 'text-heading-xlarge inline t-24 v-align-middle break-words'}).text
page_title = soup.find('div', {'class': 'text-body-medium break-words'}).text
loc = soup.find(
    'span', {'class': 'text-body-small inline t-black--light break-words'}).text

experience_list = soup.find_all('ul', {'class': 'pvs-list ph5 display-flex flex-row flex-wrap'})[3]

recent_experience = experience_list.find_all('span', {'class': 'visually-hidden'})[1].text
job_title = experience_list.find_all('span', {'class': 'visually-hidden'})[0].text

info = [link, name, page_title, loc, recent_experience, job_title]

print(info)