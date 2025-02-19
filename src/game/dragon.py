from drawable import Drawable
from memorable import Memorable


class Dragon(Drawable, Memorable):
    """
    This class is used to create a dragon object.
    Dragon is basically the pieces control by the player.
    It is the thing that moves around the board.
    """
    SCALE = 0.11

    def __init__(self, id):
        """
        This method initializes the dragon object.

        input:
        - id: the id of the dragon

        return: None
        """
        img_path = f"images/players/{id}.png"
        super().__init__(img_path, Dragon.SCALE)
        self.id = id    # The id of the dragon is same as the id of its own cave
        self.img_path = img_path
        self.board_pos = None
        self.remaining_steps = None

    def get_id(self):
        """
        The getter method to return the id of the dragon.

        return: int
        """
        return self.id

    def get_img_path(self):
        """
        The getter method to return the image path of the dragon.

        return: str
        """
        return self.img_path

    def get_board_pos(self):
        """
        The getter method to return the board position of the dragon.

        return: int
        """
        return self.board_pos

    def get_remaining_steps(self):
        """
        The getter method to return the remaining steps of the dragon.

        return: int
        """
        return self.remaining_steps

    def set_id(self, id):
        """
        The setter method to set the id of the dragon.

        input:
        - id: the id of the dragon

        return: None
        """
        self.id = id

    def set_pos(self, new_board_pos, new_xy):
        """
        The setter method to set the position of the dragon.

        input:
        - new_board_pos: the new board position of the dragon
        - new_xy: the new x and y display coordinate of the dragon 
                  (in tuple)

        return: None
        """
        self.board_pos = new_board_pos
        super().set_pos(new_xy[0]+10, new_xy[1])

    def set_remaining_steps(self, steps):
        """
        The setter method to set the remaining steps of the dragon.

        input:
        - steps: the remaining steps of the dragon

        return: None
        """
        self.remaining_steps = steps

    def save(self):
        """
        This method is used to save the dragon object.

        return: dict
        """
        return {
            "board_pos": self.board_pos,
            "remaining_steps": self.remaining_steps
        }

    def load(self, state):
        """
        This method is used to load the dragon object.

        input:
        - state: the dragon state to load

        return: None
        """
        self.set_remaining_steps(state["remaining_steps"])

    def move(self, destination, volcanoe_zones, caves):
        """
        This method moves the dragon to the destination.
        It sets the occupied status of the start land to False
        and the destination land to True.

        input:
        - destination: the destination index on the game board
        - volcanoe_zones: the list of volcanoes
        - caves: the list of caves

        return: None
        """
        # Obtain the starting land
        if self.board_pos is not None:
            if self.board_pos >= 0:
                vzone_index = self.board_pos // 3
                v_index = self.board_pos % 3
                start_land = volcanoe_zones[vzone_index].get_volcanoes()[
                    v_index]
            else:
                vol_pos = abs(self.board_pos) - 1
                vzone_index = vol_pos // 3
                v_index = vol_pos % 3
                volcano = volcanoe_zones[vzone_index].get_volcanoes()[v_index]
                start_land = caves[volcano.get_cave_id()]
            # Set the starting land's occupied status to False
            start_land.set_occupied_status(False)

        # Obtain the ending land
        if destination >= 0:
            vzone_index = destination // 3
            v_index = destination % 3
            end_land = volcanoe_zones[vzone_index].get_volcanoes()[v_index]
        else:
            vol_pos = abs(destination) - 1
            vzone_index = vol_pos // 3
            v_index = vol_pos % 3
            volcano = volcanoe_zones[vzone_index].get_volcanoes()[v_index]
            end_land = caves[volcano.get_cave_id()]

        # Move the dragon to the destination and update the occupied status
        end_land.set_occupied_status(True)
        self.set_pos(destination, end_land.get_pos())