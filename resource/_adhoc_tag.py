#   watchlist

tags_to_apply = [
    # (
    #     "",       # title
    #     ,         # year
    #     ""        # tag
    # ),
]

if __name__ == "__main__":
    from bmb.source.FilmDB       import FilmDB
    db = FilmDB()

    for title, year, tag in tags_to_apply:
        db.tag(
            db.Film( title, year, lookup=True),
            db.Tag( tag)  )
