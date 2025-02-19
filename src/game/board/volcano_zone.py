from board.volcano import Volcano
from board.land_type import LandType
from memorable import Memorable


class VolcanoZone(Memorable):
    """
    This class is used to create a volcano zone object.
    A volcano zone is a collection of volcanoes.
    """

    def __init__(self, animal_ls):
        """
        This method initializes the volcano zone object.

        input:
        - animal_ls: the list of animal types

        return: None
        """
        self.volcanoes = self._create_volcano(animal_ls)

    def get_volcanoes(self):
        """
        The getter method to return the volcanoes in the volcano zone.

        return: list
        """
        return self.volcanoes

    def save(self):
        """
        This method is used to save the volcanoes in the 
        volcano zone object.

        return: dict
        """
        return {
            "volcanoes": [volcano.save() for volcano in self.volcanoes]
        }

    def load(self, state):
        """
        This method is used to load the volcano zone object.

        input:
        - state: the volcano zone state to load

        return: None
        """
        for i in range(len(self.volcanoes)):
            self.volcanoes[i].load(state["volcanoes"][i])

    def _create_volcano(self, animal_ls):
        """
        This method is used to create the volcanoes in the volcano zone.

        input:
        - animal_ls: the list of animal types

        return: list
        """
        volcanoes = []
        for animal in animal_ls:
            volcanoes.append(Volcano(animal, LandType.VOLCANO))

        return volcanoes