from bmb.test.test_util import *
from bmb.source.util.enums import AliasType, Infoset
from collections import namedtuple

@pytest.fixture
def test_cases():
    Test = namedtuple( 'Test', 'enum table')
    return (
        Test( AliasType, 'AliasType'),
        Test( Infoset  , 'Infoset'  ) )

def test_enum_values( TestDB, test_cases):
    for test in test_cases:
        for key, value in test.enum.__members__.items():
            database_text = key.lower().replace( '_', ' ')
            assert TestDB.select_one( 'id', test.table, text=database_text) == value.value
    TestDB.destroy()

def test_enum_completeness( TestDB, test_cases):
    for test in test_cases:
        assert TestDB.select_one( 'COUNT(*)', test.table) == len( test.enum)
    TestDB.destroy()
