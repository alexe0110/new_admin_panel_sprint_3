import pytest

from mover.config import Settings
from mover.components.extract import Extract
from psycopg2.extras import RealDictCursor, RealDictRow

test_settings=Settings()


@pytest.fixture()
def pg_extractor():
    return Extract(pg_settings=test_settings.pg.model_dump())


def test_extract_kek(pg_extractor: Extract):
    res = pg_extractor.kek()

    assert isinstance(res, list), f'Return not list, type = {type(res)}'
    assert isinstance(res[0], RealDictRow), f'0 Element not RealDictRow, type = {type(res[0])}'
