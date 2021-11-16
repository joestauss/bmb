from bmb.deprecated.v1.source.webscraping.tmdb_access import *
from bmb.deprecated.v1.source.standard_import         import *


class ProcessingDB( SQLiteDB):
    DEFAULT_DB = V1_RESOURCE_DIRECTORY / "Processing.db"

    id_tables = {
        "Film"     : ( "title" ,  "year" ),
        "Genre"    : ( "text", ),
        "Credit"   : ( "name", ),
    #    "Role"     : ( "text", ),
        "Tag"      : ( "text", ),
        "Status"   : ( "text", )
    }

    @property
    def unverified_films( self):
        return self.select( 'id', "Film", status=0)

    def Film( self, title, year):
        if not self.id( "Film", title, year):
            self.insert( "Film", title=title, year=year, added=self.date_str)
        return self.id( "Film", title, year)

    def Status( self, text):
        if not self.id( "Status", text):
            self.insert( "Status", text=text, added=self.date_str )
        return self.id( "Status", text)

    def Genre( self, text):
        return self.id( "Genre", text, insert_new=True)

    def lookup_film_info( self, film_id):
        if self.select_one( "status", "Film", id=film_id ) == 0:
            UPDATE_STATUS =  "UPDATE Film SET STATUS=? WHERE id=?"
            try:
                tmdb_movie = get_tmdb_movie( *self.select_one( 'title', 'year', "Film", id=film_id) )
                if tmdb_movie.original_language != "en":
                    raise Foreign_Lanaguge_Hold()
            except UnsuccessfulTMDbSearch:
                self.set( UPDATE_STATUS, self.Status( "TMDb search failure"), film_id )
                return
            except Foreign_Lanaguge_Hold:
                holdout_languages = ('it', )
                current_language  = tmdb_movie.original_language
                if current_language in holdout_languages:
                    self.set( UPDATE_STATUS, self.Status(f"foreign language hold - {current_language.upper()}"), film_id)
                else:
                    self.set( UPDATE_STATUS, self.Status( "foreign language hold - other"), film_id)
                return

            genre      = Genre()
            genre_dict = { dd[ 'id' ]: dd[ 'name'] for dd in genre.movie_list() }
            genres     = [ genre_dict[i] for i in tmdb_movie.genre_ids ]
            for gen in genres:
                genre_id = self.Genre( gen)
                if not self.select( "FilmGenre", film=film_id, genre=genre_id):
                    self.insert( "FilmGenre"  , film=film_id, genre=genre_id   )
            self.insert( "FilmDescription", film=film_id, text=tmdb_movie.overview )
            self.set( UPDATE_STATUS, self.Status( f"basic info"), film_id )

    def old_rating_dictionary( self, film_ids):
        return_dict = defaultdict( set)
        for film_id in film_ids:
            title, year = self.select_one( 'title', 'year', "Film", id=film_id)
            old_rating  = self.select_one( 'rating', "OldRating", title=title, year=year)
            old_rating  = old_rating if old_rating else 'no rating'
            return_dict[ old_rating].add( film_id)
        return return_dict

    @property
    def films_for_analysis( self):
        valid = (
            self.Status( 'basic info'),
            self.Status( 'warehouse' ) )
        QUERY = f"SELECT id FROM Film WHERE status IN ({','.join( '?'*len(valid))})"
        return self.get( QUERY, *valid)

    def genre_combinations( self, film_ids):
        QUERY = "SELECT g.text FROM FilmGenre fg JOIN Genre g ON fg.genre=g.id WHERE fg.film=?"
        return *( tuple( self.get( QUERY, film_id)) for film_id in film_ids ),

    def genre_order( self, mode='text'):
        TEXT_QUERY = "SELECT text FROM GenreOrdering ORDER BY idx ASC"
        ID_QUERY   = "SELECT id   FROM GenreOrdering ORDER BY idx ASC"
        if mode == 'text':
            query = TEXT_QUERY
        elif mode == 'id':
            query = ID_QUERY
        else:
            raise Unknown_Genre_Order_Mode( mode)
        return self.get( query)
