from bmb.source.util.exceptions import *
from bmb.source.webscraping.webscraping_utils import SeleniumContext
PAGE_LIMIT = 50

def read_imdb_list( identifier):
    def imdb_list_url( page_num):
        return f"https://www.imdb.com/list/{identifier}/?mode=simple&page={page_num}&sort=list_order,asc"

    films = list()
    for page_number in range(1, PAGE_LIMIT + 1):
        with SeleniumContext( imdb_list_url( page_number)) as driver:
            list_items = driver.find_elements_by_class_name( 'lister-item-header')
            if not list_items:
                return films
            for list_item in list_items:
                words = list_item.text.split( ' ')
                title =' '.join(words[ 1:-1])
                year  = int(words[-1][1:-1])
                films.append((title, year))

    raise Exception( "This list has exceeded the maximum page limit.")
