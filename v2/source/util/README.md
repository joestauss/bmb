# `util` Utilities

There are three files in the `util`:

1. `enums.py` - As a performance hack, some database values are mirrored in hard-coded `FlimDB` variables.
2. `exceptions.py` - All the exceptions used anywhere.
3. `sql_queries.py` - These kept accessible by a `Query` class.

Of these, `exceptions.py` and `sql_queries.py` will be just added to as needed, so only `enums.py` needs to be unit tested.