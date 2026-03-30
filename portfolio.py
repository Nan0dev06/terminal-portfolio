from textual.app import App, ComposeResult
from textual.widgets import Static

class PortfolioApp(App):
    def compose(self) -> ComposeResult:
        with open("portrait.txt", "r", encoding="utf-8") as f:
            portrait = f.read()
        yield Static(portrait)

if __name__ == "__main__":
    app = PortfolioApp()
    app.run()