from psycopg2.extras import RealDictRow

from mover.components.extract import Extract


def test_extract_kek(pg_extractor: Extract):
    res = pg_extractor.kek()

    assert isinstance(res, list), f"Return not list, type = {type(res)}"
    assert isinstance(res[0], RealDictRow), f"0 Element not RealDictRow, type = {type(res[0])}"


def test_extract_modified_date(pg_extractor: Extract):
    res = pg_extractor.get_last_modified(table="film_work")

    print(res)
