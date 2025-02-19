from action.backward_action import BackwardAction


class SpecialBackwardAction(BackwardAction):
    """
    This class adds a special feature to the backward action.
    The dragon will move backward until it finds an unoccupied
    volcano.
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

    def _valid_destination(self, destination):
        """
        This method is used to check if the destination is valid.
        In this action, the destination is always valid as long as
        the number of player is less than the number of volcanoes.
        So, if the player's expected destination is occupied, it 
        always check the next volcano until it finds an unoccupied
        volcano.
        """
        final_destination = None
        while destination != self.dragon.get_board_pos():
            vzone_index = destination // 3
            v_index = destination % 3
            volcano = self.volcanoe_zones[vzone_index].get_volcanoes()[v_index]
            # Check whether volcano is occupied
            if not volcano.can_enter():
                destination = (destination - 1) % self.volcano_size
                self.remaining_steps += 1
            else:
                final_destination = destination
                break

        # In extreme case, the number of player is the same as the
        # number of volcanoes, the player will not move.
        if final_destination is None:
            return False
        # Unoccupied volcano found
        else:
            self.destination = final_destination
            return True