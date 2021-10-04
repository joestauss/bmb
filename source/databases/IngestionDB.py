from bmb.source.standard_import import *
from bmb.source.webscraping     import films_available_to_stream

class IngestionDB( SQLiteDB):
    DEFAULT_DB = RESOURCE_DIRECTORY / "Web Ingestion.db"

    id_tables = {
        "Streamer"      : ( "name",        ),
        "JustwatchFilm" : ( "url" ,        ),
        "TMDbFilm"      : ( 'title', 'year') }

    def JustwatchFilm( self, url):
        FILM_TABLE = "JustwatchFilm"
        if not self.id( FILM_TABLE, url):
            self.insert( FILM_TABLE, url=url, added=self.date_str )
        return self.id( FILM_TABLE, url)

    def Streamer_key( self, streamer_name):
        STREAMER_TABLE = "Streamer"
        if not self.select_one( STREAMER_TABLE, name=streamer_name):
            raise Unknown_Streaming_Service( streamer_name )
        return self.select_one( 'key', STREAMER_TABLE, name=streamer_name)

    def confirm_active_stream( self, streamer_id, film_id, date_str):
        if not self.get( "SELECT * FROM JustwatchState WHERE streamer=? AND film=? AND removed IS NULL", streamer_id, film_id):
            self.insert( "JustwatchState", streamer=streamer_id, film=film_id, added=date_str )
        self.set( "UPDATE JustwatchState SET confirmed=? WHERE streamer=? AND film=? AND removed IS NULL", date_str, streamer_id, film_id)

    def all_title_year_combinations( self):
        return self.get( query.JUSTWATCH_FILMS)

    def identify_all_JustwatchFilm_URLs( self, **kw):
        unknown_urls = self.get( "SELECT url from JustWatchFilm WHERE title is Null")
        for url in jupyter_aware_tqdm( unknown_urls, **kw):
            soup = safe_soup( url)
            tb   = soup.find( class_='title-block')
            if not tb:
                raise Justwatch_Webscraping_Error( utl)
            title, year = tb.find( 'h1').text.strip(), int( tb.find( class_='text-muted').text.split( '(')[1].split(')')[0])
            self.set( "UPDATE JustwatchFilm SET title=?, year=? WHERE url=?", title, year, url)
