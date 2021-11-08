from bmb.test.test_util import *
from collections import namedtuple

ENABLE_WEB_TESTS = True

def test_IMDb_list_with_common_films( TestDB):
    known_films = {('Scarface', 1983), ("E.T. the Extra-Terrestrial", 1982), ("Raising Arizona", 1987 ), ("Where the Buffalo Roam", 1980)}
        # These represent the first and last films from both pages of the lsit.
    test_tag    = 'IMDb list ingestion test data'
    TestDB.ingest_IMDb_list( "ls006692819", tag=test_tag)
    ingested_from_list = TestDB.filmset( tag=test_tag)

    assert len(ingested_from_list) > 0
    for title, year in known_films:
        assert TestDB.Film( title, year, lookup=True) in ingested_from_list
