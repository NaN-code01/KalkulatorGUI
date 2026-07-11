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
    self.setup_window()
    self.create_variables()
    self.create_widgets()

  def setup_window(self) -> None:
    self.title("KalkulatorGUI")

    self.geometry("300x300")
    self.minsize(300, 300)
    
    self.current_theme = THEME["dark_theme"]
    self.configure(bg=self.current_theme["bg"])

  def create_variables(self) -> None:
    self.expression: str = "(placeholder)"
    self.result: str = ""
    self.error_message: str = ""
    self.last_operation: str = ""

  def create_widgets(self) -> None:
    self.create_display(self.expression)
    self.create_buttons()
    self.create_layout()
    self.bind_events()

  def create_display(self, expression: str) -> None:
    self.display: CT.CTkLabel = CT.CTkLabel(
      text=expression,
      master=self,
      width=300,
      font=("Arial", 20),
      justify="right",
      text_color=self.current_theme["font_color"]
    )

  def create_buttons(self) -> None:
    self.btn_texts: tuple[tuple[str, ...], ...] = (
      ("7", "8", "9", "/"),
      ("4", "5", "6", "*"),
      ("1", "2", "3", "-"),
      ("0", ".", "=", "+")
    )
    
    for row in self.btn_texts:
      for btn_text in row:
        button: CT.CTkButton = CT.CTkButton(
          text=btn_text,
          master=self,
          width=50,
          height=50,
          font=("Arial", 16),
          fg_color=self.current_theme["button_bg"],
          text_color=self.current_theme["button_fg"],
          hover_color=self.current_theme["accent"],
          command=lambda text=btn_text: self.on_button_click(text)
        )
        button.grid(row=self.btn_texts.index(row) + 1, column=row.index(btn_text), padx=4, pady=4)

  def create_layout(self) -> None:
    pass

  def bind_events(self) -> None:
    pass

  
  def on_button_click(self, button_text: str) -> None:
    pass

  def calculate(self) -> None:
    pass

  def clear(self) -> None:
    pass

  def delete_last_character(self) -> None:
    pass

  def update_display(self, text: str) -> None:
    pass

  def show_error(self, message: str) -> None:
    pass


def main() -> None:
  app = GUI()
  app.mainloop()

if __name__ == "__main__":
  main()