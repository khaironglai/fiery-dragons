from gamecard.chit_card import ChitCard
from gamecard.animal_type import AnimalType
from action.backward_action import BackwardAction
from action.special_backward_action import SpecialBackwardAction


class DragonPirateCC(ChitCard):
    """
    This class is used to create a DragonPirate chit card object.
    This chit card is for letting the game to have a memory-card like feature.
    This chit card serve as a penalty for the player
    """
    ANIMAL_TYPE = AnimalType.DRAGON_PIRATE

    def __init__(self, animal_num):
        """
        This method initializes the DragonPirate chit card object.

        input:
        - animal_num: the number of the animal

        return: None
        """
        super().__init__(DragonPirateCC.ANIMAL_TYPE, animal_num,
                         f"images/chit cards/dragon pirate {animal_num}.png")

    def valid_dragon(self, dragons, volcanoe_zones, caves):
        """
        This method is used to get the valid dragons that can be moved.
        For this chit card action, all the dragons are valid.

        input:
        - dragons: the list of dragons
        - volcanoe_zones: the list of volcanoes
        - caves: the list of caves

        return: list of dragons
        """
        return dragons

    def get_action(self, dragon, volcanoe_zones, caves):
        """
        This method is used to get the action of the chit card.
        The action is to move the dragon backward.
        The specific backward action can be changed

        input:
        - dragon: the dragon object
        - volcanoe_zones: the list of volcanoes
        - caves: the list of caves

        return: BackwardAction
        """
        return SpecialBackwardAction(dragon, self.get_animal_num(), 
                                     volcanoe_zones, caves)