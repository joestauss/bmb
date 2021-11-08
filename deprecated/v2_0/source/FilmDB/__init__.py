from bmb                                                import BMBv2_RESOURCE_DIR
from bmb.source.FilmDB._FilmDB_basic_film_attributes import _FilmDB_basic_film_attributes
from bmb.source.FilmDB._FilmDB_convenient            import _FilmDB_convenient
from bmb.source.FilmDB._FilmDB_data_transfer         import _FilmDB_data_transfer
from bmb.source.FilmDB._FilmDB_filmset_slicing       import _FilmDB_filmset_slicing
from bmb.source.FilmDB._FilmDB_web_data_ingestion    import _FilmDB_web_data_ingestion
from bmb.source.FilmDB._FilmDB_streaming_status      import _FilmDB_streaming_status
from bmb.source.FilmDB._standard_import              import *
from bmb.source.SQLiteDB                             import SQLiteDB

class FilmDB(
    _FilmDB_basic_film_attributes,
    _FilmDB_convenient,
    _FilmDB_data_transfer,
    _FilmDB_filmset_slicing,
    _FilmDB_streaming_status,
    _FilmDB_web_data_ingestion,
    SQLiteDB
    ):

    DEFAULT_DB = BMBv2_RESOURCE_DIR / 'Movies.db'
