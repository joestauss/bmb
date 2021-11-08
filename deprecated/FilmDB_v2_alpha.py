from pathlib                                        import Path
from bmb.source.SQLiteDB                         import SQLiteDB
from bmb.source.util.enums                       import AliasType, Infoset
from bmb.source.util.exceptions                  import *
from bmb.source.util.sql_queries                 import Query
from bmb.source.webscraping.tmdb_api             import *
from bmb.source.webscraping.streaming_content    import check_JustWatch
from bmb.source.webscraping.webscraping_utils    import safe_soup
from bmb.source.webscraping.imdb_list            import read_imdb_list

def jupyter_aware_tqdm( iterator, **kwargs):
    from tqdm import tqdm
    from tqdm.notebook import tqdm as notebook_tqdm
    if 'VERBOSE' in kwargs.keys():
        if kwargs[ 'VERBOSE'] == 'jupyter':
            return notebook_tqdm( iterator)
        elif kwargs[ 'VERBOSE']:
            return tqdm( iterator)
    return iterator

class FilmDB( SQLiteDB):
    DEFAULT_DB = Path( __file__).parent / 'resource' / 'Movies.db'

    ############################################################################
    # Enums                                                                    #
    #   These Enums contain database constants.                                #
    #   They mirror tables in the database and are verified correct in testing.#
    ############################################################################
    AliasType = AliasType   # Mirrors "AliasType"
    Infoset   = Infoset     # Mirrors "Infoset"

    ############################################################################
    # Data Access API                                                          #
    #   Alias and Film                                                         #
    #   Genre, Streamer, and Tag (and tag)                                     #
    ############################################################################
    def Film( self, title, year, lookup=False):
        alias_id = self.Alias( title, year)
        film_id  = self.select_one( "film", "Alias", id=alias_id)
        if not film_id:
            if lookup:
                try:
                    self._identify_alias( alias_id)
                    film_id = self.select_one( "film", "Alias", id=alias_id)
                except UnsuccessfulTMDbSearch:
                    self.set( Query.ASSIGN_TYPE_TO_ALIAS, self.AliasType.SEARCH_FAILURE, alias_id)
                    return None
            else:
                raise UnidentifiedAlias( f"title={title}, year={year}")
        return film_id

    def Alias( self, title, year):
        alias_id = self.select_one( "id", "Alias", title=title, year=year)
        if not alias_id:
            near_match = self._similar_alias_search( title, year)
            type = self.AliasType.ALTERNATE if near_match else None
            film = near_match if near_match else None
            self.insert( "Alias", title=title, year=year, type=type, film=film, added=self.now)
            alias_id = self.select_one( "id", "Alias", title=title, year=year)
        return alias_id

    def _identify_alias( self, alias_id):
        title, year    = self.select_one( 'title', 'year', "Alias", id=alias_id)
        tmdb_movie     = get_tmdb_movie( title, year)
        original_title = tmdb_movie.original_title

        # Find the correct film ID.
        existing_film_id = self.select_one( "film", "Alias", id=self.Alias( original_title, year))
        if not existing_film_id:
            maximum = self.select_one( "MAX(film)", "Alias")
            new_film_id = maximum + 1 if maximum is not None else 0
        film_id = existing_film_id if existing_film_id else new_film_id

        # Modify database.
        self.set( Query.ASSIGN_FILM_TO_ALIAS, film_id, alias_id)
        self.set( Query.ASSIGN_TYPE_TO_ALIAS, self.AliasType.ALTERNATE, alias_id )
        if not existing_film_id:
            canonical_alias = self.Alias( original_title, year)
            self.set( Query.ASSIGN_FILM_TO_ALIAS, film_id, canonical_alias)
            self.set( Query.ASSIGN_TYPE_TO_ALIAS, self.AliasType.CANONICAL, canonical_alias )
            self.insert( "FilmLanguage", film=film_id, language=tmdb_movie.original_language)

    def _similar_alias_search(self, title, year):
        similar_aliases = self.get( Query.SIMILAR_ALIAS, title, year)
        for (id, film) in similar_aliases:
            if film != similar_aliases[0][1]:
                raise MultipleSimilarFilms( f"title={title}, year={year} is similar to {[a[0] for a in similar_aliases]}")
        return film if similar_aliases else None

    def Genre( self, genre_text):
        genre_id = self.select_one( 'id', 'Genre', text=genre_text)
        if not genre_id:
            self.insert( "Genre", text=genre_text )
            genre_id = self.select_one( 'id', 'Genre', text=genre_text)
        return genre_id

    def Tag( self, tag_text):
        tag_id = self.select_one( 'id', 'Tag', text=tag_text)
        if not tag_id:
            self.insert( "Tag", text=tag_text, added=self.now )
            tag_id = self.select_one( 'id', 'Tag', text=tag_text)
        return tag_id

    def tag( self, film_id, tag_id):
        if self.select_one( '*', 'FilmTag', film=film_id, tag=tag_id):
            self.set( Query.UPDATE_TIME_OF_FILM_TAG, self.now, film_id, tag_id)
        else:
            self.insert( 'FilmTag', film=film_id, tag=tag_id, added=self.now)

    def Streamer( self, text):
        streamer_id = self.get( Query.SELECT_STREAMER_ID, text, single=True)
        if not streamer_id:
            raise ValueError( f"Unknown streamer: {text}")
        return streamer_id

    def JustWatchURL( self, url):
        url_id = self.select_one( 'id', 'JustWatchURL', url=url)
        if not url_id:
            self.insert( "JustWatchURL", url=url)
            url_id = self.select_one( 'id', 'JustWatchURL', url=url)
        return url_id

    def identify_new_JustWatchURLs( self, VERBOSE=False):
        unknown_urls = self.get( "SELECT url from JustWatchURL WHERE film is Null")
        for url in jupyter_aware_tqdm( unknown_urls, VERBOSE=VERBOSE):
            soup        = safe_soup( url)
            tb          = soup.find( class_='title-block')
            title, year = tb.find( 'h1').text.strip(), int( tb.find( class_='text-muted').text.split( '(')[1].split(')')[0])
            self.set( "UPDATE JustwatchURL SET film=? WHERE url=?", self.Film( title, year, lookup=True), url)

    #   Data Lookup
    #       - unknown_aliases
    #       - unknown_films
    #       - get_infoset

    @property
    def unknown_aliases( self):
        return self.get( Query.UNKNOWN_ALIASES)

    @property
    def unknown_films( self):
        return self.get( Query.SELECT_FILMS_WITHOUT_INFOSET, self.Infoset.BASIC_INFO)

    def get_infoset( self, film_id, infoset):
        if self.select_one( "film", "FilmInfoset", film=film_id, infoset=infoset) is not None:
            return
        elif infoset == self.Infoset.BASIC_INFO:
            self._get_basic_info( film_id)
        elif infoset == self.Infoset.TMDB_RECOMMENDATIONS:
            self._get_tmdb_recs( film_id)
        else:
            raise UnknownInfoset()
        self.insert( "FilmInfoset", film=film_id, infoset=infoset, added=self.now)

    def _get_basic_info( self, film_id):
        title, year = self.select_one( 'title', 'year', 'Alias', film=film_id, type=self.AliasType.CANONICAL)
        tmdb_movie  = get_tmdb_movie( title, year)
        genre       = Genre()
        genre_dict  = { dd[ 'id' ]: dd[ 'name'] for dd in genre.movie_list() }
        genres      = [ genre_dict[i] for i in tmdb_movie.genre_ids ]
        for gen in genres:
            genre_id = self.Genre( gen)
            if not self.select_one( "FilmGenre", film=film_id, genre=genre_id):
                self.insert( "FilmGenre"  , film=film_id, genre=genre_id)
        self.insert( "FilmDescription", film=film_id, description=tmdb_movie.overview )

    def _get_tmdb_recs( self, film_id):
        recs = get_tmdb_recommendations( *self.select_one( 'title', 'year', 'Alias', film=film_id, type=self.AliasType.CANONICAL))
        for title, year in recs:
            rec_id = self.Film( title, year, lookup=True)
            if rec_id:
                self.insert( 'TMDbRecommendation',
                    film=film_id,
                    recommendation=rec_id)

    #   film set slicing

    def filmset( self, year=None, genre=None, tag=None):
        if not year:
            return_set = set(self.select( "DISTINCT film", "Alias"))
        elif isinstance( year, tuple) and len( year)== 2:
            return_set = set(self.get( "SELECT DISTINCT film FROM Alias WHERE year BETWEEN ? AND ?;", year[0], year[1]))
        else:
            raise ValueError( f"Illegal 'year' value: {year}")

        if genre:
            if isinstance( genre, str):
                passed_genre = set(self.get( "SELECT film FROM FilmGenre WHERE genre=?", self.Genre( genre)))
            elif isinstance( genre, tuple):
                passed_genre = return_set
                for g in genre:
                    passed_genre &= self.filmset( year=year, genre=g)
            elif isinstance( genre, set):
                if len( genre) == 1:
                    obj = genre.pop()
                    if isinstance( obj, str):
                        passed_genre = set(self.get( Query.SELECT_NOT_GENRE, self.Genre( obj)))
                    if isinstance( obj, tuple):
                        passed_genre = set()
                        for sub in obj:
                            passed_genre |= self.filmset( year=year, genre={sub})
                else:
                    passed_genre = return_set
                    for g in genre:
                        passed_genre &= self.filmset( year=year, genre={g})
            elif isinstance( genre, list):
                passed_genre = set()
                for g in genre:
                    passed_genre |= self.filmset( year=year, genre=g)
            else:
                raise ValueError( f"Illegal 'genre' value: {genre}")
            return_set &= passed_genre

        if tag:
            if isinstance( tag, str):
                passed_tag = set(self.get( "SELECT film FROM FilmTag WHERE tag=?", self.Tag( tag)))
            elif isinstance( tag, tuple):
                passed_tag = return_set
                for t in tag:
                    passed_tag &= self.filmset( year=year, genre=genre, tag=t)
            elif isinstance( tag, set):
                if len( tag) == 1:
                    obj = tag.pop()
                    if isinstance( obj, str):
                        passed_tag = set(self.get( Query.SELECT_NOT_TAG, self.Tag( obj)))
                    if isinstance( obj, tuple):
                        passed_tag = set()
                        for sub in obj:
                            passed_tag |= self.filmset( year=year, genre=genre, tag={sub})
                else:
                    passed_tag = return_set
                    for f in tag:
                        passed_tag &= self.filmset( year=year, genre=genre, tag={t})
            elif isinstance( tag, list):
                passed_tag = set()
                for t in tag:
                    passed_tag |= self.filmset( year=year, genre=genre, tag=t)
            else:
                raise ValueError( f"Illegal 'tag' value: {tag}")
            return_set &= passed_tag

        return return_set

    #   Web Data

    def update_streaming_content( self, streamer, **kwargs):
        streamer_id  = self.Streamer( streamer)
        streamer_key = self.select_one( 'key', 'Streamer', id=streamer_id)
        found_urls   = check_JustWatch( streamer_key, **kwargs)
        new_urls     = [ url for url in found_urls if url if not self.select_one( '*', 'JustWatchState', url=self.JustWatchURL(url), streamer=streamer_id)]

        for url in new_urls:
            self.insert( 'JustWatchState',
                streamer = streamer_id,
                url      = self.JustWatchURL( url),
                added    = self.now )

        for url in found_urls:
            self.set( Query.UPDATE_CONFIRM_TIME_FOR_JWURL_AT_STREAMER, self.now, self.JustWatchURL( url), streamer_id)

        self.insert( 'JustWatchLog',
            streamer  = streamer_id,
            start_year= kwargs[ 'ymin']  if 'ymin'  in kwargs else None,
            end_year  = kwargs[ 'ymax']  if 'ymax'  in kwargs else None,
            genre     = kwargs[ 'genre'] if 'genre' in kwargs else None,
            total     = len( found_urls),
            new       = len( new_urls),
            completed = self.now )

    def ingest_IMDb_list( self, list_identifier, tag=None):
        if not self.select_one( '*', 'IMDbList', identifier=list_identifier):
            movies = read_imdb_list( list_identifier)
            for title, year in movies:
                if tag:
                    self.tag( self.Film( title, year, lookup=True), self.Tag(tag))
                else:
                    self.Film( title, year, lookup=True)
            self.insert( 'IMDbList',
                identifier = list_identifier,
                length     = len( movies),
                tag        = tag,
                ingested   = self.now )
