from enum import Enum


class EntryState(Enum):
    EMPTY = 0
    OBSTACLE = 1
    START = 2
    TARGET = 3
    QUEUED = 4
    PROCESSED = 5
    VISITED_ONCE = 6
    VISITED_TWICE = 7
    DEAD_END = 8
    POSSIBLE_PATH = 9
