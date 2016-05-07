class craiglist_apt_search_page_scrape(object):
    '''
    this class is a collection of varirous functions to parse
    information out of single BeautifulSoup tag object.
    
    The input is expected to be a section about one apartment
    from Craiglist search webpage.
    '''
    @staticmethod
    def _get_pid_from_tag(tag):
        if 'data-pid' in tag.attrs:
            return tag.attrs['data-pid']
        else:
            return None

    @staticmethod
    def _get_housing_info_from_tag(tag):

        chilren_tags = tag.find_all('span', class_='housing')
        if len(chilren_tags) == 0:
            return None
    
        contents = chilren_tags[0].contents
        if len(contents) == 0:
            return None
        else:
            return contents[0].replace('/', '')

    @staticmethod
    def _get_price_from_tag(tag):
        price_tags = tag.find_all('span', class_='price')
        if len(price_tags) == 0:
            return None
        else:
            return price_tags[0].string

    @staticmethod
    def _get_datetime_from_tag(tag):
        children_tags = tag.find_all('time')
        if len(children_tags) == 0:
            return None

        if 'datetime' in children_tags[0].attrs:
            return children_tags[0].attrs['datetime']
        else:
            return None

    @staticmethod
    def _get_title_from_tag(tag):
        children_tags = tag.find_all('span', id='titletextonly')
        if len(children_tags) == 0:
            return None
        return children_tags[0].string

    @staticmethod
    def _get_href_from_tag(tag, prefix='http://losangeles.craigslist.org'):
        children_tags = tag.find_all('a', class_="hdrlnk")
        if len(children_tags) == 0:
            return None
        if 'href' in children_tags[0].attrs:
            return prefix + children_tags[0].attrs['href']

    @classmethod
    def get_tag_contents(self, tag):
        variable_fetch_dictionary ={'housing_info':self._get_housing_info_from_tag,
                                    'price':self._get_price_from_tag,
                                    'datetime':self._get_datetime_from_tag,
                                    'title':self._get_title_from_tag,
                                    'event_id':self._get_pid_from_tag,
                                    'href':self._get_href_from_tag
                                    }

        variable_content = {}
        for variable_name in variable_fetch_dictionary:
            variable_content[variable_name] = variable_fetch_dictionary[variable_name](tag)

        return variable_content
