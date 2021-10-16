from bmb.v2.source.SQLiteDB import SQLiteDB
from bmb.v2.source.util.enums import AliasType, Infoset
from bmb.v2.source.util.exceptions import *
from bmb.v2.source.util.sql_queries import Query
from bmb.v2.source.webscraping.tmdb_api import get_tmdb_movie

class FilmDB( SQLiteDB):

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
    ############################################################################
    def Film( self, title, year, lookup=False):
        alias_id = self.Alias( title, year)
        film_id  = self.select_one( "film", "Alias", id=alias_id)
        if not film_id:
            if lookup:
                self._identify_alias( alias_id)
                film_id = self.select_one( "film", "Alias", id=alias_id)
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
            new_film_id = maximum + 1 if maximum else 0
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
            if film != similar_aliases[0][0]:
                raise MultipleSimilarFilms( f"title={title}, year={year}")
        return film if similar_aliases else None
