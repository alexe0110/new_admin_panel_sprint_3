from mover.config import Settings
from mover.components.extract import Extract

test_settings=Settings()


def test_extract():
    ext = Extract(pg_settings=test_settings.model_dump())
