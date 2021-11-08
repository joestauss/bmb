# B-Movie Buddy V2 API Definition & TDD

One of the development goals for the next version `bmb` is to use Test-driven Development, so I am combining the API definition with the test requirements in a single document.

All test cases are designed to pass on a carefully arranged test database called`Test.db`.  In order to prevent successive tests from interfering with each other, a unique temporary copy of the database is used for each test.  The test database contains the following films:

1. *The Terminator (1984)* is used primarily for `test_fuzzy_film_alias.py`
   - The alias *Terminator (1984)* should be in the test database.
   - The following aliases should not be in the test database: *tHe terminatoR (1984)*, *The Terminator (1983)*, *Terminator 1 (1984)*
   - The sequel *Terminator 2: Judgment Day (1991)* should not be in the test database.
   
2. *Four Films from the 1960's* are used in `test_filmset_slilcing.py`.  Each is given a few generic tags.
   1. *The Hustler (1960)*: tags are `A` and `B`
   2. *The Last Man on Earth (1964)*: tags are `A` and `C`
   3. *Dr. Terror's House of Horrors (1965)*: tags are `B` and `C`
   4. *The Thomas Crown Affair (1968)*: tags are `A`, `B`, and `C`

In the lists below describing particular test cases, a <u>**Bold and Underlined Test Name**</u> has been implemented and an <u>*Italicized and Underlined Test Name*</u> represents future functionality.



## Fuzzy Film Aliases: `FilmDB.Alias` & `FilmDB.Film`

B-Movie Buddy Version 2 needs to be able to handle movie names that are only approximately correct.  This is both a convenience - since, for example, you might only know _Terminator 2: Judgment Day_ as _Terminator 2_ - and necessary for films that are known by multiple titles or have an ambiguous year stemming from an unconventional release schedule.  The first _Paranormal Activity_ is a good example of this- it was first shown at film festivals in 2007 before being opened for general viewing in 2009, and I've seen both dates used for the film by different sources.

Film identification numbers are obtained through a call to `FilmDB.Film( title, year)`, which obscures from a user the mechanics behind interpreting the `title` and `year` they provide, most notably the fact that there is no Film table in the database.  An individual title-year combination is referred to as an "Alias".  The identification number for the alias is returned by `FilmDB.Alias( title, year)`.  An alias has an _AliasType_, which can be `canonical`, `alternate`, `not a film`, or  `search failure`.

1. <u>**Canonical and alternate aliases return the same Film ID.**</u>
   	`test_canonical_alias`
   	`test_alternate_canonical_alias_equality`
2. **<u>If the</u> `lookup` <u>keyword is</u> `True`, <u>then search for the new alias and add it to the database.</u>**
3. **<u>Simple fuzzy alias search.</u>**
   	`test_wrong_capitalization_of_existing_alias`
   	`test_slightly_incorrect_year_of_existing_alias`
4. <u>*Advanced fuzzy alias search*.</u>
5. *`FilmDB.Film` <u>should throw a custom error for "search failure" or "not a film" aliases.</u>*



## Filmset Slicing: `FilmDB.Filmset`

One of the most common operations in B-Movie Buddy is selecting all of the films that meet a certain criteria.  This is accomplished through the **Filmset method**, `FilmDB.Filmset( self, **conditions)`, which returns a list of film identification numbers.

There are three keywords that can be used simultaneously as `conditions`; `year` can be either an integer or a `(year_min, year_max)` range tuple, and `genre` and `tag` both accept either a string (to require only a single genre or tag) or an object in _propositional syntax_, defined below.

1. __Lists `[]` are used as a a logical "OR".__
2. __Tuples `()` are used as a logical "AND".__
3. __A set `{a, b, ...}` is interpreted as "NOT `a` AND NOT `b` AND `...`".__  In most cases, I'll just be using `{}` for a "NOT" operation but, since a set in Python cannot contain a list, it would have been impossible to represent $\lnot(a\lor b)$. Logically, $\lnot(a\lor b)$ is equivalent to $\lnot a\land\lnot b$, so `{}` can just expand to accommodate a multiple negation.

As an example, suppose that you are looking for a light-hearted movie to watch.  You prefer a horror-comedy or a romance that isn't too dramatic, and definitely no westerns.  These categories are represented logically as:
$$
\left[ ( Horror \land Comedy) \lor (Romance \land \lnot Drama) \right] \land \lnot Western
$$
In propositional syntax, this is expressible as `([('Horror', 'Comedy'), ('Romance', {'Drama'})], { 'Western'})`.

1. **<u>Test individual conditions in isolation.</u>**
   	`test_year`
   	`test_genre`
   	`test_tags`

2. **<u>Test the use of multiple conditions simultaneously.</u>**
   	`test_multiple_conditions_1`
   	`test_multiple_conditions_2`
   	`test_multiple_conditions_3`

3. <u>*Slice an existing filmset by providing the function with an optional arg.*</u>

4. <u>*Return a custom class with some useful methods (a Flimset) instead of the current set of Film IDs.*</u>

   

## Convenience Enums

`FilmDB` has several class variables that mirror the database and are used to keep some values immediately accessible.  This access pattern is intended for status-codes and other small groups of values that rarely, if ever, change and keeps me from having to query the database every time I need them.  This helps with both convenience and readability; `FilmDB.AliasType.SEARCH_FAILURE` is clear enough to use as a function parameter, especially considering that the equivalent database call could easily be twice as long.

The enums to be tested are declared in the `test_cases` fixture.  There are two test functions, both of which contain a loop that calls each test in `test_cases`.  If both tests pass, then the table and the enum should be exactly the same.

1. **<u>Check the value of each enum against the equivalent database record.</u>**
   	`test_enum_values`
2.  **<u>Compare lengths of the enum and equivalent database table.</u>**
      	`test_enum_completeness`



## Webscraping

I am not providing the test suite for my data ingestion engine at this time.
