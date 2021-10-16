# `test` Testing

The test suite is new to Version 2 of B-Movie Buddy (the first version is untested).  Since I have been trying to use Test-driven Development, a complete description of test coverage (and consequently the Version 2 API) can be found in `TDD docs`.

Tests are run against a database of known values, `Test.db`.  An individual, temporary copy of `Test.db` is used for each test to prevent test from interfering with each other.
