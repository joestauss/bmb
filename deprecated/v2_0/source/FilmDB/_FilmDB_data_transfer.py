from bmb.source.FilmDB._standard_import           import *

import shutil

TABLES_TO_DELETE = [
    "Alias",
    "Genre",
    "FilmGenre",
    "Tag",
    "FilmTag",
    "FilmLanguage",
    "FilmInfoset",
    "FilmDescription",
    "TMDbRecommendation",
    "JustWatchURL",
    "JustWatchState",
    "JustWatchLog",
]

class _FilmDB_data_transfer:
    def _empty_copy( self, copy_location):
        shutil.copyfile( self.file, copy_location)
        db = self.__class__( copy_location)
        for table in TABLES_TO_DELETE:
            db.set( f"DELETE FROM {table}")
            db.set( "DELETE FROM sqlite_sequence WHERE name=?", table)
        return db

    def save_tags(self, tag_file):
        db = self._empty_copy( tag_file)
        for title, year, tag_text, added in self.get( Query.PREPARE_TAGS_FOR_EXPORT):
            db.tag(
                db.Film( title, year, lookup=True),
                db.Tag( tag_text),
                added=added )

    def load_tags( self, tag_file):
        db = self.__class__( tag_file)
        for title, year, tag_text, added in db.get( Query.PREPARE_TAGS_FOR_EXPORT):
            self.tag(
                self.Film( title, year, lookup=True),
                self.Tag( tag_text),
                added=added )
