#import dependencies
import pandas as pd
import os
import requests
import warnings
from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)

def scrape ():
    browser = init_browser()

    #set url
    url = "https://mars.nasa.gov/news"
    browser.visit(url)
    html = browser.html

    soup = bs(html, 'html.parser')

    #get li in class 'slide' and print
    articles = soup.find_all('li', class_='slide')[0]
    print(articles.prettify()) 

     #find the headline in the 'content_title' class
    headline = articles.find(class_='content_title').text
    headline  

    #find paragraph in 'article_teaser_body' class
    paragraph = articles.find(class_='article_teaser_body').text

    #go to URL for JPL featured space image
    url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    browser.visit(url)
    html = browser.html 

    soup = bs(html, 'html.parser') 

    #find header with image
    image = soup.find_all('div', class_='header')[0]
    print(image.prettify())

    # find image under proper class 
    featured_image = image.find('img', class_='headerimage fade-in')
    featured_image = featured_image.attrs.get('src', None)
    featured_image

    #print featured image url
    featured_image_url = os.path.dirname(url)
    print(featured_image_url)

    #print root url with image
    complete_image_url = f'{url}/{featured_image}'
    print(complete_image_url)

    # open mars fact url and view data
    mars_facts_url = "https://space-facts.com/mars/"
    table = pd.read_html(mars_facts_url)
    print(table)

    #create mars fact dataframe
    mars_facts_df = table[0]
    mars_facts_df

    #create html table
    mars_html = mars_facts_df.to_html()
    mars_html = mars_html.replace('\n', '')
    mars_html

    #Visit the USGS Astrogeology site
    astrogeology_url = "https://astrogeology.usgs.gov/search/map/Mars/Viking"

    valles_marineris_html = requests.get(f'{astrogeology_url}/valles_marineris_enhanced')
    cerberus_html = requests.get(f'{astrogeology_url}/cerberus_enhanced')
    schiaparelli_html = requests.get(f'{astrogeology_url}/schiaparelli_enhanced')
    syrtis_major_html = requests.get(f'{astrogeology_url}/syrtis_major_enhanced')

    #parse beautiful soup objects

    soup_vm = bs(valles_marineris_html.text, 'html.parser')
    soup_cb = bs(schiaparelli_html.text, 'html.parser')
    soup_sc = bs(schiaparelli_html.text, 'html.parser')
    soup_sm = bs(syrtis_major_html.text, 'html.parser')

    #create list for dictionaries
    astrogeology_image_urls = []

    # get teh class that has the needed info
    results_vm = soup_vm.find_all('div', class_='container')
    results_cb = soup_cb.find_all('div', class_='container')
    results_sc = soup_sc.find_all('div', class_='container')
    results_sm = soup_sm.find_all('div', class_='container')

    #set up loop
    astrogeology_results = [results_vm, results_cb, results_sc, results_sm]

    # run loop
    for result in astrogeology_results:
        for r in result:
            title = r.find('h2', class_='title').text
            img_url = r.find('img', class_='wide-image')
            img_url = img_url.attrs.get('src', None)
            img_url = f"https://astrogeology.usgs.gov{img_url}"
            results_dict = {"title": title, "img_url": img_url}
            astrogeology_image_urls.append(results_dict)
    
    #print results
    astrogeology_image_urls

    scrape_dict = {
        "headline": headline,
        "paragraph": paragraph, 
        "complete_image_url": complete_image_url,
        "mars_html": mars_html,
        "astrogeology_image_urls": astrogeology_image_urls

    }

    browser.quit()

    return scrape_dict


