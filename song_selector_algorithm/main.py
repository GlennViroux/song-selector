"""Song Selector Algorithm"""

import random
from pathlib import Path
from typing import List

import pandas as pd

from core import SongInfo
from core.subset_sum_solver import SubSumSetSolver


def main():
    filepath = Path(__file__).parent / "data" / "songs.csv"
    df = pd.read_csv(filepath)
    songs = []  # type: List[SongInfo]
    for title, artist, duration in zip(df.title, df.artist, df.duration):
        songs.append(SongInfo(title=title, artist=artist, duration=duration))

    for _ in range(200):
        tth = random.uniform(100, 2000)
        SubSumSetSolver(tth, songs).solve()


if __name__ == "__main__":
    main()
