import customtkinter as CT
import os

THEME: dict[str, dict[str, str]] = {
  "dark_theme": {
    "bg": "#1e1e1e",
    "fg": "#ffffff",
    "button_bg": "#2e2e2e",
    "button_fg": "#ffffff",
    "accent": "#007acc",
    "font_color": "#ffffff",
  },
  "light_theme": {
    "bg": "#ffffff",
    "fg": "#000000",
    "button_bg": "#f0f0f0",
    "button_fg": "#000000",
    "accent": "#007acc",
    "font_color": "#000000",
  }
}

class GUI(CT.CTk):
  def __init__(self) -> None:
    super().__init__()
    self.current_theme = THEME["dark_theme"]
    self.title("KalkulatorGUI")
    self.geometry("400x300")
    self.configure(bg=self.current_theme["bg"])


def main() -> None:
  app = GUI()
  app.mainloop()

if __name__ == "__main__":
  main()