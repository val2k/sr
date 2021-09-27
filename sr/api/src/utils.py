import time

def add_timestamp_to_stat(stat_payload):
    stat_payload['timestamp'] = time.time()
    return stat_payload
