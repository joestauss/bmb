from enum import Enum

class Enum_StrIsValue( Enum):
    def __str__( self): return str( self.value)

class AliasType( Enum_StrIsValue):
    CANONICAL      = 1
    ALTERNATE      = 2
    NOT_A_FILM     = 3
    SEARCH_FAILURE = 4

class Infoset( Enum_StrIsValue):
    BASIC_INFO           = 1
    TMDB_RECOMMENDATIONS = 2
