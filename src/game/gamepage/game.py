from gamepage.page import Page
from gamepage.end import End
from display import Display
from player import Player
from board.gameboard import GameBoard
from gamecard.cc_bat import BatCC
from gamecard.cc_babydragon import BabyDragonCC
from gamecard.cc_salamander import SalamanderCC
from gamecard.cc_spider import SpiderCC
from gamecard.cc_dragonpirate import DragonPirateCC
from gamecard.cc_dragonspirit import DragonSpiritCC
from save_manager import SaveManager

import pygame
import random
import time
import json


class Game(Page):
    """
    This class is used to create a game object.
    The game object is the main object that controls the game.
    It is responsible for creating the gameboard, dragons and chit cards.
    It controls the overall game logic.
    """

    def __init__(self, page_controller, window, seed, player_num, 
                 dragon_num=1, size=24, animal_num=4, cave_pos_ls=None, 
                 current_player=0, card_reveal=0):
        """
        This method initializes the game object.

        input:
        - page_controller: the page controller object
        - window: the window object
        - seed: the seed for randomization
        - player_num: the number of players
        - dragon_num: the number of dragons each player can possess
        - size: the number of volcanoes on the gameboard
        - animal_num: the number of animal types in the game
        - cave_pos_ls: the list of cave positions (if determine by player)
        - current_player: the current player index
        - card_reveal: the number of chit cards revealed

        return: None
        """
        super().__init__(page_controller, window)
        self.seed = seed  # Seed for randomization
        self.player_num = player_num
        self.dragon_num = dragon_num
        self.size = size
        self.animal_num = animal_num
        self.players = self._create_players()
        self.chit_cards = self._create_cc()
        self._set_cc_pos()
        self.gameboard = self._create_gameboard(cave_pos_ls)
        self.current_player = current_player    # Track the current player
        self.card_reveal = card_reveal          # Track the number of chit cards revealed
        # If not none, this game is loaded from a file, and if this game ends successfully, the file will be cleared
        self.load_file_path = None

    def run(self):
        """ 
        The game engine.
        Handle the game logic.
        If the game ends, the game will change to the end page.

        return: None
        """
        end = False
        self.update_gameboard()
        while not end:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Display.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                        # If the game is loaded from a file, save the game to the same file
                        if self.load_file_path is None:
                            file_path = SaveManager.get_save_file_path()
                        else:
                            file_path = self.load_file_path
                        self.save(file_path)
                        Display.draw_text(self.window, "Game saved", 25, (0, 0, 0), 
                                          self.window.get_width()//2, self.window.get_height()//2)
                        time.sleep(1)
                        self.update_gameboard()

            end_turn = False

            # Check if all chit cards are revealed
            if self.card_reveal > len(self.chit_cards) - 1:
                self._next_player()

            cc = None   # Store the chosen chit card
            for chit_card in self.chit_cards:
                # If a chit card is clicked
                if chit_card.is_clicked():
                    self.update_gameboard()
                    cc = chit_card
                    self.card_reveal += 1
                    break

            player = self.players[self.current_player]

            if cc is None:
                continue

            else:
                dragons = player.get_dragons()
                valid_dragons = cc.valid_dragon(
                    dragons, self.gameboard.get_volcanoe_zones(), self.gameboard.get_caves())
                if len(valid_dragons) < 1:
                    end_turn = True
                else:
                    dragon = player.choose_dragon(valid_dragons)
                    action = cc.get_action(
                        dragon, self.gameboard.get_volcanoe_zones(), self.gameboard.get_caves())
                    end_turn, end = action.execute()
                    self.update_gameboard()

            # if the player's turn ends, change to the next player and reset
            # the chit cards
            if end_turn:
                self._next_player()

        # Change to end page to show the winner
        Display.draw_text(self.window, "GAME OVER", 70, (0, 0, 0),
                          self.window.get_width()//2,
                          self.window.get_height()//2)
        time.sleep(1)
        # Clear memory if the loaded game ends successfully
        if self.load_file_path is not None:
            with open(self.load_file_path, "w") as file:
                file.truncate()
        self.change_page(
            End(self.page_controller, self.window, player.get_id(), dragon.get_img_path()))

    def _next_player(self):
        """
        This method is used to change the turn to the next player.
        The current player index will be increment by 1.
        All the chit cards will be reset.

        return: None
        """
        self.current_player = (self.current_player + 1) % self.player_num
        self.card_reveal = 0
        for chit_card in self.chit_cards:
            chit_card.reset()

        time.sleep(1)
        self.update_gameboard()

        Display.draw_text(self.window, f"Player {self.current_player + 1}'s turn",
                          25, (0, 0, 0), self.window.get_width()//2,
                          self.window.get_height()//2)
        time.sleep(1)
        self.update_gameboard()

    def update_gameboard(self):
        """
        This method updates the display of the game if there is any player 
        movement or flipping of chit cards, etc.

        return: None
        """
        self.gameboard.draw()
        self._draw_game_element()
        pygame.display.update()

    def save(self, file_path):
        """
        This method is used to save the game state.
        The game state is saved in a json file.

        return: None
        """
        game_state = {
            "seed": self.seed,
            "player_num": self.player_num,
            "dragon_num": self.dragon_num,
            "size": self.size,
            "animal_num": self.animal_num,
            "current_player": self.current_player,
            "card_reveal": self.card_reveal,
            "players": [player.save() for player in self.players],
            "chit_cards": [chit_card.save() for chit_card in self.chit_cards],
            "gameboard": self.gameboard.save()
        }
        with open(file_path, "w") as file:
            json.dump(game_state, file)

    def load(self, file_path):
        """
        This method is used to load the game state from a json file.
        
        input:
        - file_path: the file path of the json file to load
        
        return: None
        """
        self.load_file_path = file_path
        with open(file_path, "r") as file:
            game_state = json.load(file)

        for i in range(len(self.chit_cards)):
            self.chit_cards[i].load(game_state["chit_cards"][i])

        self.gameboard.load(game_state["gameboard"])

        for i in range(self.player_num):
            self.players[i].load(game_state["players"][i])

        # Move dragon to the correct position
        for i in range(self.player_num):
            for j in range(self.dragon_num):
                self.players[i].get_dragons()[j].move(game_state["players"][i]["dragons"][j]["board_pos"], 
                                                      self.gameboard.get_volcanoe_zones(), 
                                                      self.gameboard.get_caves())

    def _draw_game_element(self):
        """
        This method draws the chit card and dragons on the window.

        return: None
        """
        self._draw_chit_cards()
        self._draw_dragons()

    def _draw_dragons(self):
        """
        This method draws the dragons on the window.

        return: None
        """
        for player in self.players:
            player.draw(self.window)

    def _draw_chit_cards(self):
        """
        This method draws the chit cards on the window.

        return: None
        """
        for chit_card in self.chit_cards:
            chit_card.draw(self.window)

    def _create_players(self):
        """
        This method creates the dragons.

        return: list
        """
        players = []
        for i in range(self.player_num):
            players.append(Player(i, self.dragon_num))

        return players

    def _create_cc(self):
        """
        This method creates the chit cards list

        return: list
        """
        # Create chit cards
        chit_cards = []
        for i in range(1, 4):
            chit_cards.append(BatCC(i))
            chit_cards.append(BabyDragonCC(i))
            chit_cards.append(SalamanderCC(i))
            chit_cards.append(SpiderCC(i))

            # For penalty card
            if i < 3:
                chit_cards.append(DragonPirateCC(i))

        # Create the dragon spirit chit card
        for _ in range(2):
            chit_cards.append(DragonSpiritCC())

        # Randomize the chit cards
        random.seed(self.seed)
        random.shuffle(chit_cards)
        return chit_cards

    def _set_cc_pos(self):
        """
        This method sets the chit cards position on the window.

        return: None
        """
        x_pos = []
        y_pos = []
        window_w = self.window.get_width()
        window_h = self.window.get_height()
        interval = 75   # The interval between each chit card
        for i in range(1, 4, 2):
            x_pos.append(int(window_w/2 + interval*i/2))
            x_pos.append(int(window_w/2 - interval*i/2))
            y_pos.append(int(window_h/2 + interval*i/2))
            y_pos.append(int(window_h/2 - interval*i/2))

        pos_tuple = [(x, y) for x in x_pos for y in y_pos]

        for i in range(len(self.chit_cards)):
            self.chit_cards[i].set_pos(pos_tuple[i][0], pos_tuple[i][1])

    def _create_gameboard(self, cave_pos_ls):
        """
        This method creates the gameboard.

        input:
        - cave_pos_ls: the list of cave positions (if determine by player)

        return: GameBoard
        """
        dragons = []
        for player in self.players:
            dragons.extend(player.get_dragons())
        return GameBoard(self.window, self.seed, dragons, 
                         self.size, self.animal_num, cave_pos_ls)