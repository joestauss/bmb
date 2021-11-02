from bmb.v2.source.FilmDB._standard_import          import *

class _FilmDB_web_data_ingestion:
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
