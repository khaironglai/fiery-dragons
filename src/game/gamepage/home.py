from gamepage.page import Page
from button import Button
from gamepage.setup import Setup
from display import Display
from save_manager import SaveManager

import pygame


class Home(Page):
    """ Home page of the game. """

    def __init__(self, page_controller, window):
        """
        This method initializes the home page.

        input:
        - page_controller: the page controller of the game
        - window: the window of the game

        return: None
        """
        super().__init__(page_controller, window)

    def run(self):
        """
        This method runs the home page.
        The home page has three buttons, start, resume and quit:

        - The start button will change the page to the setup page
          where the number of players of this game is input.

        - The resume button will change the page to the setup page
          where the player get to choose to resume their previous 
          saved game.

        - The quit button will quit the game.

        return: None
        """
        # Load images
        home_bg = Display.load_bg(
            self.window, 'images/backgrounds/home.png')
        start_button_img_path = 'images/buttons/start.png'
        resume_button_img_path = 'images/buttons/resume.png'
        quit_button_img_path = 'images/buttons/quit.png'

        # Set scale and create button instances
        start_button_scale = 0.3
        resume_button_scale = 0.2
        quit_button_scale = 0.2
        start_button = Button(start_button_img_path, start_button_scale)
        resume_button = Button(resume_button_img_path, resume_button_scale)
        quit_button = Button(quit_button_img_path, quit_button_scale)

        # Set the display position
        start_button.set_pos(self.window.get_width()//2,
                             self.window.get_height()//2)
        resume_button.set_pos(self.window.get_width()//2,
                              self.window.get_height()*2.3//3)
        quit_button.set_pos(self.window.get_width()//2,
                            self.window.get_height()*2.55//3)

        page = None
        run = True
        while run:
            self.window.blit(home_bg, (0, 0))
            start_button.draw(self.window)
            if SaveManager.has_save_file():
                resume_button.draw(self.window)
            quit_button.draw(self.window)

            if start_button.is_clicked():
                run = False
                page = Setup(self.page_controller, self.window, False)

            if resume_button.is_clicked():
                run = False
                page = Setup(self.page_controller, self.window, True)

            if quit_button.is_clicked():
                Display.quit()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Display.quit()

            pygame.display.update()

        self.change_page(page)