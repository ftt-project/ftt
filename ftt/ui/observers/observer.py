from abc import ABC
from typing import Set, Any


class Observer(ABC):
    _notifiables: Set[Any] = set()

    def append_notifiable(self, notifiable):
        self._notifiables.add(notifiable)

    def update(self, event):
        for notifiable in self._notifiables:
            notifiable.update(event)