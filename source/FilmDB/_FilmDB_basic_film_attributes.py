from bmb.source.FilmDB._standard_import           import *

class _FilmDB_basic_film_attributes:
    def Film( self, title, year, lookup=False):
        alias_id = self.Alias( title, year)
        film_id  = self.select_one( "film", "Alias", id=alias_id)
        if not film_id:
            if lookup:
                try:
                    if alias_id is None:
                        raise Exception( f"Something is wrong with {title} ({year})")
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

    def tag( self, film_id, tag_id, added=None):
        add_time = added if added else self.now
        if self.select_one( '*', 'FilmTag', film=film_id, tag=tag_id):
            self.set( Query.UPDATE_TIME_OF_FILM_TAG, add_time, film_id, tag_id)
        else:
            self.insert( 'FilmTag', film=film_id, tag=tag_id, added=add_time)

    def untag( self, film_id, tag_id):
        self.set( Query.UNTAG_FILM, film_id, tag_id)

    def film_summary( self, film_id):
        title, year = self.select_one( 'title', 'year', 'Alias', film=film_id, type=self.AliasType.CANONICAL)
        genres = self.get( Query.FILM_ID_TO_GENRES, film_id)
        tags   = self.get( Query.FILM_ID_TO_TAGS  , film_id)
        desc   = self.select_one( 'description', 'FilmDescription', film=film_id)

        lines = [ f"FILM #{film_id}: {title} ({year}) " ]
        lines.append( "-"*len( lines[0]))
        if genres:
            lines.append( "   " + " / ".join( genres))
        if desc:
            lines.append( "   " + desc)
        for tag in tags:
            lines.append( f"   [ {tag.upper()} ]")
        return "\n".join( lines)
