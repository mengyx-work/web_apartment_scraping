import requests
import bs4
import re
from pymongo import MongoClient
from bs4 import SoupStrainer
from craiglist_apt_scraping import craiglist_apt_search_page_scrape, craiglist_apt_single_page_scrape


## local mongoDB
client = MongoClient('localhost', 27017)

database_name = 'craiglist_content_db'
collection_name ='craiglist_apartment_info' ## the collection in MongoDB is similar to table in regular DB

db = client[database_name]
table = db[collection_name]
if table.count != 0:
    deleted_cotent = table.delete_many({})
    print 'deleted ', deleted_cotent.deleted_count


init_search_url = 'https://losangeles.craigslist.org/search/apa'
search_url_prefix = 'https://losangeles.craigslist.org/search/apa?s='
search_url_num = range(100, 2500, 100)

url_list = [init_search_url]
for num in search_url_num:
    url_list.append(search_url_prefix + str(num))

scraper = craiglist_apt_search_page_scrape()

for url in url_list:
    response = requests.get(url)
    #soup = bs4.BeautifulSoup(response.text,"html.parser")
    only_content_tags = SoupStrainer("p", class_="row")
    soup = bs4.BeautifulSoup(response.text,"lxml", parse_only=only_content_tags)

    for tag in soup:
        if isinstance(tag, bs4.element.Tag):
            contents = scraper.get_tag_contents(tag)
            url = contents['href']
            print url
            pasred_page = craiglist_apt_single_page_scrape(url)
            contents['loclation'] = pasred_page.get_location()
            contents['apt_attrs'] = pasred_page.get_attrs()
            contents['description'] = pasred_page.get_description()
            table.insert_one(contents)
            #print contents

