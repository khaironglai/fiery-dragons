from action.move_action import MoveAction


class BackwardAction(MoveAction):
    """
    This class is used to determine the destination of the player
    based on the current position of the player and the steps when a 
    penalty card is drawn by the player.
    """

    def __init__(self, dragon, step, volcanoe_zones, caves):
        """
        This method initializes the backward action object.

        input:
        - dragon: the dragon instance that is going to move
        - step: the number of steps the dragon is going to move
        - volcanoe_zones: the volcano zones in the board
        - caves: the caves in the board

        return: None
        """
        super().__init__(dragon, step, volcanoe_zones, caves)

    def execute(self):
        """
        This method is used to execute the backward action.
        If destination is not None, the player moves to the destination.
        It then returns the end turn and end game flag to indicate whether 
        the player's turn end or the game end.

        return: bool, bool
        """
        if self.destination is not None:
            if self._valid_destination(self.destination):
                self.dragon.move(self.destination,
                                 self.volcanoe_zones, self.caves)
                self.dragon.set_remaining_steps(self.remaining_steps)
            else:
                self.end_turn = True
        return self.end_turn, self.end_game

    def _find_destination(self, pos):
        """
        This method is used to find the expected destination of the player.
        If the player is currently in his own cave, destination is set to 
        none and the player will not perform the backward movement.

        return: int
        """
        # When dragon is out of the cave, move backward 
        # (possible to move beyond the cave)
        if pos >= 0:
            destination = (pos - self.step) % self.volcano_size
            self.remaining_steps += self.step

        # When dragon is in the cave (remain in the cave)
        else:
            destination = None

        return destination