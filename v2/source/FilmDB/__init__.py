from bmb                                                import BMBv2_RESOURCE_DIR
from bmb.v2.source.FilmDB._FilmDB_basic_film_attributes import _FilmDB_basic_film_attributes
from bmb.v2.source.FilmDB._FilmDB_filmset_slicing       import _FilmDB_filmset_slicing
from bmb.v2.source.FilmDB._FilmDB_web_data_ingestion    import _FilmDB_web_data_ingestion
from bmb.v2.source.FilmDB._FilmDB_streaming_status      import _FilmDB_streaming_status
from bmb.v2.source.FilmDB._standard_import              import *
from bmb.v2.source.SQLiteDB                             import SQLiteDB

class FilmDB(
    _FilmDB_basic_film_attributes,
    _FilmDB_filmset_slicing,
    _FilmDB_streaming_status,
    _FilmDB_web_data_ingestion,
    SQLiteDB
    ):

    DEFAULT_DB = BMBv2_RESOURCE_DIR / 'Movies.db'

    ############################################################################
    # Enums                                                                    #
    #   These Enums contain database constants.                                #
    #   They mirror tables in the database and are verified correct in testing.#
    ############################################################################
    AliasType = AliasType   # Mirrors "AliasType"
    Infoset   = Infoset     # Mirrors "Infoset"
