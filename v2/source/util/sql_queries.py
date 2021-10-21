from bmb.v2.source.util.enums import Enum_StrIsValue

class Query( Enum_StrIsValue):

    ASSIGN_FILM_TO_ALIAS = """
        UPDATE Alias
        SET film=?
        WHERE id=?   """

    ASSIGN_TYPE_TO_ALIAS = """
        UPDATE Alias
        SET type=?
        WHERE id=?"""

    SELECT_FILMS_WITHOUT_INFOSET = """
        SELECT DISTINCT a.film
            FROM Alias a
            LEFT JOIN FilmInfoset fi ON a.film = fi.film AND fi.infoset=?
        WHERE fi.infoset IS NULL
    """

    # Hard-coded infoset number
    SELECT_NOT_GENRE = """
        SELECT film
        FROM FilmInfoset
        WHERE infoset= 1 AND film NOT IN (
            SELECT film FROM FilmGenre WHERE genre=?
        )
    """

    SELECT_NOT_TAG = """
        SELECT film
        FROM FilmInfoset
        WHERE film NOT IN (
            SELECT film FROM FilmTag WHERE tag=?
        )
    """

    SIMILAR_ALIAS = """
        SELECT id, film FROM Alias
        WHERE LOWER( title) = LOWER( ?)
        AND year - ? BETWEEN -2 AND 2; """

    UNKNOWN_ALIASES = "SELECT title, year FROM Alias WHERE type IS NULL"

    UPDATE_TIME_OF_FILM_TAG = "UPDATE FilmTag SET added=? WHERE film=? AND tag=?"
