from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from random import randint


class SnakeGame(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.score = 0
        self.game_over = False
        self.direction = (1, 0)

        self.score_label = Label(
            text="Score: 0",
            font_size=24,
            size_hint=(None, None),
            pos=(10, 10)
        )
        self.add_widget(self.score_label)

        self.reset_game()
        Clock.schedule_interval(self.update, 0.12)

    def reset_game(self):
        self.snake = [(10, 10), (9, 10), (8, 10)]
        self.food = (randint(2, 37), randint(2, 23))
        self.score = 0
        self.game_over = False
        self.direction = (1, 0)
        self.score_label.text = "Score: 0"

    def update(self, dt):

        if self.game_over:
            return

        head_x, head_y = self.snake[0]
        dx, dy = self.direction

        new_head = (head_x + dx, head_y + dy)

        # Wall collision
        if (
            new_head[0] < 0 or new_head[0] > 39 or
            new_head[1] < 0 or new_head[1] > 25
        ):
            self.game_over = True
            self.score_label.text = f"GAME OVER  |  Score: {self.score}"
            return

        # Self collision
        if new_head in self.snake:
            self.game_over = True
            self.score_label.text = f"GAME OVER  |  Score: {self.score}"
            return

        self.snake.insert(0, new_head)

        # Food
        if new_head == self.food:
            self.score += 1
            self.food = (randint(2, 37), randint(2, 23))
            self.score_label.text = f"Score: {self.score}"
        else:
            self.snake.pop()

        self.draw_game()

    def draw_game(self):

        self.canvas.clear()

        cell = 20

        with self.canvas:

            # Snake
            Color(0, 1, 0)
            for x, y in self.snake:
                Rectangle(
                    pos=(x * cell, y * cell),
                    size=(cell - 2, cell - 2)
                )

            # Food
            Color(1, 0, 0)
            x, y = self.food
            Rectangle(
                pos=(x * cell, y * cell),
                size=(cell - 2, cell - 2)
            )

    def on_touch_down(self, touch):

        self.start_x = touch.x
        self.start_y = touch.y

        return True

    def on_touch_up(self, touch):

        dx = touch.x - self.start_x
        dy = touch.y - self.start_y

        # Restart after Game Over
        if self.game_over:
            self.reset_game()
            self.draw_game()
            return True

        # Swipe direction
        if abs(dx) > abs(dy):

            if dx > 30 and self.direction != (-1, 0):
                self.direction = (1, 0)

            elif dx < -30 and self.direction != (1, 0):
                self.direction = (-1, 0)

        else:

            if dy > 30 and self.direction != (0, -1):
                self.direction = (0, 1)

            elif dy < -30 and self.direction != (0, 1):
                self.direction = (0, -1)

        return True


class SnakeApp(App):

    def build(self):
        return SnakeGame()


SnakeApp().run()
