from bmb                    import PATH_TO_V2_TEST_DB
from bmb.v2.source.FilmDB   import FilmDB
from pathlib                import Path

DATABASE_FILE = Path( __file__).parent / "Movies.db"

if __name__ == '__main__':
    FilmDB( PATH_TO_V2_TEST_DB)._empty_copy( DATABASE_FILE)
