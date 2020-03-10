import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
from datetime import datetime
import os
import time

def init_browser():
    # Capture path to Chrome Driver & Initialize browser
    executable_path = {'executable_path':"chromedriver.exe"}
    browser = Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars_facts_data = {}
    
    nasa = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(2)

    #using bs to write it into html
    html = browser.html
    soup = bs(html,"html.parser")

    news_title = soup.find("div",class_="content_title").text
    news_paragraph = soup.find("div", class_="article_teaser_body").text
    print(f"Title: {news_title}")
    print(f"Para: {news_paragraph}")


    # Mars Image
    url_image = "https://www.jpl.nasa.gov/spaceimages/?search=&category=featured#submit"
    browser.visit(url_image)

    from urllib.parse import urlsplit
    base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(url_image))
    print(base_url)

    #Design an xpath selector to grab the image
    xpath = "//*[@id=\"page\"]/section[3]/div/ul/li[1]/a/div/div[2]/img"


    #Use splinter to click on the mars featured image
    #to bring the full resolution image
    results = browser.find_by_xpath(xpath)
    img = results[0]
    img.click()
    time.sleep(2)

    #get image url using BeautifulSoup
    html_image = browser.html
    soup = bs(html_image, "html.parser")
    
    img_url = soup.find("img", class_="fancybox-image")["src"]
    full_img_url = base_url + img_url
    mars_facts_data["featured_image"] = full_img_url

    #get mars weather's latest tweet from the website
    tweet_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(tweet_url)
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')

    # Extract latest tweet
    tweet_container = soup.find_all('div', class_="js-tweet-text-container")

    # Loop through latest tweets and find the tweet that has weather information
    for tweet in tweet_container: 
        tweet_container = tweet.find('p').text
        mars_facts_data["mars_weather"] = tweet_container
        if 'sol' and 'pressure' in mars_weather:
            print(tweet_container)
            break
        else: 
            pass

    # Mars Facts
    url_facts = "https://space-facts.com/mars/"
    table = pd.read_html(url_facts)
    table[0]

    df_mars_facts = table[0]
    df_mars_facts.columns = ["Parameter", "Values"]
    df_mars_facts.set_index(["Parameter"])

    mars_html_table = df_mars_facts.to_html()
    mars_html_table = mars_html_table.replace("\n", "")
    mars_facts_data["mars_facts_table"] = mars_html_table


    # Mars Hemisphere
    url_hemisphere = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_hemisphere)

    #Get base url
    hemisphere_base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(url_hemisphere))
    hemisphere_img_urls = []
    print(hemisphere_base_url)


    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html, "html.parser")

    # Create dictionary to store titles & links to images
    hemisphere_image_urls = []

    # Retrieve all elements that contain image information
    results = soup.find("div", class_ = "result-list" )
    hemispheres = results.find_all("div", class_="item")

    # Iterate through each image
    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image_link)
        html = browser.html
        soup = bs(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        hemisphere_image_urls.append({"title": title, "img_url": image_url})

    # Print image title and url
    print(hemisphere_image_urls)
    mars_facts_data["hemisphere_img_url"] = hemisphere_image_urls
    
    return mars_facts_data





