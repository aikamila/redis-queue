import time
import requests
from collections import Counter
import heapq
import functools
from bs4 import BeautifulSoup
from bs4.element import Comment

# TAGS_RE = re.compile('<.*?>')
# NON_ALPHABET = re.compile('\W+|[0-9]+|[_]+')


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)


@functools.total_ordering
class Element:
    def __init__(self, string, counter):
        self.string = string
        self.counter = counter

    def __lt__(self, other):
        if self.string == 'the' or self.string == 'a':
            return True
        if self.counter == other.counter:
            return self.string > other.string
        return self.counter < other.counter

    def __eq__(self, other):
        return self.counter == other.counter and self.string == other.string


def find_3_most_popular_words(url: str):
    # simulating long response time
    time.sleep(3)
    try:
        resp = requests.get(url)
        text = resp.text
        text = text_from_html(text)
    except:
        # handling all possible errors with a broad exception clause
        text = 'Not valid url'
    c = Counter(text.split())
    freqs = []
    heapq.heapify(freqs)
    for key, value in c.items():
        heapq.heappush(freqs, (Element(key, value), key))
        if len(freqs) > 3:
            heapq.heappop(freqs)
    res = []
    total = len(freqs)
    for _ in range(min(3, total)):
        res.append(heapq.heappop(freqs)[1])
    return res[::-1]
