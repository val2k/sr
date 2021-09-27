from psycopg2 import TimestampFromTicks

def timestamp_from_ticks(timestamp: float):
    return TimestampFromTicks(timestamp)

def create_tuple_from_stat_dict(stat: object) -> tuple:
    return tuple([
        timestamp_from_ticks(stat['timestamp']),
        stat['token'],
        stat['customer'],
        stat['content'],
        stat['cdn'],
        stat['p2p'],
        stat['sessionDuration']
    ])
