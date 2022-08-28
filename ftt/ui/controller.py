from abc import ABC, abstractmethod
from typing import Set

from ftt.ui.observers.observer import Observer


class Controller(ABC):
    _observers: Set[Observer] = set()

    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.controller = self
        self.view.post_initialize()

    def attach(self, observer):
        observer.append_notifiable(self)
        self._observers.add(observer)

    def notify(self, event) -> None:
        for observer in self._observers:
            observer.update(event)

    @abstractmethod
    def update(self, event):
        pass

    @abstractmethod
    def initialize_and_render(self):
        pass
