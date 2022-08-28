from pathlib import Path
from typing import List

import pandas as pd
import pytest

from song_selector_algorithm import __version__, SongInfo, SongManager


def test_version():
    assert __version__ == '0.1.0'

@pytest.fixture
def songs() -> List[SongInfo]:
    filepath = Path(__file__).parent / "data" / "songs.csv"
    df = pd.read_csv(filepath)
    songs = []  # type: List[SongInfo]
    for title, artist, duration in zip(df.title, df.artist, df.duration):
        songs.append(SongInfo(title=title, artist=artist, duration=duration))

    return songs

def test_singleton(songs: List[SongInfo]):
    mgr1 = SongManager(songs)
    mgr2 = SongManager(songs[:10])

    assert mgr1 is mgr2

def test_selector(songs: List[SongInfo]):
    mgr = SongManager(songs)
    next(mgr)
    next(mgr)
    mgr.add_songs(songs[:10])
    next(mgr)
