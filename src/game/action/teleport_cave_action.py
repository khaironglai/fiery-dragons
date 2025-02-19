from action.move_action import MoveAction


class TeleportCaveAction(MoveAction):
    """
    This class is a special move action class.
    The dragon will move backward until it finds an empty cave.
    Unless if the dragon is currently in a cave, 
    then it will not move backward.
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
        This method is used to execute the teleport cave action.
        If destination is not None, the player moves to the destination.
        It then returns the end turn  and end game flag to indicate 
        whether the player's turn end.

        return: bool, bool
        """
        if self.destination is not None:
            self.dragon.move(self.destination, self.volcanoe_zones, self.caves)
            self.dragon.set_remaining_steps(self.remaining_steps)
        return self.end_turn, self.end_game

    def _find_destination(self, pos):
        """
        This method is used to find the expected destination of the player.
        It checks whether the dragon in a cave or not.
        If the dragon is currently in a cave, the dragon does not need to
        move. If the dragon is not in a cave, the dragon will move backward
        until it finds an empty cave. 

        return: int
        """
        # When dragon is out of the cave, the dragon will move backward
        # until it finds an empty cave.
        if pos >= 0:
            destination = None
            i = (pos - 1) % self.volcano_size
            self.remaining_steps += 1
            while i != pos:
                vzone_index = i // 3
                v_index = i % 3
                volcano = self.volcanoe_zones[vzone_index].get_volcanoes()[
                    v_index]
                cave_id = volcano.get_cave_id()
                if cave_id is not None:
                    cave = self.caves[cave_id]
                    if cave.can_enter():
                        destination = -(i + 1)
                        self.remaining_steps += 1
                        break
                i = (i - 1) % self.volcano_size
                self.remaining_steps += 1

        # When dragon is in the cave (remain in the cave)
        else:
            destination = None

        return destination