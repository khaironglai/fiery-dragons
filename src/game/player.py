from memorable import Memorable
from dragon import Dragon


class Player(Memorable):
    """
    This class is used to create a player object.
    Each player has a unique id and a list of dragons.
    """

    def __init__(self, id, dragon_num):
        """
        This method initializes the player object.

        input:
        - id: the id of the player
        - dragon_num: the number of dragons each player possesses

        return: None
        """
        self.player_id = id
        self.dragons = self._create_dragons(dragon_num)

    def get_id(self):
        """
        The getter method to return the id of the player.

        return: int
        """
        return self.player_id

    def get_dragons(self):
        """
        The getter method to return the dragons of the player.

        return: list
        """
        return self.dragons

    def draw(self, window):
        """
        This method is used to draw the dragons of the player on the window.

        input:
        - window: the window object to draw the dragons

        return: None
        """
        for dragon in self.dragons:
            dragon.draw(window)

    def save(self):
        """
        This method is used to save the player object.

        return: dict
        """
        return {
            "dragons": [dragon.save() for dragon in self.dragons]
        }

    def load(self, state):
        """
        This method is used to load the player object.
        Currently, the player does not need to save anything other than the dragons.

        input:
        - state: the player state to load

        return: None
        """
        for i in range(len(self.dragons)):
            self.dragons[i].load(state["dragons"][i])

    def choose_dragon(self, valid_dragons):
        """
        This method is used to let the player choose which dragon to move.
        By default, it returns the first dragon in the valid_dragons list even 
        if there are multiple choices (currently one player has one dragon only).
        Further implementation can be done for games where one player has multiple 
        dragons (prompt the user to choose the dragon).

        input:
        - valid_dragons: the list of dragons that are possible for the action 
                         to be performed

        return: Dragon
        """
        return valid_dragons[0]

    def _create_dragons(self, dragon_num):
        """
        This method creates the dragons.

        input:
        - dragon_num: the number of dragons each player possesses

        return: list
        """
        dragons = []
        initial_dragon_id = self.player_id * dragon_num
        # Dragon id is unique for each dragon
        for i in range(dragon_num):
            id = initial_dragon_id + i
            dragons.append(Dragon(id))
        return dragons