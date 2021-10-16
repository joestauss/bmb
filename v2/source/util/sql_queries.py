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

    SIMILAR_ALIAS = """
        SELECT id, film FROM Alias
        WHERE LOWER( title) = LOWER( ?)
        AND year - ? BETWEEN -2 AND 2; """
