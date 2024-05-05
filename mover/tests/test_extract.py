import pytest

from mover.config import Settings
from mover.components.extract import Extract

test_settings=Settings()


@pytest.fixture()
def pg_extractor():
    return Extract(pg_settings=test_settings.pg.model_dump())


def test_extract(pg_extractor: Extract):
    res = pg_extractor.kek()
    assert not res
