import requests, bs4, re, sys
from pymongo import MongoClient
from bs4 import SoupStrainer
from multiprocessing import Pool
from craiglist_apt_search_scrape import craiglist_apt_search_page_scrape
from craiglist_apt_page_scrape import craiglist_apt_single_page_scrape


## local mongoDB
client = MongoClient('localhost', 27017)

database_name = 'craiglist_content_db'
collection_name ='craiglist_apartment_info' ## the collection in MongoDB is similar to table in regular DB

db = client[database_name]
table = db[collection_name]
if table.count != 0:
    deleted_cotent = table.delete_many({})
    print 'deleted ', deleted_cotent.deleted_count

## increase the system recursion limit for the BeautifulSoup find_all() calls
sys.setrecursionlimit(10000) # default is 1000

scraper = craiglist_apt_search_page_scrape()

def parse_tag(tag):
    if isinstance(tag, bs4.element.Tag):
        contents = scraper.get_tag_contents(tag)
        if 'href' in contents:
            url = contents['href']
            print url
            pasred_page = craiglist_apt_single_page_scrape(url)
            page_content = pasred_page.get_page_content()
            contents.update(page_content)
            #table.insert_one(contents)

init_search_url = 'https://losangeles.craigslist.org/search/apa'
search_url_prefix = 'https://losangeles.craigslist.org/search/apa?s='
search_url_num = range(100, 2500, 100)

url_list = [init_search_url]
for num in search_url_num:
    url_list.append(search_url_prefix + str(num))

for url in url_list:
    response = requests.get(url)
    #soup = bs4.BeautifulSoup(response.text,"html.parser")
    only_content_tags = SoupStrainer("p", class_="row")
    soup = bs4.BeautifulSoup(response.text,"lxml", parse_only=only_content_tags)

    tags = list(soup)
    
    pool = Pool()
    pool.map(parse_tag, tags)
    pool.close()
    pool.join()

    '''
    for tag in soup:
        if isinstance(tag, bs4.element.Tag):
            contents = scraper.get_tag_contents(tag)
            url = contents['href']
            if url is not None:
                print url
                pasred_page = craiglist_apt_single_page_scrape(url)
                page_content = pasred_page.get_page_content()
                contents.update(page_content)
                #table.insert_one(contents)
                print contents
    '''

