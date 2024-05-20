import pytest

from mover.components.enricher import Enricher
from mover.utils.state import RedisStorage


@pytest.mark.parametrize("table_name", ["film_work", "person", "genre"])
@pytest.mark.usefixtures("_clean_redis")
@pytest.mark.parametrize("redis_db", [1])
def test_enrich_data(pg_enricher: Enricher, redis_storage: RedisStorage, table_name: str, redis_db):
    ids_for_table = {
        "film_work": ["a9b29ca3-adf2-46b9-8455-9dccda64c400", "a9b29ca3-adf2-46b9-8455-9dccda64c401"],
        "person": ["a5a8f573-3cee-4ccc-8a2b-91cb9f55250a"],
        "genre": ["f24fd632-b1a5-4273-a835-0119bd12f825"],
    }
    pg_enricher.enrich_data(where_clause_table=table_name, pkeys=ids_for_table.get(table_name))

    redis_result = redis_storage.retrieve_state()

    assert redis_result.get("table") is None
    assert redis_result.get("pkeys") is None

    # потому что self.set_state(table=None, pkeys=None...
    # assert redis_result.get("table") == table_name, f"Wrong table in redis{redis_result.get('table')}"
    # assert redis_result.get("pkeys") == ids_for_table.get(table_name), f" Wrong pkeys {redis_result.get('pkeys')}"
