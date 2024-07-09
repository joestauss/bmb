from bmb.source.util.enums import Enum_StrIsValue

class Query( Enum_StrIsValue):

    ASSIGN_FILM_TO_ALIAS = """
        UPDATE Alias
        SET film=?
        WHERE id=?   """

    ASSIGN_TYPE_TO_ALIAS = """
        UPDATE Alias
        SET type=?
        WHERE id=?"""

    FILM_ID_TO_GENRES = """
        SELECT  Genre.text
        FROM    FilmGenre
        JOIN    Genre ON FilmGenre.genre=Genre.id
        WHERE   FilmGenre.film=?
    """

    FILM_ID_TO_TAGS = """
        SELECT  Tag.text
        FROM    FilmTag
        JOIN    Tag ON FilmTag.tag=Tag.id
        WHERE   FilmTag.film=?
    """

    GET_STREAMABLE_FILMS = """
        SELECT  u.film
        FROM    JustWatchState s
        JOIN    JustWatchURL u ON  s.url = u.id
        WHERE   s.removed IS NULL
    """

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
        WHERE fi.infoset IS NULL AND a.type=1
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

    UNTAG_FILM = "DELETE FROM FilmTag WHERE film=? AND tag=?"

    UNTAGGED_FILMS = """
        SELECT Alias.film
        FROM Alias
            LEFT JOIN FilmTag ON FilmTag.film = Alias.film
        WHERE FilmTag.film IS NULL
        AND Alias.type=1
    """

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

    WATCHLIST_DETAILS = """
        SELECT
            a.title,
            a.year,
            GROUP_CONCAT( g.text ),
            fd.description

        FROM FilmTag ft
            JOIN Tag   t            ON ft.tag  = t.id
            JOIN Alias a            ON ft.film = a.film
            JOIN FilmDescription fd ON ft.film = fd.film
            JOIN FilmGenre       fg ON ft.film = fg.film
            JOIN Genre g            ON fg.genre = g.id

        WHERE t.text = "watchlist"
            AND a.type = 1

        GROUP BY
            ft.film

        ORDER BY
            a.year
    """

    WATCHLIST = """
        SELECT ft.film
        FROM   FilmTag ft
        JOIN   Tag t ON ft.tag  = t.id
        WHERE  t.text='watchlist'
    """
