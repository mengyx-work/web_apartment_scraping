import requests, bs4, re, sys
from pymongo import MongoClient
from bs4 import SoupStrainer
from multiprocessing import Pool
from multiprocessing.pool import ThreadPool

from craiglist_apt_search_scrape import craiglist_apt_search_page_scrape
from craiglist_apt_page_scrape import craiglist_apt_single_page_scrape

database_name = 'craiglist_content_db'
collection_name ='craiglist_apartment_info' ## the collection in MongoDB is similar to table in regular DB

def create_db_connection(database_name, collection_name):
    ## local mongoDB
    client = MongoClient('localhost', 27017)
    db = client[database_name]
    table = db[collection_name]
    return table

def purge_collection(table):
    if table.count != 0:
        deleted_cotent = table.delete_many({})
        print 'deleted ', deleted_cotent.deleted_count

## increase the system recursion limit for the BeautifulSoup find_all() calls
sys.setrecursionlimit(10000) # default is 1000
table = create_db_connection(database_name, collection_name)
purge_collection(table)

def parse_tag_content(contents):
    '''
    function to parse single craiglist page by URL
    argument contents is a dictionary from parsing the search page
    '''
    updated_contents = contents.copy()
    if 'href' in contents:
        url = contents['href']
        print url
        pasred_page = craiglist_apt_single_page_scrape(url)
        page_content = pasred_page.get_page_content()
        updated_contents.update(page_content)
    return updated_contents

def parse_search_page_URL(url, database_name, collection_name):
    '''
    function to parse search URL and also parse each webpage
    for every apartment.
    final result is saved into a mongoDB collection table.
    '''
    scraper = craiglist_apt_search_page_scrape()
    soup = scraper.parse_URL(url)
    for tag in soup:
        if isinstance(tag, bs4.element.Tag):
            contents = scraper.get_tag_contents(tag)
            updated_contents = parse_tag_content(contents)

            table = create_db_connection(database_name, collection_name)
            table.insert_one(updated_contents)

def create_craiglist_apt_URLs():
    init_search_url = 'https://losangeles.craigslist.org/search/apa'
    search_url_prefix = 'https://losangeles.craigslist.org/search/apa?s='
    search_url_num = range(100, 2500, 100)

    url_list = [init_search_url]
    for num in search_url_num:
        url_list.append(search_url_prefix + str(num))

    return url_list

url_list = create_craiglist_apt_URLs()

pool = Pool(8)
#pool = ThreadPool(12)
pool.map(parse_search_page_URL, url_list)
pool.close()
pool.join()

