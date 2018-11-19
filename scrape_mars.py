# Dependencies
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import pandas as pd
from flask import Flask, render_template

import pymongo


# URL of page to be scraped
url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"

# Retrieve page with the requests module
response = requests.get(url)

# Create BeautifulSoup object; parse with 'html.parser'
soup = bs(response.text, 'html.parser')
#get title
# title = soup.find_all('div', class_ = "content_title")
news_title = soup.find_all("div", class_ = "content_title")[0].text
#why's it giving me all this stuff - but not the most recent text ?

#get para text
# results = soup.find_all('li', class_="result-row")
news_para = soup.find_all("div", class_ = "image_and_description_container")[0].text

executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

for x in range(1):

    html = browser.html
    findpic = bs(html, 'html.parser')

a_find= findpic.find_all('a', class_ = "button fancybox")



imgurl = "https://twitter.com/marswxreport?lang=en"
browser.visit(imgurl)

html = browser.html
findweather = bs(html, 'html.parser')
mars_weather= findweather.find_all("div", class_="js-tweet-text-container")[0].text

facts_url = 'https://space-facts.com/mars/'
tables = pd.read_html(facts_url)

facts_df = tables[0]
facts_df.columns = ["Fact", 'Data']
facts_df.set_index("Fact", inplace = True)
html_table = facts_df.to_html()
html_table

hemisphere_image_urls = [
    {"title": "Valles Marineris Hemisphere", "img_url": "http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif"},
    {"title": "Cerberus Hemisphere", "img_url": "http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif"},
    {"title": "Schiaparelli Hemisphere", "img_url": "http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif"},
    {"title": "Syrtis Major Hemisphere", "img_url": "http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif"},
]


mars_dict = {
"newsTitle" : news_title, 
"newsPara": news_para, 
"articlePic" : a_find,
"marsWeather": mars_weather,
"webTable" : html_table,
"hemImages": hemisphere_image_urls
}

print(mars_dict)