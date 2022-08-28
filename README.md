# Song Selector Algorithm

A song selector algorithm designed for radio stations with continuous music and fixed breaks at the start of each hour.

## Installation

After cloning the project, install all dependencies with [poetry](https://python-poetry.org/):

```shell
poetry install
```

## Usage

Use the `SongManager` as a python iterator:

```python
from typing import List

from song_selector_algorithm import SongInfo, SongManager


titles = [...]  # type: List[str]
artists = [...]  # type: List[str]
durations = [...]  # type: List[float]
songs = []  # type: List[SongInfo]
for title, artist, duration in zip(titles, artists, durations):
    songs.append(SongInfo(title=title, artist=artist, duration=duration))

mgr = SongManager(songs)
next(mgr)  # The first song is requested and returned
next(mgr)  # The second song is requested and returned
mgr.add_songs(songs[:10]) # 10 new songs are added to the songs that can be played
next(mgr)  # The third song is requested and returned
```

## Tests

You can run all the tests with [pytest](https://docs.pytest.org/en/7.1.x/):

```shell
pytest tests/
```

## Implementation logic

The `SongManager` class is a singleton class, meaning there should exist only one instance of this class in the python application. It is initialized with a list of possible songs it could play.

The main working principle is an internal queue of songs that will be played. When the `SongManager` instance is created, the initial queue is created with a configurable amount of songs, for example 15 songs.

When a new song is requested, two actions occur:
* the first song in the queue is requested and removed from the queue
* the queue is "refilled"

### Refilling the queue

Refilling the queue is done in a specific manner, to make sure that at the start of each hour, the latest songs should be almost near completion.

A new concept is considered: the Time To Hour (TTH), denoting the time difference between the moment the final song of the current queue will finish playing, and the start of the following hour.

A configurable duration threshold (for example 15 minutes) is defined as the Threshold Time To Hour (TTTH), which is the period of time which we should consider to activate the optimization algorithm that selects songs to fit the hourly news constraint.

There are three different workflows possible when refilling the queue:
* if the current size of the queue is bigger than the configured size of the queue, no actions are performed
* if the current size of the queue is smaller than the configured size of the queue and the TTH is bigger than the TTTH, a new song is randomly chosen and added to the queue
* if the current size of the queue is smaller than the configured size of the queue and the TTH is smaller than the TTTH, a batch of new songs is added to the queue, minimizing the difference between the completion time of the latest song of the batch and the start of the following hour

### Time Optimization Algorithm

For the Time Optimization Algorithm, we have the following situation:

* there's a specific TTH, which is the current time difference between the completion of the final song in the queue and the start of the following hour
* there's a list of pending songs we could add to the queue

This is, in fact, a specific case of the subset-sum problem, which tries to find a subset of integers from a larger set of integers whose sum is closest to, but not greater than, a given positive integer bound. More specifically for this case, we're looking for a subset of songs whose total duration is closest to, but does not exceed the given TTH.

This mathematical problem is actually NP-hard (non-deterministic polynomial-time hardness), as there exist `2^n -1` subsets that could be checked for `n` different options. If we have only 100 possible songs we could play, this would result in `1.2676506*10^30` subsets we could check.

However, faster and more efficient algorithms have been developed. Also, for this specific case, we are not really interested in knowing if there's a solution that exactly matches the time constraint. We are, in fact, more interested in finding the set of songs that most closely approximates the time constraint. Following and implementing the [Fast Approximation Algorithm for the Subset-Sum Problem from Bartosz Przydatek](https://web.stevens.edu/algebraic/Files/SubsetSum/przydatek99fast.pdf), we can find satisfying results for our use case.
