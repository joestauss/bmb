# `bmb` B-Movie Buddy

This repository contains my __personal movie database__.  As the name implies, one of the objectives is to help me find relatively unknown retro sci-fi and horror movies.

## Repository Organization

The top-level directory contains two folders, both containing a `README` that provides more detailed information about its contents:

1. `notebooks` holds Jupyter notebooks for various tasks, including data intake, processing, visualization, *etc*.
2. `source` has source code.   I tried to design a clear API, so you should be able to follow the `notebooks` without needing to refer to `source` for any implementation details, but Python programmers will find a few things that I've done interesting.

Not everything is publicly available; all database files, webscraping code, and API keys have been *gitignore*'d.

## Databases

Data flows through three different SQLite databases:

1. The **Ingestion Database** keeps track of which films are currently available to stream on Neflix, Hulu, and Amazon Prime.  As more functionality is added, this database will be the intermediary between all the messy webscraping operations and the well-structured databases downstream.
2. The **Processing Database** is used for categorization and analysis.  It is the primary database for most use cases.  Everything done to the this database must be repeatable - no hand-annotation or tweaking.
3. The **Data Warehouse** is the deliverable - a personal movie database.  The data it contains is unique - whether I have seen *The Godfather* and my opinion of it cannot be derived from any other source.