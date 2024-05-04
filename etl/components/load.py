"""Load data process."""

import logging
from datetime import datetime
from logging.config import dictConfig
from typing import List

from elasticsearch import Elasticsearch, helpers
from redis import Redis
from etl import sql_templates, state


logger = logging.getLogger(__name__)


class ESLoader(object):
    """Load data to Elastic Search.

    Attributes:
        client: Elisticsearch client.
        storage: Permanent storage to keep state.
        state: State of the process

    """

    def __init__(
            self,
            redis_connection: Redis,
            transport_options: dict,
            index: str,
            index_schema: dict = None
    ) -> None:
        """ESLoader class constructor.

        Args:
            transport_options: Elasticsearch connection parameters.
            index: Name of the Elasticsearch index.
            index_schema: Schema of the index. Not None: the index creates.
            redis_settings: Redis connection settings.

        """
        self.client = Elasticsearch(**transport_options)
        self.storage = state.RedisStorage(redis_connection)
        self.state = state.State(self.storage)
        self.index = index

        if index_schema:
            self.create_index(index=index, index_schema=index_schema)
        self.proceed()

    def proceed(self):
        """Check the state and proceed to work if there is data in the cache."""
        if self.state.state.get('data'):
            logger.debug('Data to proceed %s', self.state.state.get('data'))
            self.proccess(self.state.state['data'])

    def convert_to_bulk_format(self, data: dict) -> dict:
        """Convert to bulk format.

        Args:
            data: Converting dictionary.

        Returns:
            dict: Converted dictionary.

        """
        print('data:', data)
        data['_index'] = self.index
        if id := data.get('id'):
            data['_id'] = id
        return data

    def proccess(self, data: dict) -> None:
        """Load data to Elasticsearch.

        Args:
            data: Loading data.

        """
        print('data in process', data)
        for i in data:
            print('\t- ', i)
        self.state.set_state(key='data', value=data)
        self.bulk(list(map(self.convert_to_bulk_format, data)))
        self.state.set_state(key='data', value=None)

    # @backoff()
    def create_index(self, index: str, index_schema: dict) -> None:
        """Create index if the index doesn't exists.

        Args:
            index: Name of the index.
            index_schema: Schema of the index.

        """
        if not self.client.indices.exists(index=index):
            self.client.indices.create(index=index, body=index_schema)

    # @backoff()
    def bulk(self, data: List[dict]) -> None:
        """Bulk data to ES with backoff implementation.

        Args:
            data: Loading data.

        """
        _, errors = helpers.bulk(self.client, data, stats_only=False)
        if errors:
            failed = self.state.get_state('failed') or []
            failed.append(
                {
                    'time': datetime.now(),
                    'details': errors,
                },
            )
            self.state.set_state(key='failed', value=failed)
            logger.error('Error to bulk data %s', errors)
