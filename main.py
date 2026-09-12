
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.metrics import dp
import math


# رنگ‌ها
BG = (0.04, 0.06, 0.12, 1)
DISPLAY_BG = (0.01, 0.02, 0.05, 1)
NUMBER = (0.10, 0.14, 0.22, 1)
OPERATOR = (0.35, 0.15, 0.65, 1)
SPECIAL = (0.15, 0.20, 0.28, 1)
EQUAL = (0.02, 0.70, 0.80, 1)
DANGER = (0.90, 0.15, 0.20, 1)

Window.clearcolor = BG


class Calculator(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = "vertical"
        self.padding = dp(15)
        self.spacing = dp(10)

        # -------------------------
        # نمایشگر
        # -------------------------

        self.display = TextInput(
            text="",
            font_size=dp(32),
            halign="right",
            multiline=False,
            readonly=True,
            background_color=DISPLAY_BG,
            foreground_color=(0.4, 0.9, 1, 1),
            cursor_color=(0.4, 0.9, 1, 1),
            padding=[dp(10), dp(20)]
        )

        self.add_widget(self.display)

        # -------------------------
        # دکمه‌ها
        # -------------------------

        buttons = GridLayout(
            cols=4,
            spacing=dp(7),
            size_hint_y=0.75
        )

        keys = [
            ("AC", DANGER),
            ("⌫", SPECIAL),
            ("%", SPECIAL),
            ("÷", OPERATOR),

            ("7", NUMBER),
            ("8", NUMBER),
            ("9", NUMBER),
            ("×", OPERATOR),

            ("4", NUMBER),
            ("5", NUMBER),
            ("6", NUMBER),
            ("-", OPERATOR),

            ("1", NUMBER),
            ("2", NUMBER),
            ("3", NUMBER),
            ("+", OPERATOR),

            ("0", NUMBER),
            (".", NUMBER),
            ("(", SPECIAL),
            (")", SPECIAL),

            ("√", SPECIAL),
            ("x²", SPECIAL),
            ("±", SPECIAL),
            ("=", EQUAL),
        ]

        for text, color in keys:

            button = Button(
                text=text,
                font_size=dp(22),
                bold=True,
                background_normal="",
                background_color=color,
                color=(1, 1, 1, 1)
            )

            button.bind(
                on_press=lambda instance, value=text:
                self.button_pressed(value)
            )

            buttons.add_widget(button)

        self.add_widget(buttons)

    # -------------------------
    # دکمه‌ها
    # -------------------------

    def button_pressed(self, value):

        if value == "AC":
            self.display.text = ""

        elif value == "⌫":
            self.display.text = self.display.text[:-1]

        elif value == "=":
            self.calculate()

        elif value == "%":
            self.percent()

        elif value == "√":
            self.sqrt()

        elif value == "x²":
            self.square()

        elif value == "±":
            self.change_sign()

        else:
            self.display.text += value

    # -------------------------
    # محاسبه
    # -------------------------

    def calculate(self):

        expression = self.display.text

        try:

            expression = expression.replace("×", "*")
            expression = expression.replace("÷", "/")
            expression = expression.replace("^", "**")

            result = eval(
                expression,
                {"__builtins__": None},
                {
                    "pi": math.pi,
                    "e": math.e
                }
            )

            if isinstance(result, float):
                result = round(result, 10)

            self.display.text = str(result)

        except ZeroDivisionError:
            self.display.text = "Cannot divide by zero"

        except:
            self.display.text = "Error"

    # -------------------------
    # درصد
    # -------------------------

    def percent(self):

        try:
            value = float(self.display.text)
            self.display.text = str(value / 100)

        except:
            self.display.text = "Error"

    # -------------------------
    # جذر
    # -------------------------

    def sqrt(self):

        try:
            value = float(self.display.text)

            if value < 0:
                self.display.text = "Error"
            else:
                self.display.text = str(math.sqrt(value))

        except:
            self.display.text = "Error"

    # -------------------------
    # توان دو
    # -------------------------

    def square(self):

        try:
            value = float(self.display.text)
            self.display.text = str(value ** 2)

        except:
            self.display.text = "Error"

    # -------------------------
    # تغییر علامت
    # -------------------------

    def change_sign(self):

        try:
            value = float(self.display.text)
            self.display.text = str(-value)

        except:
            self.display.text = "Error"


class NeoCalculatorApp(App):

    def build(self):

        self.title = "Neo Calculator"

        return Calculator()


if __name__ == "__main__":
    NeoCalculatorApp().run()

