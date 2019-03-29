from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    mars_info = {}

    ##visist nasa's website##
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    time.sleep(5)

    #scrap data with beautifulSoup
    html = browser.html
    soup = BeautifulSoup(html,'lxml')
    

    #locate news title and paragraph and assign to variables
    news_title = soup.find('div', class_='content_title').find('a').text
    news_p = soup.find('div', class_='article_teaser_body').text

    mars_info['news_title']=news_title
    mars_info['news_paragraph']=news_p

    ## Mars  ##
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)
    time.sleep(5)
    #Parse HTML with beautifulsoup
    html= browser.html
    soup = BeautifulSoup(html,'lxml')


    #scrape background image
    featured_image_url = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]
    main_url = 'http://www.jpl.nasa.gov'

    final_image_url = main_url+featured_image_url

    #image html string
    mars_info['featured_image_url'] = final_image_url

    ##visit twitter page##
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)
    time.sleep(5)
    #parse twitter page with beautifulSoup
    html= browser.html
    soup = BeautifulSoup(html,'html.parser')


    #scrape weather information
    mars_weather = soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text

    mars_info['weather_info'] = mars_weather

    #Mars Facts
    mars_facts_url = 'https://space-facts.com/mars/'

    #parse space-facts website
    mars_pd = pd.read_html(mars_facts_url)
    mars_df = mars_pd[0]
    mars_df.columns = ['Discription','Value']
    mars_table = dict(zip(mars_df['Discription'],mars_df['Value']))

    #clean_table = mars_df.set_index(["Discription"])
    #mars_html_table = clean_table.to_html()
    #mars_html_table = mars_html_table.replace("\n", "")
    mars_info['mars_facts'] = mars_table

    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)
    time.sleep(5)

    #Parse HTML with beautifulsoup
    html= browser.html
    soup = BeautifulSoup(html,'lxml')

    hemisphere_main_url = 'https://astrogeology.usgs.gov'

    #scrape background image
    images = soup.find_all('div', class_='item')

    hemisphere_image = []

    for image in images:
        #getting the title
        title = image.find('h3').text
        #getting the image link
        img_link = image.find('a', class_='itemLink product-item')['href']
        #visit link
        browser.visit(hemisphere_main_url+img_link)
        time.sleep(2)
        partial_image_url = browser.html
    
        soup = BeautifulSoup(partial_image_url, 'lxml')
    
        #scrap image
        img_url = soup.find('a',{'target':'_blank'})['href']
    
        hemisphere_image.append({'title':title,'img_url':img_url})
    
    mars_info['hemisphere_images']=hemisphere_image

    browser.quit()

    return mars_info