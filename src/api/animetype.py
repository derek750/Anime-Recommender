from typing import TypedDict

class Anime(TypedDict, total=False):
    anime_id: int
    title: str
    english_title: str | None
    japanese_title: str | None
    type: str
    episodes: int | None
    duration: str | None
    status: str
    source: str | None
    season: str | None
    studios: str | None
    genres: str | None
    rating: str | None
    score: float | None
    scored_by: int | None
    rank: int | None
    popularity: int | None
    members: int | None
    favorites: int | None
    watching: int | None
    completed: int | None
    on_hold: int | None
    dropped: int | None
    plan_to_watch: int | None
    start_date: str | None
    end_date: str | None
    broadcast_day: str | None
    broadcast_time: str | None
    synopsis: str | None