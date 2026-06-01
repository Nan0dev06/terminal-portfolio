from pathlib import Path

from textual.app import App, ComposeResult
from textual.widgets import Static
from textual.containers import Horizontal, Vertical
from textual.widgets import Static, Footer
from textual.theme import Theme
import pyfiglet
import random


ROOT = Path(__file__).resolve().parent

nano_green = Theme(
    name="nano-green",
    primary="#00FF41",
    secondary="#008F11",
    accent="#00FF41",
    foreground="#00FF41",
    background="#0D0208",
    success="#00FF41",
    warning="#FFD700",
    error="#FF0000",
    surface="#0D0208",
    panel="#0D0208",
    dark=True,
)

class TitleWithStars(Static):

    STAR_POSITIONS = [
        (0, 5),    #adjustable
        (0,15),
        (1, 2),
    ]

    def on_mount(self):
        
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
        self.full_text = """Nour Al Shami is a computer science student at USAL, building toward AI Engineering.
                            \nDrawn to machine perception, computer vision, and creative sides of code.

                            \nWhen not coding, she is deep in game lore or failing to teach her cat new tricks.
                            \nCurrently exploring the world of humanoid robotics and AI research."""
                                
        self.displayed = ""
        self.set_interval(0.03, self.type_next_char)

    def type_next_char(self):
        if len(self.displayed) < len(self.full_text):
            self.displayed += self.full_text[len(self.displayed)]
            self.update(self.displayed)  
        else:
            self.app.query_one(".links").display = True  
class PortfolioApp(App):
    CSS_PATH = "portfolio.tcss"
    BINDINGS = [
        ("t", "next_theme", "Theme"),
        ("q", "quit", "Quit"),
    ]
    def action_open_github(self):
        import webbrowser
        webbrowser.open("https://github.com/Nan0dev06")

    def action_open_linkedin(self):
        import webbrowser
        webbrowser.open("https://www.linkedin.com/in/nour-al-shami-3701a037a/")
    theme_index = 0
    def on_mount(self):
        self.register_theme(nano_green)
    def action_next_theme(self):
        themes = ["nord",
                  "gruvbox", 
                  "tokyo-night", 
                  "textual-dark", 
                  "atom-one-dark",
                  "nano-green"
                  ]
        self.theme_index = (self.theme_index + 1) % len(themes)
        self.theme = themes[self.theme_index]
        

    def compose(self) -> ComposeResult:
        with open(ROOT / "portrait.txt", "r", encoding="utf-8") as f:
            portrait = f.read()
        yield Static("01001000 01100101 01101100 01101100 01101111 00100000 01010111 01101111 01110010 01101100 01100100", classes="header-binary")    
        with Horizontal():
            yield Static(portrait, classes="portrait")
            with Vertical(classes="right-panel"):
                yield TitleWithStars(classes="title")
                yield TypingText( classes="bio")
                yield Static("""
                            [dim]----------------------------------------[/dim]
                            [bold]GitHub[/bold]    [@click='app.open_github']@Nan0dev06[/]
                            [bold]Email[/bold]     nano.06dev@gmail.com
                            [bold]LinkedIn[/bold]  [@click='app.open_linkedin']/in/nour-al-shami[/]
""", classes="links", markup=True)
        yield Footer()

if __name__ == "__main__":
    app = PortfolioApp()
    app.run()
