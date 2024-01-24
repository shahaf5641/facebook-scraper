import os
import pandas as pd
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
import time
 
def Get_FB_Group_Links():
    print(f"Collecting group links...")
    driver.get('https://www.facebook.com/groups/search/groups/?q=' + search_word)
    # Toggle the public groups
    public_group_button = driver.find_element(By.XPATH, "//input[@role='switch' and @class='x1i10hfl x9f619 xggy1nq x1s07b3s x1ypdohk x5yr21d xdj266r x11i5rnm xat24cr x1mh8g0r x1w3u9th x1a2a7pz xexx8yu x4uap5 x18d9i69 xkhd6sd x10l6tqk x17qophe x13vifvy xh8yej3']")
    public_group_button.click()
    # Find all anchor elements that are links to Facebook groups
    group_elements = driver.find_elements(By.XPATH, "//a[contains(@href, '/groups/') and @class='x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz xt0b8zv xzsf02u x1s688f']")

    while len(group_elements) <= group_links_number:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        group_elements = driver.find_elements(By.XPATH, "//a[contains(@href, '/groups/') and @class='x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz xt0b8zv xzsf02u x1s688f']")


    # Initialize an empty list to store the URLs
    group_links = []
 
    # Creating a list of group links
    for i in range(group_links_number):
        # Extract the href attribute (URL) from the anchor element and append it to the list
        group_links.append(group_elements[i].get_attribute("href"))
    
    return group_links

def ScrapeGroupDetails(group_link, content_list, name_list, post_links,post_times, posts_number_requested, groupnum):
    driver.get(group_link)
    print(f"Group: {groupnum}/{group_links_number}")
    postsnum=posts_number_requested
    # Reached the number of requested posts
    posts=[]
    i = 0
    # Extracting information from each post
    while posts_number_requested > 0:
        #Checks if we reached to the last post we have in the list, if yes, get more posts to the list
        if i==len(posts):
            while i+postsnum>len(posts):
                #Checking if we at same place
                start_position = driver.execute_script("return window.pageYOffset;")
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                current_position = driver.execute_script("return window.pageYOffset;")
                if current_position <= start_position:
                    return posts_number_requested
                try:
                    posts = WebDriverWait(driver, 5).until(
                        EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z')]")))
                    see_more_buttons = WebDriverWait(driver, 5).until(
                        EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'x1i10hfl xjbqb8w') and contains(., 'ראה עוד')]")))
                    for button in see_more_buttons:
                        ActionChains(driver).click(button).perform()
                except:
                    pass
            soup = BeautifulSoup(driver.page_source, "html.parser")
            all_posts = soup.find_all("div", {"class": "x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z"})
        #Extracting mame
        try:
            name = all_posts[i].find("a", {
                "class": "x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz xt0b8zv xzsf02u x1s688f"}).get_text(strip=True)
        except:
            name = ""

        # Extracting content
        try:
            content = all_posts[i].find("span", {
                "class": "x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xzsf02u x1yc453h"}).get_text(strip=True)

        except:
            content = ""

        # Extracting post link and time
        try:
            element = all_posts[i].find("a", {
                "class": "x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g xt0b8zv xo1l8bm"})
            link = element.get("href")
            post_time = element.get_text(strip=True)

        except:
            link=""
            post_time=""

        #NEED TO DO VIDEO
        try:
            video = all_posts[i].find("div", {
            "class": "x1ey2m1c x10l6tqk x1d8287x x6o7n8i xl405pv xh8yej3 x11uqc5h x6s0dn4 xzt5al7 x78zum5 x1q0g3np"})
        except:
            video= None
        if content != "" and name != "" and content not in content_list and video==None:
            content_list.append(content)
            name_list.append(name)
            post_links.append(link)
            post_times.append(post_time)
            posts_number_requested -= 1
            print(f"Posts: {len(content_list)}/{table_size}")
        i += 1
    return posts_number_requested


#Opens and access the environment variables
load_dotenv()
facebook_username = os.environ.get("FACEBOOK_USERNAME")
facebook_password = os.environ.get("FACEBOOK_PASSWORD")
group_links_number = int(os.environ.get("GROUP_LINKS_NUMBER"))
posts_from_each_group = int(os.environ.get("POSTS_FROM_EACH_GROUP"))
search_word = os.environ.get("SEARCH_WORD")
table_size=group_links_number*posts_from_each_group


# Set up ChromeOptions to disable notifications
chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--disable-usb-keyboard-detect')
chrome_options.add_argument("--disable-notifications")
 
# Set up the Selenium WebDriver with ChromeOptions
driver = webdriver.Chrome(options=chrome_options)
 
# Ensure that you are already logged into Facebook before running the script
driver.get("https://www.facebook.com")
driver.maximize_window()

print(f"Starting the program...")
# Enter the login details
email_input = driver.find_element(By.ID, 'email')
password_input = driver.find_element(By.ID, 'pass')
 
email_input.send_keys(facebook_username)
password_input.send_keys(facebook_password)
 
# Click the login button
password_input.send_keys(Keys.ENTER)

#Checks if we at home page

try:
    # Wait for up to 5 seconds for the presence of the Facebook logo 
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, ":Rqir3aj9emhpapd5aq:"))
    )
except Exception as e:
    print(f"Low internet connection {e}")
    # Search for car-related groups

print(f"Logged in succesfuly")
#We at home page

#Getting links
car_group_links=Get_FB_Group_Links()

#Lists to store information
content_list, name_list, post_links,post_times = [], [], [], []
posts_not_added=0
print("Starting to process groups...")
#Getting posts information from each group
for j in range(group_links_number):
    res = ScrapeGroupDetails(car_group_links[j], content_list, name_list, post_links, post_times,posts_from_each_group, j+1)
    if res==0:
        print(f"Group number {j+1} has finished succesfuly\n")
    else:
        posts_not_added+=res
        print(f"Group number {j+1} has no enough posts\n")

#Creating a table - csv file
table=pd.DataFrame({"שם":name_list,"תוכן הפוסט":content_list,"לינק לפוסט":post_links,"זמן":post_times})
table.reset_index(drop=True, inplace=True)
table.to_csv("facebookposts.csv", index=False)
print(f"Finised.\nTable size:{table_size-posts_not_added}")


# Close the WebDriver
driver.quit