import time
import requests
from collections import Counter
import heapq
import functools
import re


CLEAN_RE = re.compile('<.*?>')

@functools.total_ordering
class Element:
    def __init__(self, string, counter):
        self.string = string
        self.counter = counter

    def __lt__(self, other):
        if self.counter == other.counter:
            return self.string > other.string
        return self.counter < other.counter

    def __eq__(self, other):
        return self.counter == other.counter and self.string == other.string


def find_3_most_popular(url: str):
    # simulating long response time
    time.sleep(3)
    resp = requests.get(url)
    text = resp.text
    text = re.sub(CLEAN_RE, '', text)
    c = Counter(text.split())
    freqs = []
    heapq.heapify(freqs)
    for key, value in c.items():
        heapq.heappush(freqs, (Element(key, value), key))
        if len(freqs) > 3:
            heapq.heappop(freqs)
    res = []
    for _ in range(3):
        res.append(heapq.heappop(freqs)[1])
    return res[::-1]
