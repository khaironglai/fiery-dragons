from action.move_action import MoveAction


class ForwardAction(MoveAction):
    """
    This class is used to determine the destination of the player
    based on the current position of the player and the steps when a 
    matching card is drawn by the player.
    """

    def __init__(self, dragon, step, volcanoe_zones, caves):
        """
        This method initializes the forward action object.

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
        This method is used to execute the forward action.
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
                self.end_game = False
        return self.end_turn, self.end_game

    def _find_destination(self, pos):
        """
        This method is used to find the expected destination of the player.
        If the player is almost reach his cave but does not get the exact 
        number of steps, the player will remain at the initial position and 
        hence the destination is set to none. Meanwhile, if the player 
        successfully lands on its own cave in the exact number of steps, 
        the game ends.

        return: int
        """
        # When dragon is out of the cave, move forward 
        if pos >= 0:
            # Not exact steps to reach the cave (remain at the initial position)
            if self.step > self.remaining_steps:
                destination = None
                self.end_turn = True
            # Move forward
            elif self.step < self.remaining_steps:
                destination = (pos + self.step) % self.volcano_size
                self.remaining_steps -= self.step
            # Exact steps to reach the cave (game ends, player wins the game)
            else:
                destination = -(((pos + self.step - 1) %
                                self.volcano_size) + 1)
                self.end_game = True
                self.remaining_steps = 0

        # When dragon is in the cave, move to the volcano tiles
        else:
            vol_pos = abs(pos) - 1
            destination = (vol_pos + (self.step - 1)) % self.volcano_size
            self.remaining_steps -= self.step

        return destination