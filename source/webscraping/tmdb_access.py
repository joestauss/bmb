from tmdbv3api      import TMDb, Movie, Genre, Person
from bmb.gitignored import TMDB_API_KEY

tmdb = TMDb()
tmdb.api_key = TMDB_API_KEY
tmdb.language = 'en'
tmdb.debug = True

class UnsuccessfulTMDbSearch( Exception): pass

def get_release_year( tmdb_result):
    if "release_date" not in dir( tmdb_result) or not tmdb_result.release_date:
        return None
    try:
        return int(tmdb_result.release_date.split('-')[0])
    except:
        raise ValueError( f"Unknown date format: {tmdb_result.release_date}")

def _parse_film_args( *args, **kw):
    if len( args) == 1:
        title, year = args[0], None
        if 'year' in kw:
            year = kw[ 'year']
    elif len( args) == 2:
        title, year = args[0], int( args[1])
    else:
        raise ValueError
    return title, year

def get_tmdb_movie( *args, **kw):
    title, year = _parse_film_args( *args, **kw)
    movie       = Movie()
    search      = movie.search( title)

    if not year:
        return search[0]
    else:
        for result in search:
            search_year = get_release_year( result)
            if search_year and 'release_date' in dir( result) and len( result.release_date) > 0 and year == search_year:
                return result
        raise UnsuccessfulTMDbSearch
