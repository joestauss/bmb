from bmb.v2.source.FilmDB import FilmDB
from tqdm import tqdm

db = FilmDB()

for film_id in tqdm( db.filmset()):
    db.get_infoset( film_id, db.Infoset.BASIC_INFO)
    db.get_infoset( film_id, db.Infoset.TMDB_RECOMMENDATIONS)
