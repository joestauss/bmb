from bmb.source.FilmDB._standard_import           import *

class _FilmDB_filmset_slicing:
    def filmset( self, year=None, genre=None, tag=None, streamable=None):
        if not year:
            return_set = set(self.select( "DISTINCT film", "Alias"))
        elif isinstance( year, tuple) and len( year)== 2:
            return_set = set(self.get( "SELECT DISTINCT film FROM Alias WHERE year BETWEEN ? AND ?;", year[0], year[1]))
        else:
            raise ValueError( f"Illegal 'year' value: {year}")

        if genre:
            if isinstance( genre, str):
                passed_genre = set(self.get( "SELECT film FROM FilmGenre WHERE genre=?", self.Genre( genre)))
            elif isinstance( genre, tuple):
                passed_genre = return_set
                for g in genre:
                    passed_genre &= self.filmset( year=year, genre=g)
            elif isinstance( genre, set):
                if len( genre) == 1:
                    obj = genre.pop()
                    if isinstance( obj, str):
                        passed_genre = set(self.get( Query.SELECT_NOT_GENRE, self.Genre( obj)))
                    if isinstance( obj, tuple):
                        passed_genre = set()
                        for sub in obj:
                            passed_genre |= self.filmset( year=year, genre={sub})
                else:
                    passed_genre = return_set
                    for g in genre:
                        passed_genre &= self.filmset( year=year, genre={g})
            elif isinstance( genre, list):
                passed_genre = set()
                for g in genre:
                    passed_genre |= self.filmset( year=year, genre=g)
            else:
                raise ValueError( f"Illegal 'genre' value: {genre}")
            return_set &= passed_genre

        if tag:
            if isinstance( tag, str):
                passed_tag = set(self.get( "SELECT film FROM FilmTag WHERE tag=?", self.Tag( tag)))
            elif isinstance( tag, tuple):
                passed_tag = return_set
                for t in tag:
                    passed_tag &= self.filmset( year=year, genre=genre, tag=t)
            elif isinstance( tag, set):
                if len( tag) == 1:
                    obj = tag.pop()
                    if isinstance( obj, str):
                        passed_tag = set(self.get( Query.SELECT_NOT_TAG, self.Tag( obj)))
                    if isinstance( obj, tuple):
                        passed_tag = set()
                        for sub in obj:
                            passed_tag |= self.filmset( year=year, genre=genre, tag={sub})
                else:
                    passed_tag = return_set
                    for t in tag:
                        passed_tag &= self.filmset( year=year, genre=genre, tag={t})
            elif isinstance( tag, list):
                passed_tag = set()
                for t in tag:
                    passed_tag |= self.filmset( year=year, genre=genre, tag=t)
            else:
                raise ValueError( f"Illegal 'tag' value: {tag}")
            return_set &= passed_tag

        if streamable:
            if streamable:
                return_set &= set( self.get( Query.GET_STREAMABLE_FILMS))


        return_set = {item for item in return_set if item is not None}
        return return_set
