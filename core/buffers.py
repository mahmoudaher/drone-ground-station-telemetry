from collections import deque

buffers = {}

MAX_POINTS = 200


def get_key(d):
    return f'{d["src"]}:{d["ch"]}'


def add_sample(d):
    key = get_key(d)

    if key not in buffers:
        buffers[key] = deque(maxlen=MAX_POINTS)

    buffers[key].append((d["ts"], d["val"]))


def get_buffer(key):
    return list(buffers.get(key, []))


def list_channels():
    return list(buffers.keys())
