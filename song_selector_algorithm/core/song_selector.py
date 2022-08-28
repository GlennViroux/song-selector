"""Song Selector Algorithm"""

import random
from datetime import timedelta, datetime
from typing import List

from common import StuBruSingleton
from common.logger import StuBruLogger
from core import SongInfo
from core.subset_sum_solver import SubSumSetSolver


class SongManager(metaclass=StuBruSingleton):
    QueueSize = 15
    TimeToHourThreshold = timedelta(minutes=50)
    Logger = StuBruLogger()

    def __init__(self, songs: List[SongInfo]):
        self.Logger.info(f"Initializing SongManager with {len(songs)} songs")
        self.pending_songs = songs
        self.queue = self._initialize_queue()

    def _get_new_song(self) -> SongInfo:
        """Randomly pop a new song from the list of pending songs."""
        if not self.pending_songs:
            raise StopIteration(
                "Sorry friend, I've got no songs left. This is almost as bad as the day the music died."
            )
        result = self.pending_songs.pop(random.randint(0, len(self.pending_songs) - 1))
        self.Logger.info(f"Getting new song ({result})")
        return result

    def _initialize_queue(self) -> List[SongInfo]:
        """Initialize the queue with the configured amount of songs in the queue."""
        return [self._get_new_song() for _ in range(self.QueueSize - 1)]

    def _get_next_song(self) -> SongInfo:
        """Get the next song in the queue."""
        if not len(self.queue):
            raise StopIteration("Sorry friend, I've got no songs in my queue.")
        return self.queue.pop(0)

    def _add_batch_of_songs(self, time_to_hour: timedelta):
        """
        Add a batch of songs to the queue, minimizing the difference between the moment the final song ends and the
        start of the next hour.
        """

        self.Logger.info(f"Adding batch of songs, time to hour: {time_to_hour}")
        selected_songs = SubSumSetSolver(abs(time_to_hour.total_seconds()), self.pending_songs).solve()
        self.Logger.info(f"Found {len(selected_songs)} songs, adding to queue.")
        self.queue += selected_songs

    def _refill_queue(self, duration_current_song: timedelta):
        """
        Add one new song to the queue after a song had just been played from the queue. If there not much time left
        between the end of the queue and the following hour, a batch of songs if added at once to the queue, optimizing
        the time between the last song for the hour and the beginning of the next hour.
        """

        self.Logger.info(f"Refilling queue. Duration current song: {duration_current_song}")
        if len(self.queue) >= self.QueueSize:
            msg = (
                f"Current queue size ({len(self.queue)}) if bigger than configured queue size ({self.QueueSize}). "
                f"No new songs are added for now."
            )
            self.Logger.info(msg)
            return None

        total_seconds_queue = sum([song.duration for song in self.queue])
        end_of_songs = datetime.now() + duration_current_song + timedelta(seconds=int(total_seconds_queue))
        next_hour = (end_of_songs + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)

        if (time_to_hour := next_hour - end_of_songs) <= self.TimeToHourThreshold:
            self._add_batch_of_songs(time_to_hour)
        else:
            self.queue += self._get_new_song()

    def add_songs(self, new_songs: List[SongInfo]):
        """Add a batch of new songs to the list of pending songs."""
        songs_left = len(new_songs) + len(self.pending_songs)
        self.Logger.info(f"Adding {len(new_songs)} songs to SongManager. Total remaining songs: {songs_left}")
        self.pending_songs += new_songs

    def __iter__(self):
        return self

    def __next__(self):
        self.Logger.info("New song requested")
        next_song = self._get_next_song()
        self.Logger.info(f"Selected song: {next_song}")
        self._refill_queue(timedelta(seconds=int(next_song.duration)))
        return next_song
