from gamecard.card import Card
from board.land import Land
from memorable import Memorable


class Volcano(Card, Land, Memorable):
    """
    This class is used to create a volcano object.
    A volcano is where the dragon walks on the board.
    """
    SCALE = 0.055

    def __init__(self, animal, land):
        """
        This method initializes the volcano object.

        input:
        - animal: the animal type of the card
        - land: the land type of the card

        return: None
        """
        Card.__init__(self, animal)
        Land.__init__(
            self, land, f"images/volcanoes/{str(animal)[11:]}.png", Volcano.SCALE)
        self.cave_id = None # Mark the cave id if the volcano is connected to a cave

    def set_cave_id(self, cave_id):
        """
        This method is used to set the cave of the volcano.
        Only some caves can be connected to the volcano.

        input:
        - cave_id: the cave id

        return: None
        """
        self.cave_id = cave_id

    def get_cave_id(self):
        """
        This method is used to get the cave id of the volcano.

        return: int
        """
        return self.cave_id

    def save(self):
        """
        This method is used to save the volcano object.

        return: dict
        """
        return {
            "cave": self.cave_id if self.cave_id else None
        }

    def load(self, state):
        """
        This method is used to load the volcano object.

        input:
        - state: the volcano state to load

        return: None
        """
        self.cave = state["cave"]

    def can_enter(self):
        """
        This method is used to check if the player can enter the volcano.
        The player can enter the volcano if the volcano is not occupied.

        return: bool
        """
        return not self.occupied