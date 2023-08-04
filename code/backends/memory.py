from .base import GameBackend
from code.event import GameEvent


class MemoryBackend(GameBackend):
    def __init__(self) -> None:
        self.events = []
        self.cursor = 0

    def connect(self) -> None:
        pass

    def disconnect(self) -> None:
        pass

    def add_event(self, event: GameEvent) -> None:
        self.events.append(event)

    def current_state(self) -> GameEvent:
        if len(self.events) > self.cursor:
            return self.events[self.cursor]
        else:
            return None

    def next_state(self) -> GameEvent:
        if len(self.events) > self.cursor + 1:
            self.cursor = self.cursor + 1
            return self.events[self.cursor]
        else:
            return None

    def previous_state(self) -> GameEvent:
        if len(self.events) > self.cursor - 1 >= 0:
            self.cursor = self.cursor - 1
            return self.events[self.cursor]
        else:
            return None
