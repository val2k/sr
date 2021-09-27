import datetime
import json
import click
import logging

from .db import DBClient

logger = logging.getLogger("stats")

class StatService():

    def __init__(self):
        self.db_client = DBClient()

    def insert_aggregated_stat(self, aggregated_stat: object):
        stat = json.loads(aggregated_stat)
        self.db_client.insert_aggregated_stat(stat)    

    def insert_non_aggregated_stat(self, stat_payload: str):
        stat = json.loads(stat_payload)
        self.db_client.insert_non_aggregated_stat(stat)    

    @staticmethod
    def dag_timestamp_to_isoformat(dag_timestamp: str) -> float:
        dag_timestamp = dag_timestamp.split('.')[0]
        dag_timestamp = dag_timestamp.replace(" ", "T")
        isoformat: float = datetime.datetime.fromisoformat(dag_timestamp).timestamp()
        return isoformat

    @staticmethod
    @click.command()
    @click.option('--window-start')
    @click.option('--window-end')
    def aggregate_stats(window_start, window_end):
        """
        This function will aggregate stats with timestamps starting at
        {{ prev_execution_date }} (Airflow macro) and ending at {{ execution_date }} (Airflow macro)
        
        Parameters:
        window_start (int): Passed by Airflow DAG.
        window_end (int): Passed by Airflow DAG.
        """
        db_client = DBClient()
        window_start_isoformat: float = StatService.dag_timestamp_to_isoformat(window_start)
        window_end_isoformat: float = StatService.dag_timestamp_to_isoformat(window_end)

        aggregated_stats = db_client.select_aggregated_stat_in_window(
            window_start_isoformat,
            window_end_isoformat
        )

        for aggregated_stat in aggregated_stats:
            # TODO(vkinyock): Bulk insert
            db_client.insert_aggregated_stat(aggregated_stat)
