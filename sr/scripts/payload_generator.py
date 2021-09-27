import requests
import time

# This script is very naive. Values should be randomized

def send_payload():
    while True:
        data = {
            "token" : "c98arf53-ae39-4c9d-af44-c6957ee2f748",
            "customer": "Customer1",
            "content": "channel1",
            "timespan": 30000,
            "p2p": 10,
            "cdn": 10,
            "sessionDuration": 120000,
        }
        requests.post('http://localhost:80/stats', json=data)
        time.sleep(2)

if __name__ == "__main__":
    send_payload()
