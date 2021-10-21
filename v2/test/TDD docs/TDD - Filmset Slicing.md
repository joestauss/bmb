# TDD: Filmset Slicing

One of the most common operations in B-Movie Buddy is selecting all of the films that meet a certain criteria.  This is accomplished through the **Filmset method**, `FilmDB.Filmset( self, **conditions)`, which returns a list of film identification numbers.

There are three keywords that can be used simultaneously as `conditions`; `year` can be either an integer or a `(year_min, year_max)` range tuple, and `genre` and `tag` both accept either a string (to require only a single genre or tag) or an object in _propositional syntax_, defined below.

## Propositional Syntax

_Propositional syntax_ is a Python-based method for representing complex category requirements to the filmset slicer. 

1. __Lists `[]` are used as a a logical "OR".__
2. __Tuples `()` are used as a logical "AND".__
3. __A set `{a, b, ...}` is interpreted as "NOT `a` AND NOT `b` AND `...`".__  In most cases, I'll just be using `{}` for a "NOT" operation but, since a set in Python cannot contain a list, it would have been impossible to represent $\lnot(a\lor b)$. Logically, $\lnot(a\lor b)$ is equivalent to $\lnot a\land\lnot b$, so `{}` can just expand to accommodate a multiple negation.

As an example, suppose that you are looking for a light-hearted movie to watch.  You prefer a horror-comedy or a romance that isn't too dramatic, and definitely no westerns.  These categories are represented logically as:
$$
\left[ ( Horror \land Comedy) \lor (Romance \land \lnot Drama) \right] \land \lnot Western
$$
In propositional syntax, this will be expressible as:

```python
genre=(
    [
        ('Horror', 'Comedy'),
        ('Romance', {'Drama'})
    ],
    { 'Western'}
) 
```



## Test Coverage

The data used to test this function is a set of films from the 1960's:  Each film is followed by its _ID number_ and _tags_.

1. The Hustler (1961) - 2; A, B
2. The Last Man on Earth (1964) - 3; A, C
3. Dr. Terror's House of Horrors (1965) - 4; B, C
4. The Thomas Crown Affair (1968) - 5; A, B, C

### Single Condition Tests

These tags each test one of the three keyword conditions by itself.

```python
def test_year( TestDB):
    known_ids = [2, 3, 4, 5]
    found_ids = TestDB.filmset( year=(1960, 1969))
    assert( all((film_id in found_ids for film_id in known_ids)))
    assert( len( known_ids) == len( found_ids))
    
def test_genre( TestDB):
	test_cases = [
     	("Horror", (3, 4) ),
     	(("Horror", {'Science Fiction'}), (4, ) ), # Horror and not SF
        (['Drama', 'Science Fiction'], (1, 2, 3, 5) ) # Drama OR SF
        ({('Crime', 'Romance')}, (1, 2, 3, 4)),    # not (Crime and romance)
        ({'Crime', 'Horror'}, (1, 2)),             # not crime and not horror
    ]
    for genres, result in test_cases:
        assert tuple( sorted( TestDB.filmset( genre=genres))) == result
    
def test_tags( TestDB):
    test_cases = [
        ( 'A'		               , (2, 3, 5) ), # A
        ( ('A', 'B')                , (2, 5 )),    # A and B
        ( ('A', {'B'})              , (3, )),      # A and not B
        ( [('A', 'B', 'C'), ('B', {'C'})], (2, 5))   # (A and B) or (B and not C)
    ]
    for tags, result in test_cases:
        assert tuple( sorted( TestDB.filmset( tag=tags))) == result
```

## Multiple Condition Tests

```python
def test_multiple_conditions_1( TestDB):
    known_ids = (2, 3, 4)
    found_ids = TestDB.filmset( year=(1960, 1969), genre={ 'Crime'} )
    assert tuple( sorted( found_ids)) == known_ids

def test_multiple_conditions_2( TestDB):
    known_ids = (4, 5)
    found_ids = TestDB.filmset( year=(1960, 1969), genre=['Horror', 'Crime'], tags=('B', 'C') )
    assert tuple( sorted( found_ids)) == known_ids
    
def test_multiple_conditions_3( TestDB):
    known_ids = (3, )
    found_ids = TestDB.filmset( year=(1960, 1969), genre='Horror', tags='A' )
    assert tuple( sorted( found_ids)) == known_ids
```

## To Do

* The Filmset method currently returns a set of film identification numbers, but it should return a custom list-like class with its own helper methods (a Filmset).
* Enable slicing; `FilmDB.Filmset` should accept an optional `arg` of films from which to slice