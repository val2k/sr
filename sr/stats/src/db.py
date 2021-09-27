import logging
import psycopg2
import sys

from src.constants import (
    POSTGRES_DB,
    POSTGRES_HOST,
    POSTGRES_USER,
    POSTGRES_PW
)
from .utils import create_tuple_from_stat_dict, timestamp_from_ticks

logger = logging.getLogger("stats")

class SQLQueries:

    INSERT_STAT_AGGREGATED = """
        INSERT INTO stats
        VALUES (%(time)s, %(customer)s, %(content)s, %(cdn)s, %(p2p)s, %(sessions)s);
    """

    INSERT_STAT_NON_AGGREGATED = """
        INSERT INTO stats_non_aggregated
        VALUES (%s, %s, %s, %s, %s, %s, %s);
    """

    SELECT_STATS_IN_WINDOW = """
        SELECT COUNT(DISTINCT token), customer, content, sum(cdn), sum(p2p)
        FROM stats_non_aggregated
        WHERE time
        BETWEEN to_timestamp(%s) AND to_timestamp(%s)
        GROUP BY (customer, content)
    """

class DBClient():

    def __init__(self):
        self._connection = self._init()
        self._cursor = self._connection.cursor()

    def _init(self):
        try:
            connection = psycopg2.connect(
                database=POSTGRES_DB,
                host=POSTGRES_HOST,
                user=POSTGRES_USER,
                password=POSTGRES_PW
            )
        except Exception as e:
            logger.error("Error accessing database: {}".format(e))
            sys.exit(1)
        return connection

    def __del__(self):
        try:
            self._connection.close()
            self._cursor.close()
        except AttributeError:
            pass

    def query(self, sql_query_string, query_tuple):
        self._cursor.execute(sql_query_string, query_tuple)
        self._connection.commit()
        return self._cursor

    def insert_aggregated_stat(self, aggregated_stat: dict):
        logger.info("Trying to insert aggregated stat ({}).".format(aggregated_stat))
        self.query(SQLQueries.INSERT_STAT_AGGREGATED, aggregated_stat)
        logger.info("Inserted ({}).".format(aggregated_stat))

    def insert_non_aggregated_stat(self, stat: dict):
        query_tuple = create_tuple_from_stat_dict(stat)
        logger.info("Trying to insert non_aggregated stat ({}).".format(stat))
        self.query(SQLQueries.INSERT_STAT_NON_AGGREGATED, query_tuple)
        logger.info("Inserted ({}).".format(stat))

    def select_aggregated_stat_in_window(self, window_start: float, window_end: float):
        """
        This methods aggregates and returns the non-aggregated stats in the given window.
        To calculate the number of sessions, we calculate the number of differents tokens
        for a given customer & content.
        """

        query_tuple = (window_start, window_end)
        cursor = self.query(SQLQueries.SELECT_STATS_IN_WINDOW, query_tuple)
        results = cursor.fetchall()

        if not results:
            return []

        stats_dict_keys = ["sessions", "customer", "content", "cdn", "p2p"]
        aggregated_stats = []
        for result in results:
            aggregated_stat = dict(zip(stats_dict_keys, result))
            aggregated_stat['time'] = timestamp_from_ticks(window_end)
            aggregated_stats.append(aggregated_stat)
        
        return aggregated_stats
