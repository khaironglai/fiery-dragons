from abc import ABC, abstractmethod


class Memorable(ABC):
    """
    Represents an interface for a memorable object.
    A memorable object is an object that can be saved and loaded.
    """

    @abstractmethod
    def save(self):
        """
        This method is used to save the object.
        Detailed implementation will be in the subclass.
        """
        pass

    @abstractmethod
    def load(self, state):
        """
        This method is used to load the object.
        Detailed implementation will be in the subclass.
        """
        pass