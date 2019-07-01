import sys
import random
import arcade

from sklearn.externals import joblib

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 300
SCREEN_TITLE = "Walking Dude"

class MyGame(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.GRAY)

    def setup(self):
        self.protagonist_moves = 0
        self.protagonist = arcade.Sprite("u1.png", 0.2)
        self.protagonist.center_x = 50
        self.protagonist.center_y = SCREEN_HEIGHT / 2

        self.num_antagonists = 2
        self.antagonists = {}

        self.died = 0

        for a in range(self.num_antagonists):
            self.antagonists[a] = arcade.Sprite("u2.png", 0.2)
            self.antagonists[a].center_x = SCREEN_WIDTH - 50
            self.antagonists[a].center_y = random.randint(0, SCREEN_HEIGHT)

        self.gamma = 0.05
        self.actions = [arcade.key.UP, arcade.key.DOWN, None]
        self.Q = {}
        try:
            self.Q = joblib.load('Q.pkl')
        except:
            pass

    def get_state(self):
        return [
            int((self.protagonist.center_y - self.antagonists[0].center_y) / 20),
            int((self.protagonist.center_y - self.antagonists[1].center_y) / 20),
            self.protagonist.center_y <= 20,
            self.protagonist.center_y >= (SCREEN_HEIGHT - 20)
            # min(
            #     self.antagonists[0].center_x,
            #     self.antagonists[1].center_x,
            # ),
            # self.antagonists[0].center_x,
            # self.antagonists[0].center_y,
            # self.antagonists[1].center_y,
        ]

    def on_draw(self):
        arcade.start_render()
        self.protagonist.draw()
        for a in range(self.num_antagonists):
            self.antagonists[a].draw()
        arcade.draw_text(f'Died: {self.died}', 10, 20, arcade.color.WHITE, 14)

    def update_protagonist(self):
        if self.protagonist.center_y < 0:
            self.protagonist.center_y = SCREEN_HEIGHT - 20
        elif self.protagonist.center_y > SCREEN_HEIGHT:
            self.protagonist.center_y = 20
        else:
            self.protagonist.center_y += self.protagonist_moves
            self.protagonist.set_position(
                center_x=self.protagonist.center_x,
                center_y=self.protagonist.center_y
            )

    def update_antagonists(self):
        for a in range(self.num_antagonists):
            if self.antagonists[a].center_x < 0:
                self.antagonists[a].center_x = SCREEN_WIDTH
                self.antagonists[a].center_y = random.randint(0, SCREEN_HEIGHT)
            elif self.antagonists[a].center_x > SCREEN_WIDTH:
                self.antagonists[a].center_x = 0
                self.antagonists[a].center_y = random.randint(0, SCREEN_HEIGHT)
            else:
                self.antagonists[a].center_x -= (1+a)*10
                self.antagonists[a].set_position(
                    center_x=self.antagonists[a].center_x,
                    center_y=self.antagonists[a].center_y
                )

    def on_update(self, delta_time):
        current_state = self.get_state()
        self.gamma -= 0.000001
        if random.randint(0, 100) <= self.gamma:
            chosen_action = random.choice(self.actions)
            print(self.gamma, chosen_action)
            next_q = self.Q.get(str(current_state + [chosen_action]), 0)
        else:
            chosen_action, chosen_q = sorted(
                [
                    (action, self.Q.get(str(current_state + [action]), 0))
                    for action in self.actions
                ],
                key=lambda x: x[1]
            )[-1]
        self.press_key(chosen_action)
        self.update_protagonist()
        self.release_key()
        self.update_antagonists()
        v = 0
        for a in range(self.num_antagonists):
            if arcade.check_for_collision(self.protagonist, self.antagonists[a]):
                self.died += 1
                v = -1
                self.antagonists[a].center_x = SCREEN_WIDTH - 50
                self.antagonists[a].center_y = random.randint(0, SCREEN_HEIGHT)
                self.protagonist.center_y = SCREEN_HEIGHT / 2
        _, next_q = sorted(
            [
                (action, self.Q.get(str(current_state + [action]), 0))
                for action in self.actions
            ],
            key=lambda x: x[1]
        )[-1]
        self.Q[
            str(current_state + [chosen_action])
        ] = next_q + 0.1 * v

    def press_key(self, key):
        if key == arcade.key.Q:
            print(self.gamma, self.Q)
            joblib.dump(self.Q, 'Q.pkl')
            arcade.close_window()
        elif key == arcade.key.UP:
            self.protagonist_moves = 20
        elif key == arcade.key.DOWN:
            self.protagonist_moves = -20
        else:
            self.protagonist_moves = 0

    def release_key(self):
        self.protagonist_moves = 0

    def on_key_press(self, key, key_modifiers):
        self.press_key(key)

    def on_key_release(self, key, key_modifiers):
        self.release_key()


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    try:
        arcade.run()
    except:
        arcade.close_window()


if __name__ == "__main__":
    main()
