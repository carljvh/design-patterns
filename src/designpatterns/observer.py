from collections.abc import MutableSequence, Sequence
from dataclasses import dataclass, field
from typing import Generic, Literal, Protocol, TypeAlias, TypeVar
from datetime import datetime, timedelta

Sport: TypeAlias = Literal["Run", "Walk", "Bike", "Swim"]
T = TypeVar("T", covariant=True)
U = TypeVar("U", contravariant=True)


class Publisher(Generic[T], Protocol):
    def attach(self, subscriber: "Subscriber") -> None: ...

    def detach(self, subscriber: "Subscriber") -> None: ...

    def notify(self) -> None: ...

    def get_update(self) -> T: ...


class Subscriber(Generic[U], Protocol):
    def update(self, publisher: Publisher[U]) -> None: ...


@dataclass
class Recording:
    sport: Sport
    start_time: datetime
    end_time: datetime
    gps_coordinates: Sequence[tuple[float, float]]


@dataclass
class StrawaUser(Publisher[Recording], Subscriber[Recording]):
    ID: str
    recording: Recording | None = None
    subscribers: MutableSequence[Subscriber] = field(default_factory=list)
    feed: MutableSequence[Recording] = field(default_factory=list)

    def attach(self, subscriber: Subscriber[Recording]) -> None:
        if isinstance(subscriber, StrawaUser) and subscriber.ID == self.ID:
            raise ValueError(f"User cannot subscribe to own feed - ID: {self.ID}")
        self.subscribers.append(subscriber)

    def detach(self, subscriber: Subscriber[Recording]) -> None:
        self.subscribers.remove(subscriber)

    def notify(self) -> None:
        for subscriber in self.subscribers:
            subscriber.update(self)

    def get_update(self) -> Recording:
        if self.recording is None:
            raise ValueError(f"Feed for user with ID {self.ID} is empty")
        return self.recording

    def register_activity(self, recording: Recording) -> None:
        self.recording = recording
        self.feed.append(recording)
        print(f"Your new activity has been saved, {self.ID}!")
        self.notify()

    def update(self, publisher: Publisher[Recording]) -> None:
        if isinstance(publisher, StrawaUser) and publisher.ID == self.ID:
            raise ValueError(f"User cannot add own recording as subscribed content - ID: {self.ID}")
        recording = publisher.get_update()
        self.feed.append(recording)
        print(f"One of your Strawa mates has just completed a {recording.sport.lower()}, {self.ID}!")


if __name__ == "__main__":
    start_time = datetime.now()
    end_time = start_time + timedelta(minutes=55)
    gps_coordinates = [
        (59.363329, 17.872139),
        (59.36361925977473, 17.87227045888949),
        (59.36374800255386, 17.87244817040548),
        (59.36402006051324, 17.872563650512124),
        (59.3641472860572, 17.872678956245146),
        (59.364446992568425, 17.872795679290945),
        (59.36471494807265, 17.872996993154874),
        (59.364866428949085, 17.873137912591194),
        (59.36516249036535, 17.8734198373526),
        (59.365309617684225, 17.87355603326321),
    ]

    calle = StrawaUser("Calle")
    johan = StrawaUser("Johan")
    jonas = StrawaUser("Jonas")
    emma = StrawaUser("Emma")
    calle.attach(johan)
    calle.attach(jonas)
    calle.attach(emma)
    johan.attach(calle)
    johan.attach(jonas)
    recording = Recording("Walk", start_time, end_time, gps_coordinates)
    calle.register_activity(recording)
    recording = Recording("Run", start_time, end_time, gps_coordinates)
    johan.register_activity(recording)
