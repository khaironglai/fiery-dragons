from gamecard.chit_card import ChitCard
from gamecard.animal_type import AnimalType
from action.forward_action import ForwardAction

class SpiderCC(ChitCard):
    """
    This class is used to create a Spider chit card object.
    This chit card is for letting the game to have a memory-card like feature.
    """
    ANIMAL_TYPE = AnimalType.SPIDER

    def __init__(self, animal_num):
        """
        This method initializes the Spider chit card object.
        
        input:
        - animal_num: the number of the animal
        
        return: None
        """
        super().__init__(SpiderCC.ANIMAL_TYPE, animal_num, 
                         f"images/chit cards/spider {animal_num}.png")

    def get_action(self, dragon, volcanoe_zones, caves):
        """
        This method is used to get the action of the chit card.
        The action is to move the dragon forward.
        
        input:
        - dragon: the dragon object
        - volcanoe_zones: the list of volcanoes
        - caves: the list of caves
        
        return: ForwardAction
        """
        return ForwardAction(dragon, self.get_animal_num(), 
                             volcanoe_zones, caves)