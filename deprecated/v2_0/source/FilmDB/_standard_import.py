from bmb.source.SQLiteDB                         import SQLiteDB
from bmb.source.util.enums                       import AliasType, Infoset
from bmb.source.util.exceptions                  import *
from bmb.source.util.sql_queries                 import Query
from bmb.source.webscraping.tmdb_api             import *
from bmb.source.webscraping.imdb_list            import read_imdb_list
from bmb.source.webscraping.streaming_content    import check_JustWatch
from bmb.source.webscraping.webscraping_utils    import safe_soup

def jupyter_aware_tqdm( iterator, **kwargs):
    from tqdm import tqdm
    from tqdm.notebook import tqdm as notebook_tqdm
    if 'VERBOSE' in kwargs.keys():
        if kwargs[ 'VERBOSE'] == 'jupyter':
            return notebook_tqdm( iterator)
        elif kwargs[ 'VERBOSE']:
            return tqdm( iterator)
    return iterator
