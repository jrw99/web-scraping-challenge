import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

def scrape():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


    # ************* NASA Mars News **************

    # Load the page
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Scrape into Soup
    html = browser.html
    soup = bs(html, 'html.parser')

    # time.sleep(1)

    # get the first list_date (if needed) and retain content_title and article_teaser_body inside of list_text as they 
    # are in chronological order with the latest being first
    marsNews_latest_Title = soup.find('div', class_='content_title').get_text()
    marsNews_latest_ArticleBody = soup.find('div', class_='article_teaser_body').get_text()    


    # ************* JPL Mars Space Images - Featured Image **************

    # Load the page
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)

    # Scrape into Soup
    html = browser.html
    soup = bs(html, 'html.parser')

    # Make sure to find the image url to the full size .jpg image.
    btn = soup.find('button', text=' FULL IMAGE')
    if btn.parent.name == 'a':
        a = btn.parent

    if a:
        featured_image_url = a['href']

    # Make sure to save a complete url string for this image.
    marsImages_featured_image_url = url + featured_image_url


    # ************* Mars Facts **************
    
    # scrape the site and gather the html for the table
    url = 'https://galaxyfacts-mars.com/'
    table = pd.read_html(url, match='Equatorial Diameter')

    # convert to dataframe
    df = table[0]

    # render out to html table string
    marsFacts_html_tbl = df.to_html(index=False, classes="table table-striped", header=False)
    marsFacts_html_tbl = marsFacts_html_tbl.replace('\n', '')


    # ************* Mars Hemispheres **************

    marsHemispheres_image_urls = []

    # load initial page
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # Scrape into Soup
    html = browser.html
    soup = bs(html, 'html.parser')

    # Second browser to find full res image in sub pages
    browser2 = Browser("chrome", **executable_path, headless=False)

    # find the parent of the list of hemishpere items we want
    container = soup.find('div', class_='results')

    # get all of the hemispheres within
    items = container.find_all('div', class_='item')

    # loop through each hemishpere 
    for item in items:
    
        # get the title 
        title = item.find('h3').get_text() 

        # launch second browser to sub page to find the full res image
        page = item.find('a', class_='product-item')['href']
        url2 = url + page   
        browser2.visit(url2)
        html2 = browser2.html
        soup2 = bs(html2, 'html.parser')

        # NOTE instructions say to get the full res image which is a tif and doesn't make sense to try and render in browser (only Safari supports it) 
        # Download it instead. Change Sample to Original to refer to the tif as per the instructions, but it won't render...
        img_url = url + soup2.find('a', text='Sample')['href']

        # Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys img_url and title.
        hemishpere_dict = {
            "title":title, 
            "img_url":img_url
        }

        # Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.
        marsHemispheres_image_urls.append(hemishpere_dict)

        # Store data in a dictionary
        mars_data = {
            "marsNews_latest_Title": marsNews_latest_Title,
            "marsNews_latest_ArticleBody": marsNews_latest_ArticleBody,
            "marsImages_featured_image_url": marsImages_featured_image_url,
            "marsFacts_html_tbl": marsFacts_html_tbl,
            "marsHemispheres_image_urls": marsHemispheres_image_urls
        }

    # Close the browsers after scraping
    browser2.quit()
    browser.quit()

    # Return results
    return mars_data
