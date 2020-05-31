# import dependencies

from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import requests
import time

def init_browser():
    executable_path = {'executable_path': './chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)

mars_dict= {}
hemisphere_image_urls = []

def scrape_news():
    
    browser = init_browser()

    #browser.visit('https://mars.nasa.gov/news/')
    #mars_news_html = browser.html
    #news_soup = BeautifulSoup(mars_news_html,'html.parser')

    browser = init_browser()

    browser.visit('https://mars.nasa.gov/news/')
    time.sleep(5)

    mars_news_html = browser.html
    news_soup = BeautifulSoup(mars_news_html,'html.parser')


    news_title = news_soup.find_all('div', attrs={'class':'content_title'})[1].get_text()
    news_des = news_soup.find('div', attrs={'class':'article_teaser_body'}).get_text()
    
    mars_dict['latest_news_title'] = news_title
    mars_dict['latest_news_description'] = news_des
   
    browser.quit()
    return mars_dict
    
def scrape_marsImage():
    
    browser = init_browser()
    
    featured_image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(featured_image_url)
    
    img_html = browser.html
    soup = BeautifulSoup(img_html, 'html.parser')
    
    feature_img = soup.find('article',class_='carousel_item')['style']    
    featured_image_url = 'https://www.jpl.nasa.gov' + feature_img[23:-3]

    mars_dict['featured_image'] = featured_image_url
    
    browser.quit()
    return mars_dict
    
def scrape_marsWeather():

    browser = init_browser()

    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)

    time.sleep(5)

    html_weather = browser.html
    soup = BeautifulSoup(html_weather, 'html.parser')
    
    latest_tweets = soup.find_all('span')
    
    weather =[]
    for i in latest_tweets:
        if "InSight sol" in i.text:
            print(i)
            weather.append(i.text)

    mars_dict['mars_weather'] = weather[0].replace("\n", " ")
    browser.quit() 
    return mars_dict
    
def scrape_marsFacts():
    browser = init_browser()
    
    facts_url = 'http://space-facts.com/mars/'
    mars_facts = pd.read_html(facts_url)
    mars_df = mars_facts[0]
    mars_df.columns = ['Description','Value']
    mars_df.set_index('Description', inplace=True)
    data = mars_df.to_html()
    mars_dict['mars_data'] = data
    browser.quit()
    return mars_dict
        
def scrape_mars_hemispheres():

    browser = init_browser()

    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)
    html_hemispheres = browser.html

    soup = BeautifulSoup(html_hemispheres, 'html.parser')
    items = soup.find_all('div', class_='item')

    hemispheres = []

    hemispheres_main_url = 'https://astrogeology.usgs.gov' 

    for i in items: 
        title = i.find('h3').text
        partial_img_url = i.find('a', class_='itemLink product-item')['href']
        
        browser.visit(hemispheres_main_url + partial_img_url)
        partial_img_html = browser.html
        
        soup = BeautifulSoup( partial_img_html, 'html.parser')
        img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
        
        hemispheres.append({"title" : title, "img_url" : img_url})

    mars_dict['hem_info'] = hemispheres

    browser.quit()
    return mars_dict

