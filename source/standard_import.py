from pathlib     import Path
from collections import defaultdict, namedtuple

from bmb.source.databases       import SQLiteDB
from bmb.source.util.safe_soup  import *
from bmb.source.util.exceptions import *
from bmb.gitignored             import *

def jupyter_aware_tqdm( iterator, **kwargs):
    from tqdm import tqdm
    from tqdm.notebook import tqdm as notebook_tqdm
    if 'VERBOSE' in kwargs.keys():
        if kwargs[ 'VERBOSE'] == 'jupyter':
            return notebook_tqdm( iterator)
        return tqdm( iterator)
    return iterator
