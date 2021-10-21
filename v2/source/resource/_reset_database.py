from bmb import PATH_TO_V2_TEST_DB, ProcessingDB
from bmb.gitignored import seed_films
import shutil
from tqdm import tqdm
from pathlib import Path
from bmb.v2.source.FilmDB import FilmDB

DATABASE_FILE = Path( __file__).parent / "Movies.db"

TABLES_TO_DELETE = [
    "Alias",
    "Genre",
    "FilmGenre",
    "Tag",
    "FilmTag",
    "FilmLanguage",
    "FilmInfoset",
    "FilmDescription"
]

def _reset():
#    shutil.copyfile( PATH_TO_V2_TEST_DB, DATABASE_FILE)
    db = FilmDB()

#    for table in TABLES_TO_DELETE:
#        db.set( f"DELETE FROM {table}")
#        db.set( "DELETE FROM sqlite_sequence WHERE name=?", table)

#    for film in seed_films:
#        db.Film( film.title, film.year, lookup=True)

    for title, year in tqdm(ProcessingDB().select( 'title', 'year', 'OldRating', rating=4)):
        db.tag(
            db.Film( title, year, lookup=True),
            db.Tag( "watched") )

    for film in tqdm(db.unknown_films):
        db.get_infoset( film, db.Infoset.BASIC_INFO)

if __name__ == '__main__':
    _reset()
