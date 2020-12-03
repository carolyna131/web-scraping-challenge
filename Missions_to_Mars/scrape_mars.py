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
    base_url = "https://astrogeology.usgs.gov"
    mars_hemi_url= "https://astrogeology.usgs.gov/search/resultsq=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(mars_hemi_url)
    html = browser.html
    soup = bs(html,'html.parser')
    hemispheres_list = soup.find('div', id='product-section')

    
    hemi_desc = hemispheres_list.find_all("div", class_="description")
    hemisphere_image_urls = []

    for i in hemi_desc:
        hemisphere_dict = {}
    
        title = i.find('h3').text
        hemisphere_dict['title']= title
        link = i.find('a')['href']
        page = base_url+link
    
        # Navigate the new page
        browser.visit(page)
        hemisphere_html = browser.html
        hemisphere_page = bs(hemisphere_html,'html.parser')
    
        # save mars hemisphere images urls
        img_url = hemisphere_page.find('li').a['href']
        hemisphere_dict['img_url']= img_url
        hemisphere_image_urls.append(hemisphere_dict)

        return hemisphere_image_urls

      

    mars_info = {}
    mars_info["news_title"] = news_title
    mars_info["news_p"] = news_p
    mars_info["featured_image_url"] = featured_image_url
    mars_info["marsfacts_html"] = facts_html_table
    mars_info["hemisphere_image_urls"] = hemisphere_image_urls
       
    return mars_info