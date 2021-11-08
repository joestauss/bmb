from bmb.source.standard_import import *

class WarehouseDB( SQLiteDB):
    DEFAULT_DB = RESOURCE_DIRECTORY / "Warehouse.db"


    id_tables = {
        "Film"     : ( "title" ,  "year" ),
        "Genre"    : ( "text", ),
        "Credit"   : ( "name", ),
        "Tag"      : ( "text", ),
        "Status"   : ( "text", )
    }

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

    def load_from_processing( self, processing, **kw):
        processing_ids = processing.select( 'id', 'Film', status=processing.Status( 'warehouse') )
        for processing_id in jupyter_aware_tqdm( processing_ids, **kw):

            #   Create ID
            local_id = self.Film( *processing.select_one( 'title', 'year', 'Film', id=processing_id))

            #   Description
            if not self.select_one( 'FilmDescription', film=local_id):
                self.insert( 'FilmDescription',
                    film=local_id,
                    text=processing.select_one( 'text', 'FilmDescription', film=processing_id) )

            #   Genres
            query = "SELECT g.text FROM FilmGenre fg JOIN Genre g on fg.genre=g.id WHERE fg.film=?"
            for genre_name in processing.get( query, processing_id):
                genre_id = self.Genre( genre_name)
                if not self.select_one( "FilmGenre", film=local_id, genre=genre_id):
                    self.insert( "FilmGenre", film=local_id, genre=genre_id)
