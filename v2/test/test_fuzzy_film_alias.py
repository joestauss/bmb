from bmb.v2.test.test_util import *
from collections import namedtuple

ENABLE_WEB_TESTS = True

def test_correctly_called_film( TestDB):
    assert TestDB.Film( "The Terminator", 1984) == TestDB.select_one( "film", "Alias", title="The Terminator", year=1984)
    TestDB.destroy()

def test_known_alias_wrong_title( TestDB):
    assert TestDB.Film( "The Terminator", 1984) == TestDB.Film( "Terminator", 1984)
    TestDB.destroy()

def test_wrong_capitalization_not_an_alias( TestDB):
    initial_alias_count = TestDB.select_one( "COUNT(*)", "Alias")
    assert TestDB.Film( "tHe terminatoR", 1984) == TestDB.Film( "Terminator", 1984)
    assert TestDB.AliasType.ALTERNATE.value == TestDB.select_one( "type", "Alias", title="tHe terminatoR", year=1984)
    assert initial_alias_count < TestDB.select_one( "COUNT(*)", "Alias")
    TestDB.destroy()

def test_wrong_year_not_an_alias( TestDB):
    initial_alias_count = TestDB.select_one( "COUNT(*)", "Alias")
    assert TestDB.Film( "The Terminator", 1984) == TestDB.Film( "The Terminator", 1983)
    assert TestDB.AliasType.ALTERNATE.value == TestDB.select_one( "type", "Alias", title="The Terminator", year=1983)
    assert initial_alias_count < TestDB.select_one( "COUNT(*)", "Alias")
    TestDB.destroy()

def test_web_lookup_alias( TestDB):
    if ENABLE_WEB_TESTS:
        assert TestDB.Film( "Terminator 1", 1984, lookup=True) == TestDB.Film( "The Terminator", 1984)
    else:
        assert True
    TestDB.destroy()

def test_web_lookup_new_film( TestDB):
    main_title = "Terminator 2: Judgment Day"
    alt_title  = "Terminator 2"
    if ENABLE_WEB_TESTS:
        assert TestDB.Film( alt_title, 1991, lookup=True) == TestDB.Film( main_title, 1991)
        assert TestDB.AliasType.CANONICAL.value == TestDB.select_one( "type", "Alias", title=main_title, year=1991)
        assert TestDB.AliasType.ALTERNATE.value == TestDB.select_one( "type", "Alias", title=alt_title, year=1991)
    else:
        assert True
    TestDB.destroy()
