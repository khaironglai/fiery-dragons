from gamepage.page import Page
from display import Display
from gamepage.game import Game
from save_manager import SaveManager

import pygame
import time
import random
import json


class Setup(Page):
    """
    Setup page of the game.
    Used to get the number of players from the user
    or prompt the user to choose the previous game
    saved.
    """

    def __init__(self, page_controller, window, resume=False):
        """
        This method initializes the setup page.

        input:
        - page_controller: the page controller of the game
        - window: the window of the game
        - resume: boolean value to check if the player wants to resume the game

        return: None
        """
        super().__init__(page_controller, window)
        self.resume = resume

    def run(self):
        """
        This method runs the setup page.

        return: None
        """
        page = None
        # For new game (prompt the user to input the number of players)
        if not self.resume:
            player_num = self._get_player_num()
            seed = random.randint(0, 1000)  # Seed for randomization
            page = Game(self.page_controller, self.window, seed,
                        player_num)
        # For resuming game (prompt the user to choose the previous game saved)
        else:
            files = SaveManager.show_save_files()
            file_num = self._get_file_num(files)
            file_path = files[file_num-1][0]

            # file_path = "src/memory/testsave.json"
            with open(file_path, "r") as file:
                game_state = json.load(file)

            game = Game(self.page_controller, self.window, game_state["seed"], game_state["player_num"], game_state[
                        "dragon_num"], game_state["size"], game_state["animal_num"], game_state["gameboard"]["caves"], game_state["current_player"], game_state["card_reveal"])
            game.load(file_path)
            page = game
        self.change_page(page)

    def _get_file_num(self, files):
        """
        Get the saved file index from the user.

        input:
        - files: list of saved files

        return: int
        """
        # Load image
        setup_bg = Display.load_bg(
            self.window, 'images/backgrounds/setup.png')

        input = ""
        run = True
        while run:
            self.window.blit(setup_bg, (0, 0))

            Display.draw_text(self.window,
                              "Please choose the file you would like to resume with:", 24,
                              (0, 0, 0), self.window.get_width()//2,
                              self.window.get_height()//4.5, False)

            # Show the date of the saved files for the player to choose
            for i in range(len(files)):
                Display.draw_text(self.window,
                                  f"{i+1}:    {files[i][1]}", 24,
                                  (0, 0, 0), self.window.get_width()//2,
                                  self.window.get_height()//3.5*(1+(i/7)), False)

            Display.draw_text(self.window, input, 32, (255, 255, 255),
                              self.window.get_width()//2,
                              self.window.get_height()*1.5//3, True)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Display.quit()
                elif event.type == pygame.KEYDOWN:
                    # Check if the user pressed enter (indicates the user
                    # has finished the input)
                    if event.key == pygame.K_RETURN:
                        # Check valid input
                        valid = [str(i) for i in range(1, len(files)+1)]
                        if input in valid:
                            return int(input)
                        # If input is invalid, display error message and
                        # prompt user to input again
                        else:
                            input = ""
                            self.window.blit(setup_bg, (0, 0))
                            Display.draw_text(self.window, "Invalid input!",
                                              50, (255, 255, 255),
                                              self.window.get_width()//2,
                                              self.window.get_height()*1.6//4)
                            time.sleep(1)
                    # Check if the user pressed backspace
                    elif event.key == pygame.K_BACKSPACE:
                        input = input[:-1]
                    else:
                        input += event.unicode

    def _get_player_num(self):
        """
        Get the number of players from the user.
        If the input is invalid, display an error message and ask for 
        input again.

        return: int
        """
        # Load image
        setup_bg = Display.load_bg(
            self.window, 'images/backgrounds/setup.png')

        input = ""
        run = True
        while run:
            self.window.blit(setup_bg, (0, 0))
            Display.draw_text(self.window,
                              "Enter the number of players. (2-4)", 24,
                              (255, 255, 255), self.window.get_width()//2,
                              self.window.get_height()//3, False)

            Display.draw_text(self.window, input, 32, (255, 255, 255),
                              self.window.get_width()//2,
                              self.window.get_height()*1.5//3, True)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Display.quit()
                elif event.type == pygame.KEYDOWN:
                    # Check if the user pressed enter (indicates the user
                    # has finished the input)
                    if event.key == pygame.K_RETURN:
                        # Check valid input
                        valid = ['2', '3', '4']
                        if input in valid:
                            return int(input)
                        # If input is invalid, display error message and
                        # prompt user to input again
                        else:
                            input = ""
                            self.window.blit(setup_bg, (0, 0))
                            Display.draw_text(self.window, "Invalid input!",
                                              50, (255, 255, 255),
                                              self.window.get_width()//2,
                                              self.window.get_height()*1.6//4)
                            time.sleep(1)
                    # Check if the user pressed backspace
                    elif event.key == pygame.K_BACKSPACE:
                        input = input[:-1]
                    else:
                        input += event.unicode