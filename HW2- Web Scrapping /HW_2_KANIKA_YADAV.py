#!/usr/bin/env python
# coding: utf-8

# <h1><center>HW2: Scrape Hotel Reviews</center></h1>

# <div class="alert alert-block alert-warning">Each assignment needs to be completed independently. Never ever copy others' work (even with minor modification, e.g. changing variable names). Anti-Plagiarism software will be used to check all submissions. </div>

# Choose one hotel at tripadvisor.com (e.g.https://www.tripadvisor.com/Hotel_Review-g60763-d23448880-Reviews-Motto_by_Hilton_New_York_City_Chelsea-New_York_City_New_York.html) to scrape reviews

# ## Q1. Scrape the first page
# 
# Write a function `getReviews(page_url, driver)` to scrape all **reviews on the first page**, which
# - accepts two input parameters:
#     - `page_url` is the URL to be scraped
#     - `driver` is the selenium web driver object initiated. Firefox, Chrome, or any web driver is acceptable.
# - locates all the reviews on this page, and for each review, scrape the following 
#     - `username` (see (1) in Figure)
#     - `helpful votes` (see (2) in Figure)
#     - `rating` (see (3) in Figure)
#     - `title` (see (4) in Figure)
#     - `review` (see (5) in Figure. You can just scrape the truncated text. You don't have to expand it.
#     - `date of stay` (see (6) in Figure)
# - if a field, e.g., rating, is missing, uses `None` to indicate it. 
# - collects all reviews as a DataFrame and each field as a column
# - returns the dataframe

# ## Q2 (bonus): Scrape full text in more reviews
# 
# Modify the function you defined in Q1 as `getReviews(page_url, driver, expand_review = False, limit = 10)` as follows:
# - If `expand_review = True`, click the "read_more" button (see (7) in Figure) of each review and collect the full text.
# - Collect the required number of reviews as specified by `limit`. For example, if `limit=50`, you'll need to collect at least 50 reviews. This requires you to keep clicking the `next` button (see (8) in Figure), if clickable, until the required number of reviews are collected.
# - Return a dataframe as specified in Q1.

# ![alt text](tripadvisor.png "TripAdvisor")

# ## Solution

# In[4]:


import requests
from bs4 import BeautifulSoup  
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re


# ### Q1

# In[3]:


#pip install webdriver-manager


# In[5]:


from webdriver_manager.chrome import ChromeDriverManager 
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service as ChromeService

browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install())) 
browser.implicitly_wait(5)


# In[88]:


def getReviews(page_url, driver):
    
    # add your code here
    driver.get(page_url)

    # now get the page content dynamically generated
    page = driver.page_source
    

    # parse the content by beautifulsoup 
    soup = BeautifulSoup(page, 'html.parser')
    #time.sleep(3)
    reviews_list = soup.select("body div[data-test-target=HR_CC_CARD]")
    rows =[]
    for review in reviews_list:
        reviewer = review.find(class_="ui_header_link")
        username = reviewer.get_text()

        vote = review.select("div[class=MziKN] span[class=phMBo]")
        #print(vote, len(vote))
        v = vote[1].get_text() if len(vote)==2 else None

        ratings = review.select("div[data-test-target=review-rating]")
        rating = ratings[0].span['class'][1]

        reviewtitle = review.select("div[data-test-target=review-title]")
        title = reviewtitle[0].getText()

        
        desc = review.find(class_="QewHA")
        de = desc.getText()

        dates =soup.find(class_="teHYY")
        date = dates.getText()

        rows.append((username, rating, v,  title,de, date))
        
    result =  pd.DataFrame(rows, columns =['reviewer','rating','vote','title','text','date'])
    
    return result


# In[89]:


page_url = "https://www.tripadvisor.com/Hotel_Review-g60763-d23448880-Reviews-or10-Motto_by_Hilton_New_York_City_Chelsea-New_York_City_New_York.html#REVIEWS"

