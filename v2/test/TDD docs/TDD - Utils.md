# API Definition & Test Coverage: Utilities

**Test-driven Development for `bmb` version 2.**

There are three files in the utilities directory `util`:

1. `enums.py` - As a performance hack, some database values are mirrored in hard-coded `FlimDB` variables.
2. `exceptions.py` - All the exceptions used anywhere.
3. `sql_queries.py` - These kept accessible by a `Query` class.

Of these, `exceptions.py` and `sql_queries.py` will be just added to as needed, so only `enums.py` needs to be tested.

## Enums `test_enums.py`

As mentioned above, `enums.py` only exists to keep a few values immediately accessible.  It is intended to contain, for example, status-codes that I don't want to have to write a database call for.  This is mostly for convenience and readability; `FilmDB.AliasType.SEARCH_FAILURE` is clear enough to use as a function parameter, especially considering that the equivalent database call could easily be twice as long.

The enums to be tested are declared in the `test_cases` fixture.  There are two test functions, both of which contain a loop that calls each test in `test_cases`:

1. `test_enum_values` checks each enum's value against the equivalent database ID.
2. `test_enum_completeness` compares lengths of the enum and equivalent database table.

