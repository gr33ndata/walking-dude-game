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
        self.lives = 50
        self.protagonist_moves = 0

        self.protagonist = arcade.Sprite("u1.png", 0.25)
        self.protagonist.center_x = 50
        self.protagonist.center_y = SCREEN_HEIGHT / 2

        self.antagonists = {}
        for a in range(2):
            self.antagonists[a] = arcade.Sprite("u2.png", 0.25)
            self.antagonists[a].center_x = SCREEN_WIDTH - 50
            self.antagonists[a].center_y = random.randint(0, SCREEN_HEIGHT)

    def on_draw(self):
        arcade.start_render()
        self.protagonist.draw()
        for a in range(2):
            self.antagonists[a].draw()
        if self.lives < 1:
            arcade.draw_text('Game Over', 10, 20, arcade.color.RED, 14)
        else:
            arcade.draw_text(f"Lives: {self.lives}", 10, 20, arcade.color.WHITE, 14)

    def update_protagonist(self):
        if self.lives < 1:
            return None
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
        for a in range(2):
            if self.antagonists[a].center_x < 0:
                self.antagonists[a].center_x = SCREEN_WIDTH
                self.antagonists[a].center_y = random.randint(0, SCREEN_HEIGHT)
            elif self.antagonists[a].center_x > SCREEN_WIDTH:
                self.antagonists[a].center_x = 0
                self.antagonists[a].center_y = random.randint(0, SCREEN_HEIGHT)
            else:
                self.antagonists[a].center_x -= (1+a)*5
                self.antagonists[a].set_position(
                    center_x=self.antagonists[a].center_x,
                    center_y=self.antagonists[a].center_y
                )

    def on_update(self, delta_time):
        self.update_protagonist()
        self.update_antagonists()
        for a in range(2):
            if arcade.check_for_collision(self.protagonist, self.antagonists[a]):
                self.lives -= 1
                self.antagonists[a].center_x = SCREEN_WIDTH - 50
        if self.lives < 1:
            self.protagonist.center_y = 2 * SCREEN_HEIGHT

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
