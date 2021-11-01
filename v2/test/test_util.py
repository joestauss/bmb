from bmb.v2.source.FilmDB import FilmDB
from bmb import PATH_TO_V2_TEST_DB
import pytest
import shutil
import random
from pathlib import Path

UNIQUE_TEMP_FILES = False

def _temp_copy( file, unique=UNIQUE_TEMP_FILES):
    if not UNIQUE_TEMP_FILES:
        temp_file = Path( f"{file}.temp")
    else:
        temp_file = file
        i = 1
        while temp_file.exists():
            tempend = f".temp{i}"
            temp_file = Path( f"{file}{tempend}")
            i += 1
    shutil.copyfile( file, temp_file)
    return temp_file

def destroy( self):
    self.file.unlink()

@pytest.fixture
def TestDB():
    db = FilmDB( _temp_copy(PATH_TO_V2_TEST_DB))
    db.destroy = lambda: destroy( db)
    return db
