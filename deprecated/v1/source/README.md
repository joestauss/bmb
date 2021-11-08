# `source` Source Code

The source code is split among four folders:

1. `databases` contains the `SQLiteDB` class, plus subclasses for each of the three B-Movie Buddy databases: `IngestionDB`, `ProcessingDB`, and `WarehouseDB`.
2. `util` has utility code.  Custom error statements are defined in `exceptions.py` and a custom `BeautifulSoup` initializer can be found in `safe_soup.py`.
3. `webscraping` is incomplete; I'm not sure how much webscraping code I want to release, so for now only `tmdb_access.py` is provided, which uses the API provided by TMDb.
4. `resources`, which contains my SQLite databases, is *gitignore*'d and should not be visible. 

## About `standard_import.py`

Most of my python files begin with `from bmb.source.standard_import import *`, which adds to the namespace any objects, functions, and constants that I find myself coming back to as I code.  I prefer this method to starting each script with a lot of boilerplate `import` statements.

