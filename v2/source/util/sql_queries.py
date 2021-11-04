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

    PREPARE_TAGS_FOR_EXPORT = """
        SELECT a.title, a.year, t.text, t.added
        FROM FilmTag ft
            JOIN Alias a on ft.film = a.film
            JOIN Tag   t on ft.tag  = t.id
        WHERE
            a.type = 1
    """

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

    SELECT_CURRENTLY_STREAMABLE_AT_STREAMER = """
        SELECT url FROM JustWatchState
        WHERE streamer=? AND REMOVED IS NULL
    """

    SELECT_STREAMER_ID = """
        SELECT id
        FROM Streamer
        WHERE LOWER(name)=LOWER(?)
    """

    SIMILAR_ALIAS = """
        SELECT id, film FROM Alias
        WHERE LOWER( title) = LOWER( ?)
        AND year - ? BETWEEN -2 AND 2; """

    UNKNOWN_ALIASES = "SELECT title, year FROM Alias WHERE type IS NULL"

    UPDATE_CONFIRM_TIME_FOR_JWURL_AT_STREAMER = """
        UPDATE JustWatchState
        SET    confirmed=?
        WHERE  url=?
        AND    streamer=?
    """

    UPDATE_REMOVE_TIME_FOR_JWURL_AT_STREAMER = """
        UPDATE JustWatchState
        SET    removed=?
        WHERE  url=?
        AND    streamer=?
    """

    UPDATE_TIME_OF_FILM_TAG = "UPDATE FilmTag SET added=? WHERE film=? AND tag=?"
