# Dependencies
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    listings = {}

    url =  "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)

    # Retrieve page with the requests module
    response = requests.get(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(response.text, 'html.parser')
    #get title
    # title = soup.find_all('div', class_ = "content_title")
    title_elem = soup.find_all("div", class_ = "grid_layout")

    for div in title_elem:
        if div.find(class_ ="content_title"): 
            actual_title = div
            break
        # else: print("Sorry")

    news_title= actual_title.find_all("a")[1].text

    #get para text

    news_para = soup.find_all("div", class_ = "rollover_description_inner")[0].text

    #get wallpaper url

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)


    imgurl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(imgurl)

    html = browser.html
    findpic = bs(html, 'html.parser')

    pic_filter1 = findpic.find_all('article', class_="carousel_item")[0]

    pic_filter2 = pic_filter1["style"]

    pic_url = pic_filter2.split("(")[1].split(")")[0].split("'")[1]

    base_url = "https://www.jpl.nasa.gov"

    featured_image_url = base_url+pic_url


    #get latest twitter weather report

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)


    weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(weather_url)

    html = browser.html
    findweather = bs(html, 'html.parser')
    mars_weather= findweather.find_all("div", class_="js-tweet-text-container")[0].text

    #get hemisphere urls

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
    "articlePic" : featured_image_url,
    "marsWeather": mars_weather,
    "webTable" : html_table,
    "hemImages": hemisphere_image_urls
    }


    browser.quit()

    return(mars_dict)
