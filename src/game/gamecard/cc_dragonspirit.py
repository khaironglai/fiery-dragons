from gamecard.chit_card import ChitCard
from gamecard.animal_type import AnimalType
from action.teleport_cave_action import TeleportCaveAction


class DragonSpiritCC(ChitCard):
    """
    This class is used to create a DragonSpirit chit card object.
    This chit card is for letting the game to have a memory-card like feature.
    This chit card serve for letting the game be more interesting and unpredictable.
    """
    ANIMAL_TYPE = AnimalType.DRAGON_SPIRIT

    def __init__(self):
        """
        This method initializes the DragonSpirit chit card object.
        
        return: None
        """
        super().__init__(DragonSpiritCC.ANIMAL_TYPE, 1,
                         f"images/chit cards/dragon spirit.png")

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
        The action is to teleport the dragon to a nearest unoccupied cave
        which is located at the backwards.
        """
        return TeleportCaveAction(dragon, self.get_animal_num(), 
                                  volcanoe_zones, caves)