from bmb.v2.source.FilmDB import FilmDB
from bmb import PATH_TO_V2_TEST_DB

def _update():
    db = FilmDB( PATH_TO_V2_TEST_DB)

    for title, year in db.unknown_aliases:
        db.Film( title, year, lookup=True)

    for film_id in db.unknown_films:
        db.get_infoset( film_id, db.Infoset.BASIC_INFO )

if __name__ == "__main__":
    _update()
