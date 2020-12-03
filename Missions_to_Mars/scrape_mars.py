from flask import Flask, render_template, redirect
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import pymongo

def request_soup(url):
    # Retrieve page with the requests module
    response = requests.get(url)
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(response.text, 'html.parser')

    return soup

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
  # executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    executable_path = {'executable_path':ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
 
    # NASA Mars News title and paragraph
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    # Retrieve the latest news title and paragraph
    news_titles = soup.find('div', class_='content_title').text
    news_paragraph = soup.find('div',class_='rollover_description_inner').text
    
    return news_titles, news_paragraph

    # Scrape JPL Mars images
    base_url = "https://www.jpl.nasa.gov"
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)
    html = browser.html
    image_page = bs(html,'html.parser')
   
    featured_image = image_page.find('img',class_='thumb')
    featured_image_url = base_url + featured_image['src']
    return featured_image_url
    
    # Mars Facts
    mars_facts_url = "https://space-facts.com/mars/"
    mars_facts = pd.read_html(facts_url)[2]
    mars_facts.columns = ['Data','Value']
    
    mars_facts_table_html = mars_facts.to_html()
    return mars_facts_table_html


    # Mars Hemisphere

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    soup = bs(html,'html.parser')   
    

    # Get the html containing the title and put itnto a list
    title_list = soup.find_all('div', class_='description')

    # Loop through the 'div' objects and scrape the titles and urls of images
    # Create a list to store the dictionaries
    hemisphere_image_urls = []
    for title in title_list:
        # Navigate browser to page then click on title link to image page
        browser.visit(url)
        browser.click_link_by_partial_text(title.a.h3.text)
    
         # Grab the destination page html and make into BeautifulSoup Object
        html = browser.html
        soup = bs(html, 'html.parser')
    
         # Parse the imgage source(src) relative url and then append to domain name
         # for absolute url
        img_url_list = soup.find('img', class_='wide-image')
        img_url = f"https://astrogeology.usgs.gov{img_url_list['src']}"
    
         # Create Dictionary with returned values and add dict to hemi_image_urls list
        post = {
                'title': title.a.h3.text,
                'image_url': img_url
                }
            
        hemisphere_image_urls.append(post)
    
    # Initialize mars_data dictionary to hold all scraped values to be entered into MongoDB
                

    mars_data = {
    "news_titles": news_titles,
    "news_paragraph": news_paragraph,
    "featured_image_url": featured_image_url,
    "mars_facts_table_html": mars_facts_table_html,
    "hemisphere_image_urls": hemisphere_image_urls
    }
    print(mars_data)   
    return mars_data