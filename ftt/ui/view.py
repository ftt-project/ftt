from abc import abstractmethod
from tkinter import ttk


class NoControllerException(Exception):
    """View has no controller"""
    pass


class View(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._controller = None

    @abstractmethod
    def post_initialize(self):
        pass

    @property
    def controller(self):
        if self._controller is None:
            raise NoControllerException()

        return self._controller

    @controller.setter
    def controller(self, value):
        self._controller = value
