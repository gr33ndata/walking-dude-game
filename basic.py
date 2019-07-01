import sys
import random
import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
SCREEN_TITLE = "Walking Dude"


class MyGame(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.GRAY)

    def setup(self):
        self.lives = 5
        self.protagonist_moves = 0

        self.protagonist = arcade.Sprite("u1.png", 0.25)
        self.protagonist.center_x = 50
        self.protagonist.center_y = SCREEN_HEIGHT / 2

    def on_draw(self):
        arcade.start_render()
        self.protagonist.draw()
        output = f"Lives: {self.lives}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

    def update_protagonist(self):
        if self.protagonist.center_y < 0:
            self.protagonist.center_y = 0
        elif self.protagonist.center_y > SCREEN_HEIGHT:
            self.protagonist.center_y = SCREEN_HEIGHT
        else:
            self.protagonist.center_y += self.protagonist_moves
            self.protagonist.set_position(
                center_x=self.protagonist.center_x,
                center_y=self.protagonist.center_y
            )

    def update_antagonists(self):
        pass

    def on_update(self, delta_time):
        self.update_protagonist()
        self.update_antagonists()

    def on_key_press(self, key, key_modifiers):
        if key == 113:
            arcade.close_window()
        elif key == arcade.key.UP:
            self.protagonist_moves = 10
        elif key == arcade.key.DOWN:
            self.protagonist_moves = -10
        else:
            self.protagonist_moves = 0

    def on_key_release(self, key, key_modifiers):
        self.protagonist_moves = 0


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    try:
        arcade.run()
    except:
        arcade.close_window()


if __name__ == "__main__":
    main()
