from textual.app import App, ComposeResult
from textual.widgets import Static
from textual.containers import Horizontal, Vertical
import pyfiglet
import random

class TitleWithStars(Static):

    STAR_POSITIONS = [
        (0, 5),    #adjustable
        (0,15),
        (1, 2),
    ]

    def on_mount(self):
        import pyfiglet
        self.title_text = pyfiglet.figlet_format("Nano", font="slant")
        self.set_interval(0.5, self.render_all)

    def render_all(self):
        chars = ["*", ".", "+", "`", " ", " "]
        rows = 3
        cols = 25
        grid = [[" "] * cols for _ in range(rows)]
        for row,col in self.STAR_POSITIONS:
            grid[row][col] = random.choice(chars)
        stars = "\n".join("".join(r) for r in grid)
        self.update(stars + "\n" + self.title_text)

class TypingText(Static):

    def on_mount(self):
        self.full_text = "Nour Al Shami is a computer science student at USAL, building toward AI Engineering.\n Drawn to machine perception, computer vision, and creative sides of code.\n\nWhen not coding, she is deep in game lore or failing to teach her cat new tricks.\nCurrently exploring the world of humanoid robotics and AI research."
        self.displayed = ""
        self.set_interval(0.05, self.type_next_char)

    def type_next_char(self):
        if len(self.displayed) < len(self.full_text):
            self.displayed += self.full_text[len(self.displayed)]
            self.update(self.displayed)    
class PortfolioApp(App):
    CSS_PATH = "portfolio.tcss"

    def compose(self) -> ComposeResult:
        with open("portrait.txt", "r", encoding="utf-8") as f:
            portrait = f.read()
        with Horizontal():
            yield Static(portrait, classes="portrait")
            with Vertical(classes="right-panel"):
                yield TitleWithStars(classes="title")
                yield TypingText( classes="bio")

if __name__ == "__main__":
    app = PortfolioApp()
    app.run()