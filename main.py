from kivy.app import App
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Line
from kivy.utils import get_color_from_hex


COLORS = {
    "Red": "#e53935",
    "Green": "#2e7d32",
    "Blue": "#1e88e5",
    "Yellow": "#fdd835",
    "Black": "#212121",
    "Orange": "#fb8c00",
    "Purple": "#8e24aa",
}


class ChessBoard(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.distance = dp(30)
        self.counter = 4
        self.board_color = COLORS["Red"]
        self.bind(pos=self.draw_board, size=self.draw_board)

    def configure(self, distance, counter, color):
        self.distance = dp(distance)
        self.counter = counter
        self.board_color = COLORS[color]
        self.size_hint = (None, None)
        side = self.distance * self.counter * 2
        self.size = (side, side)
        self.draw_board()

    def draw_board(self, *args):
        self.canvas.clear()
        n = self.counter * 2
        cell = self.distance

        with self.canvas:
            Color(1, 1, 1, 1)
            Rectangle(pos=self.pos, size=(n * cell, n * cell))

            for row in range(n):
                for col in range(n):
                    if (row + col) % 2 == 0:
                        Color(*get_color_from_hex(self.board_color))
                        Rectangle(
                            pos=(
                                self.x + col * cell,
                                self.y + row * cell
                            ),
                            size=(cell, cell)
                        )

            Color(0.1, 0.1, 0.1, 1)
            Line(
                rectangle=(self.x, self.y, n * cell, n * cell),
                width=1
            )


class CheckerboardApp(App):
    def build(self):
        self.title = "Checkerboard"

        root = BoxLayout(
            orientation="vertical",
            padding=dp(12),
            spacing=dp(8)
        )

        root.add_widget(Label(
            text="Checkerboard",
            font_size="22sp",
            size_hint_y=None,
            height=dp(42)
        ))

        self.distance_input = TextInput(
            text="30",
            hint_text="Distance: 5 to 100",
            multiline=False,
            input_filter="int",
            size_hint_y=None,
            height=dp(42)
        )

        self.counter_input = TextInput(
            text="4",
            hint_text="Counter: 1 to 20",
            multiline=False,
            input_filter="int",
            size_hint_y=None,
            height=dp(42)
        )

        self.color_spinner = Spinner(
            text="Red",
            values=tuple(COLORS.keys()),
            size_hint_y=None,
            height=dp(42)
        )

        for control in (
            self.distance_input,
            self.counter_input,
            self.color_spinner
        ):
            root.add_widget(control)

        button = Button(
            text="Draw Checkerboard",
            size_hint_y=None,
            height=dp(46)
        )
        button.bind(on_release=self.draw)
        root.add_widget(button)

        self.status = Label(
            text="Enter values and draw",
            size_hint_y=None,
            height=dp(35)
        )
        root.add_widget(self.status)

        scroll = ScrollView()
        self.board = ChessBoard()
        scroll.add_widget(self.board)
        root.add_widget(scroll)

        self.draw()
        return root

    def draw(self, *args):
        try:
            distance = int(self.distance_input.text)
            counter = int(self.counter_input.text)

            if not 5 <= distance <= 100:
                raise ValueError("Distance must be 5-100")

            if not 1 <= counter <= 20:
                raise ValueError("Counter must be 1-20")

            color = self.color_spinner.text
            self.board.configure(distance, counter, color)

            self.status.text = (
                f"Board: {counter * 2} x {counter * 2}"
            )

        except ValueError as error:
            self.status.text = str(error)


if __name__ == "__main__":
    CheckerboardApp().run()
