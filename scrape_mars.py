# Dependencies
from bs4 import BeautifulSoup
import requests
import pymongo
import dns
import datetime
from time import sleep
import random
import json
import pandas as pd

from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

import config

class scraper:

    # init method or constructor
    def __init__(self):
        self.name = config.pg_username
        self.listings_collection = None

        conn = config.mongo_conn
        client = pymongo.MongoClient(conn)

        client.server_info() # Will throw an exception if DB is not connected. @TODO Add better handling of this

        # Define database and collection
        db = client[config.db_name]
        self.listings_collection = db.listings


    def get_soup(self,listing_url, browser):
        # URL of page to be scraped
        url = listing_url

        # Sleep for a bit
        sleep(random.randint(1,3))

        browser.visit(url)
        html_listings = browser.html
        # Parse HTML with Beautiful Soup
        soup = BeautifulSoup(html_listings, 'html.parser')
        
        return soup
    
    def scrape(self, browser):
        # NASA Mars News
        url_nasanews = 'https://mars.nasa.gov/news/'

        # JPL Mars Space Images - Featured Image
        url_spaceimage = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'

        # Mars Facts
        url_spacefacts = 'https://space-facts.com/mars/'

        # Mars Hemispheres
        url_usgs_astro ='https://astrogeology.usgs.gov'

        usgs_astro_search = '/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        
        # mars news
        soup_news = self.get_soup(url_nasanews,browser)
        news_title = ''
        news_p = ''
        list_item = soup_news.find('div',class_='slide')
        news_title = list_item.find('div',class_='content_title').text.strip()
        news_p = list_item.find('div',class_='rollover_description_inner').text.strip()

        # featured image
        soup_spaceimage = self.get_soup(url_spaceimage,browser)
        header = soup_spaceimage.find('div',class_='floating_text_area')
        featured_image_url = url_spaceimage.replace('index.html','') + header.a['href']

        # mars facts
        tables = pd.read_html(url_spacefacts)        
        df = tables[0]
        df.columns = ['Fact Label', 'Fact']        
        html_table = df.to_html()

        # mars hemisphere
        soup_marshem = self.get_soup(url_usgs_astro + usgs_astro_search, browser)
        sleep(5)
        items = soup_marshem.find_all('div',class_='item')
        item_detail_urls = []
        for item in items:
            item_detail_urls.append(url_usgs_astro + item.a['href'])
        hemisphere_image_urls = []

        for url in item_detail_urls:
            title = ''
            img_url = ''        
            
            soup_hemdetails = self.get_soup(url,browser)
            sleep(5)
            title = soup_hemdetails.find('h2',class_='title').text

            downloads = soup_hemdetails.find('div',class_='downloads')    
            sleep(5)
            for a in downloads.find_all('a'):
                if a.text.lower() == 'original':
                    img_url = a['href']

            hemisphere_img_dict = {
                'title': title,
                'img_url': img_url
            }

            hemisphere_image_urls.append(hemisphere_img_dict)
        
        # if outside source scrape has problem (url will not resolve), add test placeholder images
        if len(hemisphere_image_urls) == 0:
            hemisphere_image_urls = [
                {
                'title': 'Valles Marineris Hemisphere Enhanced',
                'img_url': 'images/mars1.jpg'
                },
                {
                'title': 'Cerberus Hemisphere Enhanced',
                'img_url': 'images/mars2.jpg'
                },
                {
                'title': 'Schiaparelli Hemisphere Enhanced',
                'img_url': 'images/mars3.jpg'
                },
                {
                'title': 'Syrtis Marjo Hemisphere Enhanced',
                'img_url': 'images/mars4.jpg'
                }
            ]

        mars_dict = {
            'news_title': news_title,
            'news_p': news_p,
            'featured_image_url': featured_image_url,
            'mars_facts_html': html_table,
            'hemisphere_image_urls':hemisphere_image_urls
        }

        #######################################
        # insert or update document in mongoDB
        #######################################

        client = pymongo.MongoClient(config.mongo_conn)

        # Define the 'mars_collection' database in Mongo
        db = client.mars_db
        collection = db.mars_collection

        # check if document already exists
        objectId = ''
        for item in collection.find():
            objectId = item['_id']
            break   

        if objectId == '':
            collection.insert(mars_dict)
        else:
            modified_datetime = datetime.datetime.utcnow()
            
            collection.find_one_and_update(
                {'_id' : objectId},
                {'$set':
                    {
                        'modified_datetime': modified_datetime,
                        'news_title': mars_dict['news_title'],                
                        'news_p': mars_dict['news_p'],
                        'featured_image_url': mars_dict['featured_image_url'],
                        'mars_facts_html': mars_dict['mars_facts_html'],
                        'hemisphere_image_urls':mars_dict['hemisphere_image_urls']
                    }
                    
                },upsert=True
            )
            

        return mars_dict