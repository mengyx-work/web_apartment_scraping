import requests, bs4, re
from bs4 import SoupStrainer

class craiglist_apt_single_page_scrape(object):
    '''
    this class provides object to parse sinle craigplist
    apartment webpage. class functions are able to parse
    out the location and attributes.
    '''
    def __init__(self, url):
        response = requests.get(url)
        self.soup = bs4.BeautifulSoup(response.text,"lxml") 

    def _get_attrs(self):
        attrs_list = []
        attrgroups = self.soup.find_all('p', class_='attrgroup')
        for attrgroup in attrgroups:
            attrs = attrgroup.find_all('span', text=True)
            for attr in attrs:
                attrs_list.append(attr.string)
        return attrs_list

    def _get_location(self):
        mapAddr_tags = self.soup.find_all('div', class_='mapaddress')
        if len(mapAddr_tags) == 0:
            mapAddr = None
        else:
            mapAddr = mapAddr_tags[0].string

        locale_attrs_tags = self.soup.find_all('div', class_='viewposting')
        if len(locale_attrs_tags) == 0:
            mapLatitude, mapLongtitude = None, None
        else:
            mapLatitude = locale_attrs_tags[0].attrs['data-latitude']
            mapLongtitude = locale_attrs_tags[0].attrs['data-longitude']

        return {'mapAddr':mapAddr, 'mapLatitude':mapLatitude, 'mapLongtitude':mapLongtitude}

    def _get_description(self):
        dspr_tags = self.soup.find_all('section', id='postingbody')
        if len(dspr_tags) == 0:
            return None
        else:
            str_list = dspr_tags[0].find_all(text=True)
            tmp_list = [elem for elem in str_list if elem != u'\n']
            return ''.join(tmp_list)

    def get_page_content(self):
        contents = {}
        contents['loclation'] = self._get_location()
        contents['apt_attrs'] = self._get_attrs()
        contents['description'] = self._get_description()
        return contents

