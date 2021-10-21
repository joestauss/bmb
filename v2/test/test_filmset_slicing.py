from bmb.v2.test.test_util import *

def test_year( TestDB):
    known_ids = [2, 3, 4, 5]
    found_ids = TestDB.filmset( year=(1960, 1969))
    assert( all((film_id in found_ids for film_id in known_ids)))
    assert( len( known_ids) == len( found_ids))

def test_genre( TestDB):
    test_cases = [
        ("Horror", (3, 4) ),
        (("Horror", {'Science Fiction'}), (4, ) ), # Horror and not SF
        (['Drama', 'Science Fiction'], (1, 2, 3, 5) ), # Drama OR SF
        ({('Crime', 'Romance')}, (1, 2, 3, 4)),    # not (Crime and romance)
        ({'Crime', 'Horror'}, (1, 2))              # not crime and not horror
    ]
    for genres, result in test_cases:
        assert tuple( sorted( TestDB.filmset( genre=genres))) == result

def test_tags( TestDB):
    test_cases = [
        ( 'A'                       , (2, 3, 5) ), # A
        ( ('A', 'B')                , (2, 5 )),    # A and B
        ( ('A', {'B'})              , (3, )),      # A and not B
        ( [('A', 'B', 'C'), ('B', {'C'})], (2, 5))   # (A and B) or (B and not C)
    ]
    for tags, result in test_cases:
        assert tuple( sorted( TestDB.filmset( tag=tags))) == result

def test_multiple_conditions_1( TestDB):
    known_ids = (2, 3, 4)
    found_ids = TestDB.filmset( year=(1960, 1969), genre={ 'Crime'} )
    assert tuple( sorted( found_ids)) == known_ids

def test_multiple_conditions_2( TestDB):
    known_ids = (4, 5)
    found_ids = TestDB.filmset( year=(1960, 1969), genre=['Horror', 'Crime'],  tag=('B', 'C') )
    assert tuple( sorted( found_ids)) == known_ids

def test_multiple_conditions_3( TestDB):
    known_ids = (3, )
    found_ids = TestDB.filmset( year=(1960, 1969), genre='Horror',  tag='A' )
    assert tuple( sorted( found_ids)) == known_ids
