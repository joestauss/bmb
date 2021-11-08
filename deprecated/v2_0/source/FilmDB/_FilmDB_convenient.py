from bmb.source.FilmDB._standard_import           import *

class _FilmDB_convenient:
    @property
    def watchlist( self):
        return self.get( Query.WATCHLIST)

    @property
    def watchlist_details( self):
        return self.get( Query.WATCHLIST_DETAILS)

    @property
    def unknown_aliases( self):
        return self.get( Query.UNKNOWN_ALIASES)

    @property
    def unknown_films( self):
        return self.get( Query.SELECT_FILMS_WITHOUT_INFOSET, self.Infoset.BASIC_INFO)

    ############################################################################
    # Enums                                                                    #
    #   These Enums contain database constants.                                #
    #   They mirror tables in the database and are verified correct in testing.#
    ############################################################################
    AliasType = AliasType   # Mirrors "AliasType"
    Infoset   = Infoset     # Mirrors "Infoset"
