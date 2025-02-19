from button import Button
from gamecard.card import Card
from display import Display
from memorable import Memorable


from abc import abstractmethod
import pygame


class ChitCard(Button, Card, Memorable):
    """
    This class is used to create a chit card object.
    A chit card is what the player choose and flip to reveal the animal 
    type. If the animal type matches, they can move forward in the game.

    Animal type         : bat, baby dragon, salamander, spider
    Penalty animal type : dragon pirate
    Special animal type : dragon spirit
    """
    BACK_IMG_PATH = "images/chit cards/card back.png"
    SCALE = 0.05

    def __init__(self, animal, animal_num, front_image_path):
        """
        This method initializes the chit card object.

        input:
        - animal: the animal type of the chit card
        - animal_num: the animal number on the chit card
        - front_image_path: the path of the front image of the chit card

        return: None
        """
        Button.__init__(self, ChitCard.BACK_IMG_PATH, ChitCard.SCALE)
        Card.__init__(self, animal)
        self.animal_num = animal_num
        self.reveal = False  # To detect whether the card is flipped
        self.front_image = Display.load_img(front_image_path, ChitCard.SCALE)
        self.back_image = Display.load_img(
            ChitCard.BACK_IMG_PATH, ChitCard.SCALE)

    def is_clicked(self):
        """
        This method checks if the chit card is clicked.
        If the chit card is clicked, the method returns True and the front 
        image of the chit card is shown.
        It cannot be clicked anymore until the next player's turn.

        return: bool
        """
        rect = self.image.get_rect()
        rect.center = (self.x, self.y)

        pos = pygame.mouse.get_pos()
        if rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and not self.clicked and not self.reveal:
                self.clicked = True
                self.set_reveal_true()
                return True
        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False

    def get_animal_num(self):
        """
        The getter method return the animal number on the chit 
        card.

        return: int
        """
        return self.animal_num

    def set_reveal_true(self):
        """
        This method sets the reveal attribute to True
        and change the display image to the front image.

        return: None
        """
        self.reveal = True
        self.image = self.front_image

    def save(self):
        """
        This method is used to save the chit card object.

        return: dict
        """
        return {
            "reveal": self.reveal
        }

    def load(self, state):
        """
        This method is used to load the chit card object.

        input:
        - state: the chit card state to load

        return: None
        """
        if state["reveal"]:
            self.set_reveal_true()

    def reset(self):
        """
        This method resets the chit card to its original state.
        Usually trigered when it is the turn of the next player.

        return: None
        """
        self.reveal = False
        self.image = self.back_image

    def valid_dragon(self, dragons, volcanoe_zones, caves):
        """
        This method checks if any dragon is valid to move 
        based on the animal on the chit card.

        input:
        - dragons: the list of dragons
        - volcanoe_zones: the list of volcanoes
        - caves: the list of caves

        return: list of dragons
        """
        valid_dragons = []
        for dragon in dragons:
            pos = dragon.get_board_pos()
            # Get the volcano the dragon is currently on
            vzone_index = pos // 3
            v_index = pos % 3
            volcano = volcanoe_zones[vzone_index].get_volcanoes()[v_index]
            if pos >= 0:
                vzone_index = pos // 3
                v_index = pos % 3
                land = volcanoe_zones[vzone_index].get_volcanoes()[v_index]
            # Get the cave the dragon is currently on
            else:
                vol_pos = abs(pos) - 1
                vzone_index = vol_pos // 3
                v_index = vol_pos % 3
                volcano = volcanoe_zones[vzone_index].get_volcanoes()[v_index]
                land = caves[volcano.get_cave_id()]
            if land.get_animal() == self.get_animal():
                valid_dragons.append(dragon)
        return valid_dragons

    @abstractmethod
    def get_action(self, dragon, volcanoe_zones, caves):
        """
        This method is an abstract method that is used to define the 
        action of the chit card. The specific action should be 
        determine the specific chit card

        input:
        - dragon: the dragon object
        - volcanoe_zones: the list of volcanoes
        - caves: the list of caves

        return: MoveAction
        """
        pass