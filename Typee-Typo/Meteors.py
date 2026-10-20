import pygame
import random

class Meteors:
    meteor = pygame.image.load("Media/meteors/m1.png")
    meteor_pop = [
        pygame.image.load("Media/meteors/m%s.png" % img) for img in range(2, 5)
    ]
    meteor_array = []

    def __init__(self, game, word_meteor=False, word_x=0, word_y=0):
        self.img = Meteors.meteor
        size = self.img.get_size()
        self.width = size[0]
        self.height = size[1]
        if (word_meteor):
            self.x = word_x
            self.y = word_y
            self.popping = True
        else:
            self.x = random.randint(0, 2000)
            self.y = game.screenH + self.height
            self.popping = False
            self.startX = self.x
            self.speed = random.uniform(.5, 2)
            self.direction = random.choice(["right", "left"])
        self.pop_count = 1
        self.pop_FPS = 3
        self.bubbling = True


    #####################
    #   Event Handling  #
    #####################
    def pop_meteor(self, screen):
        if (self.popping):
            img = self.meteor_pop[self.pop_count // self.pop_FPS]
            screen.blit(img, (self.x, self.y))
            self.pop_count += 1
            if (self.pop_count > len(self.meteor_pop) + 1):
                return True
        return False

    def update_meteors(self, game):
        x = random.randint(1, 100)
        if x == 1:
            Meteors.meteor_array.append(Meteors(game))
        return

    def add_word_meteor(game, word, screen):
        image_size = game.menu_header.get_size()
        y_offset = word.y - image_size[1] / 2
        Meteors.meteor_array.append(Meteors(
            game,
            True,
            word.x,
            y_offset)
        )
        return

    def pop_word_meteors(screen):
        # Iterate over a copy: removing from the list being iterated skips items.
        for meteor in list(Meteors.meteor_array):
            if (meteor.pop_meteor(screen)):
                Meteors.meteor_array.remove(meteor)
        return


    #####################
    #      Drawing      #
    #####################
    def draw(self, screen, game):
        if not (self.popping):
            screen.blit(self.img, (self.x, self.y))
            self.y -= self.speed
            self.x -= self.speed
            if (self.x <= (0 - game.font_size - game.border_width)):
                self.popping = True
            elif (self.y <= (0 - game.font_size - game.border_width)):
                self.popping = True
        return

    def draw_meteors(self, game, screen):
        for meteor in list(Meteors.meteor_array):
            if not (meteor.draw(screen, game)):
                if (meteor.pop_meteor(screen)):
                    Meteors.meteor_array.remove(meteor)
        Meteors.update_meteors(self, game)
        return

    def draw_button_meteor(button, screen, game):
        # NOTE: unused at the moment (draw_buttons is never called with
        # game_button=True) and it refers to images the Game class doesn't load.
        text_size = game.text_size(button.text)

        if (button.text == "Mute"):
            image_size = game.game_button_left.get_size()
            x = button.x - text_size[0] / 2
            y = button.y - image_size[1] / 2 + text_size[1]
            screen.blit(game.game_button_left, (x, y))
        elif (button.text == "Speed"):
            image_size = game.game_button_right.get_size()
            x = button.x - text_size[0] / 2
            y = button.y - image_size[1] / 2 + text_size[1]
            screen.blit(game.game_button_right, (x, y))
        elif (button.text == "+"):
            pixel_y_offset = 12
            image_size = game.speed_up.get_size()
            speed_meteor_size = game.speed_image.get_size()
            x = button.x - image_size[0] + text_size[0]
            text_size = game.text_size("Speed")
            y = button.y - speed_meteor_size[1] + text_size[1] / 2 + pixel_y_offset
            screen.blit(game.speed_change, (x, y))
        elif (button.text == "-"):
            pixel_x_offset = 2
            pixel_y_offset = 5
            image_size = game.speed_down.get_size()
            speed_meteor_size = game.speed_image.get_size()
            x = button.x - image_size[0] / 2 - text_size[0] * 2 + pixel_x_offset
            text_size = game.text_size("Speed")
            y = button.y - speed_meteor_size[1] + text_size[1] / 2 + pixel_y_offset
            screen.blit(game.speed_change, (x, y))
        return

    def draw_corner_meteor(screen, game, left_meteor=False):
        image_size = game.right_corner.get_size()
        y = game.screenH - image_size[1] * game.meteor_y_offset
        if (left_meteor):
            x = 0 - image_size[0] * game.left_corner_x_offset
            screen.blit(game.left_corner, (x, y))
        else:
            x = game.screenW - image_size[0] * game.right_corner_x_offset
            screen.blit(game.right_corner, (x, y))
        return
