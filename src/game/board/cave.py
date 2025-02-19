from gamecard.card import Card
from board.land import Land
from memorable import Memorable


class Cave(Card, Land, Memorable):
    """
    This class is used to create a cave object.
    A cave is where the dragon starts and end in the game.
    A cave does not allow other dragons to enter.
    """
    SCALE = 0.055

    def __init__(self, id, animal, land, board_pos):
        """
        This method initializes the cave object.

        input:
        - id: the id of the cave (match with the owner's id)
        - animal: the animal type of the card
        - land: the land type of the card
        - board_pos: the board position of the cave

        return: None
        """
        Card.__init__(self, animal)
        Land.__init__(
            self, land, f"images/caves/{str(animal)[11:]}.png", Cave.SCALE)
        self.id = id
        self.board_pos = board_pos

    def get_id(self):
        """
        This method is used to get the id of the cave.

        return: int
        """
        return self.id

    def get_board_pos(self):
        """
        This method is used to get the board position of the cave.

        return: int
        """
        return self.board_pos

    def set_board_pos(self, pos):
        """
        This method is used to set the board position of the cave.

        input:
        - pos: the board position of the cave

        return: None
        """
        self.board_pos = pos

    def save(self):
        """
        This method is used to save the cave object.

        return: int
        """
        return self.board_pos

    def load(self, state):
        """
        This method is used to load the cave object.
        Currently, nothing is needed

        input:
        - state: the cave state to load

        return: None
        """
        pass

    def can_enter(self):
        """
        This method is used to check if the player can enter the cave.

        return: bool
        """
        return not self.occupied