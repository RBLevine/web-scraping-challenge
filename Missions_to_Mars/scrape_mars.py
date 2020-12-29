# Dependencies
from bs4 import BeautifulSoup
import requests
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import pymongo
import time

def init_browser():
    executable_path={'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser=init_browser()
    dictionaryMars={}

    # NASA Mars News

    # URL of page to be scraped
    url="https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(1)
    # Beautiful Soup
    html=browser.html
    soup=BeautifulSoup(html,'html.parser')
    # Store Latest News Title and Paragraph Text
    newsInfo=soup.select_one('ul.item_list li.slide')
    news_title=newsInfo.find('div', class_='content_title').text
    news_p=newsInfo.find('div', class_='article_teaser_body').get_text()

    # JPL Mars Space Images - Featured Image

    # URL of page to be scraped
    space_url="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(space_url)
    # Beautiful Soup
    html_image=browser.html
    soup=BeautifulSoup(html_image,'html.parser')
    # Store the full image link
    new_html_image=browser.html
    soup=BeautifulSoup(new_html_image,'html.parser')
    featured_image=soup.find_all('img')[74]['src']
    featured_image_url="https://www.jpl.nasa.gov"+featured_image

    # Mars Facts

    # URL of page to be scraped
    mars_url="https://space-facts.com/mars/"
    # use Pandas to read
    table=pd.read_html(mars_url)
    # Convert to data frame
    marsDF=table[2]
    marsDF.columns=["Description","Value"]
    # Convert to html
    marsHtml=marsDF.to_html()
    marsHtml=marsHtml.replace('\n',"")

    # Mars Hemispheres

    # URL of page to be scraped
    hemisphere_url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemisphere_url)
    # Beautiful Soup
    hemisphere_html=browser.html
    soup=BeautifulSoup(hemisphere_html, 'html.parser')
    # Hemisphere information
    hemisphereInfo=soup.find_all('div', class_='item')
    # Empty list for hemispher urls
    hemisphere_image_urls=[]
    # Main url
    main_url="https://astrogeology.usgs.gov"
    # loop through the hemisphere information
    for item in hemisphereInfo:
        # Store hemisphere name
        title=item.find('h3').text
        # Grab partial image link
        partialImage=item.find('a', class_='itemLink product-item')['href']
        browser.visit(main_url+partialImage)
        # Store the full url
        fullUrl=browser.html
        soup=BeautifulSoup(fullUrl,'html.parser')
        # Store the full image url sourc
        imageUrl=main_url+soup.find('img', class_='wide-image')['src']
        # Add information to the hemisphere list
        hemisphere_image_urls.append({"title":title, "image_url":imageUrl})   
        
    dictionaryMars={
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_fact_table": str(marsHtml),
        "hemisphere_images": hemisphere_image_urls
    }

    browser.quit()

    return dictionaryMars