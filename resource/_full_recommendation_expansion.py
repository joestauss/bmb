from bmb.source.FilmDB import FilmDB
from tqdm import tqdm

db      = FilmDB()
films   = db.get( "SELECT DISTINCT film FROM Alias ORDER BY RANDOM()")

for film_id in tqdm( films[:300] ):
    db.get_infoset( film_id, db.Infoset.BASIC_INFO)
    db.get_infoset( film_id, db.Infoset.TMDB_RECOMMENDATIONS)

db.get_basic_info_for_all( VERBOSE=True)
