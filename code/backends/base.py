from typing import Any
from code.event import GameEvent


class GameBackend:
    def __init__(self) -> None:
        self.events = []

    def connect(self) -> None:
        raise NotImplementedError()

    def disconnect(self) -> None:
        raise NotImplementedError()

    def add_event(self, event: GameEvent) -> None:
        raise NotImplementedError()

    def current_state(self) -> None:
        raise NotImplementedError()

    def next_state(self) -> None:
        raise NotImplementedError()

    def previous_state(self) -> None:
        raise NotImplementedError()
