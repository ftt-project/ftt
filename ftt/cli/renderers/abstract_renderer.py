from abc import ABC, abstractmethod


class AbstractRenderer(ABC):
    @abstractmethod
    def render(self) -> None:
        pass