#executable_path = '../driver/chromedriver'

from webdriver_manager.chrome import ChromeDriverManager 
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service as ChromeService

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install())) 
driver.implicitly_wait(5)
#driver = webdriver.Chrome(executable_path=executable_path)

reviews = getReviews(page_url, driver)

driver.quit()
reviews


# ### Q2. Bonus question

# In[98]:


def getReviews(page_url, driver, expand_review = False, limit = 10):

    result = None
    # add your code here
    driver.get(page_url)
    # now get the page content dynamically generated

    loop = limit//10 if limit%10==0 else (limit//10)+1
    count =0
    reviews_list =[]
    rows=[]
    for i in range(loop):
        page = driver.page_source
        # parse the content by beautifulsoup 
        soup = BeautifulSoup(page, 'html.parser')
        #time.sleep(3)
            
        reviews_list=soup.select("body div[data-test-target=HR_CC_CARD]")
        
        for review in reviews_list:
            reviewer = review.find(class_="ui_header_link")
            username = reviewer.get_text()

            vote = review.select("div[class=MziKN] span[class=phMBo]")

            helpful_votes = vote[1].get_text() if len(vote)==2 else None

            ratings = review.select("div[data-test-target=review-rating]")
            rating = ratings[0].span['class'][1]
            
            reviewtitle = review.select("div[data-test-target=review-title]")
            title = reviewtitle[0].getText()

            if expand_review:
                driver.find_element(By.CLASS_NAME,"TnInx").click
            desc = review.find(class_="QewHA")
            description = desc.getText()

            dates =soup.find(class_="teHYY")
            date = dates.getText()
            
            if count == limit:
                break
            count +=1
            rows.append((username, rating, helpful_votes, title,description, date))
        driver.find_element(By.CLASS_NAME,"next").click()
   
    result =  pd.DataFrame(rows, columns =['reviewer','rating','vote','title','text','date'])
    return result
    


# In[102]:


# Test

page_url = "https://www.tripadvisor.com/Hotel_Review-g60763-d23448880-Reviews-or10-Motto_by_Hilton_New_York_City_Chelsea-New_York_City_New_York.html#REVIEWS"

#executable_path = '../Notes/Web_Scraping/driver/geckodriver'
#driver = webdriver.Firefox(executable_path=executable_path)
from webdriver_manager.chrome import ChromeDriverManager 
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service as ChromeService

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install())) 

reviews = getReviews(page_url, driver, limit =18)

driver.quit()

reviews


# ### Check if full text is collected

# In[106]:


# check if full text is collected

reviews.text.iloc[0]


# ## Main block for testing

# In[107]:


# best practice to test your class
# if your script is exported as a module,
# the following part is ignored
# this is equivalent to main() in Java

if __name__ == "__main__":  
    
    # Test Question 1

    print("\nTest Question 1")
    page_url = "https://www.tripadvisor.com/Hotel_Review-g60763-d23448880-Reviews-or10-Motto_by_Hilton_New_York_City_Chelsea-New_York_City_New_York.html#REVIEWS"

    executable_path = '../Notes/Web_Scraping/driver/geckodriver'
    #driver = webdriver.Firefox(executable_path=executable_path)
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install())) 

    reviews = getReviews(page_url, driver)

    driver.quit()

    print(reviews.head())
    
    
    #3 Test Question 2
    
    print("\nTest Question 2")
    page_url = "https://www.tripadvisor.com/Hotel_Review-g60763-d23448880-Reviews-or10-Motto_by_Hilton_New_York_City_Chelsea-New_York_City_New_York.html#REVIEWS"

    #executable_path = '../Notes/Web_Scraping/driver/geckodriver'
    #driver = webdriver.Firefox(executable_path=executable_path)
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install())) 

    reviews = getReviews(page_url, driver, expand_review = True, limit = 50)

    driver.quit()

    print(reviews.head())
    


# In[ ]:




