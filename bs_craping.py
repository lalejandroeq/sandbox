from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import re


class Sauce:
    def __init__(self, url):
        self.__url = url
        self.sauce = self.__get_sauce()

    # *****Private methods*****
    def __get_sauce(self):
        try:
            sauce = urlopen(self.__url)
            return sauce
        except HTTPError:
            raise Exception('Page not found in server: error found while requesting html on {0}'.format(self.__url))
        except URLError:
            raise Exception('Page server not found: error found while requesting html on {0}'.format(self.__url))


class Soup(Sauce):
    def __init__(self, url, parser='lxml', filters_list=None):
        Sauce.__init__(self, url)
        self.__sauce = self.sauce
        self.__parser = parser
        self.__filters_list = filters_list
        self.__beautiful_soup = self.__get_soup()

    # *****Special methods*****
    def __str__(self):
        pass

    # *****Private methods*****
    def __get_soup(self):
        beautiful_soup = BeautifulSoup(self.__sauce, self.__parser)
        if self.__filters_list is not None:
            for filter_item in self.__filters_list:
                for tag in beautiful_soup.select(filter_item):
                    tag.decompose()
        return beautiful_soup

    def get_links(self, url_pattern=''):
        link_list = [link.get('href')
                     for link in self.__beautiful_soup.find_all('a')
                     if link.get('href') is not None
                     and re.search(url_pattern, link.get('href')) is not None]
        return link_list

    def get_tags(self):
        tags = self.__beautiful_soup.find_all(True)
        return tags

    def get_text(self):
        text_string = ' '.join(self.__beautiful_soup.stripped_strings)
        return text_string


class TagDetails(Soup):
    def __init__(self, url, parser='lxml', filters_list=None):
        Soup.__init__(self, url, parser=parser, filters_list=filters_list)
        self.__tags = self.get_tags()

    # *****Special methods*****
    def __str__(self):
        pass

    # *****Private methods*****
    @staticmethod
    def __get_tag_class(tag):
        try:
            tag_class = ' '.join(tag["class"])
            return tag_class
        except KeyError:
            return None

    @staticmethod
    def __get_tag_style(tag):
        try:
            tag_style = tag["style"]
            return tag_style
        except KeyError:
            return None

    @staticmethod
    def __get_tag_text(tag):
        try:
            tag_text = tag.string
            return tag_text
        except AttributeError:
            return None

    # *****Public methods*****
    def get_tag_names(self):
        tag_names = [tag.name for tag in self.__tags]
        return tag_names

    def get_tag_classes(self):
        tag_classes = [self.__get_tag_class(tag) for tag in self.__tags]
        return tag_classes

    def get_tag_styles(self):
        tag_classes = [self.__get_tag_style(tag) for tag in self.__tags]
        return tag_classes

    def get_text_flags(self):
        text_flags = [1 if tag.string is not None else 0 for tag in self.__tags]
        return text_flags

    def get_tag_texts(self):
        tag_classes = [self.__get_tag_text(tag) for tag in self.__tags]
        return tag_classes
