from board.cave import Cave
from board.volcano_zone import VolcanoZone
from board.land_type import LandType
from gamecard.animal_type import AnimalType
from memorable import Memorable

import random
import pygame
import math


class GameBoard(Memorable):
    """
    This class is used to create the gameboard.
    The gameboard contains the caves and volcanoe zones.
    The gameboard manages the creation and arrangement of the caves and 
    volcanoe zones.
    """
    MIN_CAVE = 4    # Minimum number of caves

    def __init__(self, window, seed, dragons, size, animal_num, cave_pos_ls):
        """
        This method initializes the gameboard.

        input:
        - window: the pygame window
        - seed: the random seed for randomization
        - dragons: the list of dragons
        - size: the number of volcanoes
        - animal_num: the number of animal types
        - cave_pos_ls: the list of cave positions (if set by players)

        return: None
        """
        self.window = window
        self.seed = seed
        self.size = size
        self.animal_num = animal_num
        self.volcanoe_zones = self._create_vzones()
        self.caves = self._create_caves(dragons, cave_pos_ls)
        self._set_position(dragons)

    def get_volcanoe_zones(self):
        """
        The getter method to return the volcano zones list.

        return: list
        """
        return self.volcanoe_zones

    def get_caves(self):
        """
        The getter method to return the caves.

        return: list
        """
        return self.caves

    def draw(self):
        """
        This method is used to draw the gameboard on the window display.

        return: None
        """
        self.window.fill((221, 209, 178))
        for volcano_zone in self.volcanoe_zones:
            for volcano in volcano_zone.get_volcanoes():
                volcano.draw(self.window)
        for cave in self.caves:
            cave.draw(self.window)

    def save(self):
        """
        This method is used to save the gameboard object.
        Currently, the volcano zones and caves are saved.

        return: dict
        """
        return {
            "volcanoe_zones": [volcano_zone.save() for volcano_zone in self.volcanoe_zones],
            "caves": [cave.save() for cave in self.caves]
        }

    def load(self, state):
        """
        This method is used to load the gameboard object.

        input:
        - state: the gameboard state to load

        return: None
        """
        for i in range(len(self.volcanoe_zones)):
            self.volcanoe_zones[i].load(state["volcanoe_zones"][i])

    def _create_caves(self, dragons, cave_pos_ls):
        """
        This method creates the caves.
        The minimum number of caves is 4.

        input:
        - dragons: the list of dragons
        - cave_pos_ls: the list of cave positions (if set by players)

        return: list
        """
        caves_num = max(GameBoard.MIN_CAVE, len(dragons))
        # Cave default position
        if cave_pos_ls is None:
            cave_distance = int(self.size / caves_num)
            # cave_pos_ls = [i for i in range(0, self.size, cave_distance)]
            cave_pos_ls = [-(i+1) for i in range(0, self.size, cave_distance)]

            # For default cave position, 2 players game will have caves opposite to each other
            if len(dragons) == 2:
                dragons[-1].set_id(2)

        # Create caves
        caves = []
        for i in range(caves_num):
            cave = Cave(i, AnimalType(i), LandType.CAVE, cave_pos_ls[i])
            caves.append(cave)
            vol_pos = abs(cave_pos_ls[i]) - 1
            vzone_index = vol_pos // 3
            v_index = vol_pos % 3
            volcanoes = self.volcanoe_zones[vzone_index].get_volcanoes()
            # Mark the cave id on the corresponding volcano
            volcanoes[v_index].set_cave_id(i)

        return caves

    def _create_vzones(self, volcano_zone_size=3):
        """
        This method creates the volcanoe zones.

        input:
        - volcano_zone_size: the size of the volcano zone

        return: list
        """
        # Create animal list
        animal_ls = []
        # A total of (board_size/animal_num) volcanoes will be created for
        # each type of animal
        for i in range(self.animal_num):
            for _ in range(int(self.size//self.animal_num)):
                animal_ls.append(AnimalType(i))
        # Shuffle the animal list (same as shuffling the final volcano zones outcome)
        random.seed(self.seed)
        random.shuffle(animal_ls)

        # Create volcanoe zones
        volcano_zones = []
        for i in range(0, len(animal_ls), volcano_zone_size):
            zone_animal_ls = animal_ls[i:i+volcano_zone_size]
            volcano_zones.append(VolcanoZone(zone_animal_ls))

        # return volcanoe zones
        return volcano_zones

    def _set_position(self, dragons):
        """
        This method sets the display position of the caves and volcanoes.

        input:
        - dragons: the list of dragons

        return: None
        """
        window_w = self.window.get_width()
        window_h = self.window.get_height()

        self._set_cave_pos(window_w, window_h)
        self._set_vol_pos(window_w, window_h)
        self._set_dragon_pos(dragons)

    def _set_cave_pos(self, window_w, window_h):
        """
        This method sets the display position of the caves.
        It arranges the caves in a circular pattern where the radius is 
        slightly larger than the volcanoes' circular pattern.
        Tile size and tile density control the radius of the circular 
        pattern.
        The higher the tile density, the smaller the interval between the 
        caves.

        input:
        - window_w: the width of the window
        - window_h: the height of the window

        return: None
        """
        tile_num = self.size
        tile_size = 51.5
        tile_density = 4.5

        for cave in self.caves:
            i = abs(cave.get_board_pos()) - 1
            x = window_w // 2 + (tile_size * (tile_num // tile_density)) * (
                pygame.math.Vector2(1, 0).rotate_rad(
                    i * 2 * math.pi / tile_num)
            ).x
            y = window_h // 2 + (tile_size * (tile_num // tile_density)) * (
                pygame.math.Vector2(1, 0).rotate_rad(
                    i * 2 * math.pi / tile_num)
            ).y
            cave.set_pos(x, y)

    def _set_vol_pos(self, window_w, window_h):
        """
        This method sets the display position of the volcanoes.
        It arranges the volcanoes in a circular pattern where the radius is 
        slightly smaller than the caves' circular pattern.
        Tile size and tile density control the radius of the circular 
        pattern.
        The higher the tile density, the smaller the interval between the 
        volcanoes.

        input:
        - window_w: the width of the window
        - window_h: the height of the window

        return: None
        """
        tile_num = self.size
        tile_size = 43
        tile_density = 4.5

        for i in range(tile_num):
            x = window_w // 2 + (tile_size * (tile_num // tile_density)) * (
                pygame.math.Vector2(1, 0).rotate_rad(
                    i * 2 * math.pi / tile_num)
            ).x
            y = window_h // 2 + (tile_size * (tile_num // tile_density)) * (
                pygame.math.Vector2(1, 0).rotate_rad(
                    i * 2 * math.pi / tile_num)
            ).y

            vzone_index = i // 3
            v_index = i % 3
            volcanoes = self.volcanoe_zones[vzone_index].get_volcanoes()
            volcanoes[v_index].set_pos(x, y)

    def _set_dragon_pos(self, dragons):
        """
        This method sets the starting position of the dragons on the caves.

        input:
        - dragons: the list of dragons

        return: None
        """
        # Set the starting position of the players on the board
        for i in range(len(dragons)):
            index = dragons[i].get_id()    # The index of the cave
            starting_point = self.caves[index].get_board_pos()
            dragons[i].move(starting_point, self.volcanoe_zones, self.caves)
            # Set the remaining steps of the dragons
            dragons[i].set_remaining_steps(self.size + 2)