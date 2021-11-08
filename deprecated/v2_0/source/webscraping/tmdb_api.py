from tmdbv3api      import TMDb, Movie, Genre, Person
from bmb.gitignored import TMDB_API_KEY
from bmb.source.util.exceptions import *

tmdb = TMDb()
tmdb.api_key = TMDB_API_KEY
tmdb.language = 'en'
tmdb.debug = True

def get_release_year( tmdb_result):
    if "release_date" not in dir( tmdb_result) or not tmdb_result.release_date:
        raise ValueError( f"This object has no date: {tmdb_result}")
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
    title, search_year = _parse_film_args( *args, **kw)
    movie              = Movie()
    search             = movie.search( title)

    if not search_year:
        return search[0]
    else:
        for result in search:
            if 'release_date' in dir( result) and result.release_date and len( result.release_date) > 0:
                found_year = get_release_year( result)
                if found_year == search_year:
                    return result
        raise UnsuccessfulTMDbSearch( str( args))

def get_tmdb_recommendations( *args, **kw):
    film_id = get_tmdb_movie( *args, **kw).id
    return *( (r.title, get_release_year( r)) for r in Movie().recommendations( movie_id=film_id) ),
