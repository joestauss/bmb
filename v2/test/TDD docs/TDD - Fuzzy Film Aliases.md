# API Definition & Test Coverage: Fuzzy Film Aliases

One of the goals for B-Movie Buddy Version 2 is to be able to handle movie names that are only approximately correct.  This is both a convenience - since, for example, you might only know _Terminator 2: Judgment Day_ as _Terminator 2_ - and a necessity, since the correct year for some films is ambiguous due to an unconventional release schedule.  The first _Paranormal Activity_ is a good example of this- it was first shown at film festivals in 2007 before being opened for general viewing in 2009, and I've seen both dates used for the film.

An individual title-year combination is referred to as a film's "Alias".  An alias has an _AliasType_:

1. `canonical`: The most correct way to refer to a film, such as _Terminator 2: Judgment Day_.
2. `alternate`: Secondary monikers, such as _Terminator 2_.
3. `not a film`
4. `search failure`

Film identification numbers are obtained through a call to `FilmDB.Film( title, year)`, which obscures from a user the mechanics behind interpreting the `title` and `year` they provide, most notably the fact that there is no actual Film table.  The identification number for the alias itself can be obtained through `FilmDB.Alias( title, year)`.

## `FilmDB.Film( title, year)`

1. If `title` (`year`) is a known alias for a film, then return that film's ID.  *(tested)*
2. If `title` has fuzzy-equality* to the title of a film in the database with the same year, then assume that same film is being referred to, add `title` as a new alias, and return the film's identification number. *(tested)*
   \*: fuzzy-equality is currently just case-insensitive string equality. More types of error will be caught later.
3. If there is a film with a title of `title` released within two years of `year`, then assume that same film is being referred to, add `title` as a new alias, and return the film's identification number. *(tested)*
4. Otherwise, perform a web-lookup. *(tested)*
