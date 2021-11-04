#   watchlist

tags_to_apply = [
    # (
    #     "",
    #     ,
    #     ""
    # ),
    (
        "I'm with Lucy",
        2002,
        "watchlist"
    ),
    (
        "Hudson Hawk",
        1991,
        "watchlist"
    ),
    (
        "Terminal Exposure",
        1987,
        "watchlist"
    ),
    (
        "Pumpkin",
        2002,
        "watchlist"
    ),
    (
        "Silver City",
        2004,
        "watchlist"
    ),
    (
        "Stinger",
        2005,
        "watchlist"
    ),
    (
        "Crush",
        2001,
        "watchlist"
    ),
    (
        "Double Whammy",
        2001,
        "watchlist"
    ),
]

if __name__ == "__main__":
    from bmb.v2.source.FilmDB       import FilmDB
    db = FilmDB()

    for title, year, tag in tags_to_apply:
        db.tag(
            db.Film( title, year, lookup=True),
            db.Tag( tag)  )
