from abc import ABC, abstractmethod


class MoveAction(ABC):
    """
    Abstract class for a move action.
    This class determines the destination of the player based on 
    the current position of the player and the steps.
    It checks whether the expected destination of the player is 
    occupied. If it is, the player will not move to the destination
    and the player's turn end.
    """

    def __init__(self, dragon, step, volcanoe_zones, caves):
        """
        This method initializes the move action object.

        input:
        - dragon: the dragon instance that is going to move
        - step: the number of steps the dragon is going to move
        - volcanoe_zones: the volcano zones in the board
        - caves: the caves in the board

        return: None
        """
        self.dragon = dragon
        self.step = step
        self.volcanoe_zones = volcanoe_zones
        self.caves = caves
        self.volcano_size = len(volcanoe_zones) * \
            len(volcanoe_zones[0].get_volcanoes())
        self.remaining_steps = self.dragon.get_remaining_steps()
        self.end_turn = False   # Flag to check if the player's turn ends
        self.end_game = False   # Flag to check if the game ends
        self.destination = self._find_destination(self.dragon.get_board_pos())

    def _valid_destination(self, destination):
        """
        This method is used to check if the destination is valid.
        A destination is valid if:
            - the volcano/cave is not occupied by other dragon

        input:
        - destination: the destination index on the game board

        return: bool
        """
        if destination >= 0:
            vzone_index = destination // 3
            v_index = destination % 3
            volcano = self.volcanoe_zones[vzone_index].get_volcanoes()[v_index]
            return volcano.can_enter()
        else:
            vol_pos = abs(destination) - 1
            vzone_index = vol_pos // 3
            v_index = vol_pos % 3
            volcano = self.volcanoe_zones[vzone_index].get_volcanoes()[v_index]
            return self.caves[volcano.get_cave_id()].can_enter()

    @abstractmethod
    def execute(self):
        """
        This method is used to execute the move action.
        """
        pass

    @abstractmethod
    def _find_destination(self):
        """
        This method is used to find the expected destination of the player.
        """
        pass