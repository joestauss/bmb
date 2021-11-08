from bmb.source.FilmDB       import FilmDB
from pathlib                    import Path

FilmDB().load_tags( Path( __file__).parent / "Saved Tags.db")
