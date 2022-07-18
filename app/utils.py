import time
import requests
from collections import Counter
import heapq
import functools


def find_3_most_popular(url: str):
    # simulating long response time
    time.sleep(20)
    resp = requests.get(url)
    c = Counter(resp.text.split())

    return ['hi', 'nice', 'day']
