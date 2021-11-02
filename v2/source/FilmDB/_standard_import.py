from bmb.v2.source.SQLiteDB                         import SQLiteDB
from bmb.v2.source.util.enums                       import AliasType, Infoset
from bmb.v2.source.util.exceptions                  import *
from bmb.v2.source.util.sql_queries                 import Query
from bmb.v2.source.webscraping.tmdb_api             import *
from bmb.v2.source.webscraping.imdb_list            import read_imdb_list
from bmb.v2.source.webscraping.streaming_content    import check_JustWatch
from bmb.v2.source.webscraping.webscraping_utils    import safe_soup

def jupyter_aware_tqdm( iterator, **kwargs):
    from tqdm import tqdm
    from tqdm.notebook import tqdm as notebook_tqdm
    if 'VERBOSE' in kwargs.keys():
        if kwargs[ 'VERBOSE'] == 'jupyter':
            return notebook_tqdm( iterator)
        elif kwargs[ 'VERBOSE']:
            return tqdm( iterator)
    return iterator
