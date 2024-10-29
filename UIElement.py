from abc import ABC, abstractmethod
from Renderable import Renderable


class UIElement(ABC):

    @abstractmethod
    def hide(self):
        pass

    @abstractmethod
    def reset(self):
        pass