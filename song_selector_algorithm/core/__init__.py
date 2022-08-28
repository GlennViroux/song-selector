from datetime import timedelta

from pydantic import BaseModel

from common.snippets import pretty_duration


class SongInfo(BaseModel):
    title: str
    artist: str
    duration: float

    def __str__(self):
        duration_timedelta = timedelta(seconds=int(self.duration))
        return f"{self.title} - {self.artist} ({pretty_duration(duration_timedelta)})"

    def __hash__(self):
        return hash((self.title, self.artist, self.duration))
