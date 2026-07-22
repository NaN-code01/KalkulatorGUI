import customtkinter as CT
from calculator import Calculator

# Centralized theme configuration.
# Each theme defines the color palette used throughout the application.
THEME: dict[str, dict[str, str]] = {
  "dark_theme": {
    "bg": "#1e1e1e",
    "fg": "#ffffff",
    "button_bg": "#2e2e2e",
    "button_fg": "#ffffff",
    "operator_button_bg": "#007acc",
    "operator_button_hover": "#464646",
    "accent": "#007acc",
    "font_color": "#ffffff",
    "error_color": "#ff0000"
  },
  "light_theme": {
    "bg": "#ffffff",
    "fg": "#000000",
    "button_bg": "#f0f0f0",
    "button_fg": "#000000",
    "operator_button_bg": "#007acc",
    "operator_button_hover": "#cccccc",
    "accent": "#007acc",
    "font_color": "#000000",
    "error_color": "#ff0000"
  }
}

class GUI(CT.CTk):
  def __init__(self) -> None:
    super().__init__()
    self.setup_window()
    self.create_frame()
    self.create_variables()
    self.create_widgets()

  def setup_window(self) -> None:
    self.title("KalkulatorGUI")
    self.geometry("300x400")
    self.minsize(300, 400)
    self.current_theme = THEME["dark_theme"]
    self.configure(bg=self.current_theme["bg"])

  def create_frame(self) -> None:
    self.display_frame: CT.CTkFrame = CT.CTkFrame(
      master=self,
      fg_color=self.current_theme["bg"],
      border_color=self.current_theme["fg"]
    )

    self.btn_frame: CT.CTkFrame = CT.CTkFrame(
      master=self,
      fg_color=self.current_theme["bg"],
      border_color=self.current_theme["fg"]
    )

  def create_variables(self) -> None:
    self.expression: str = ""
    self.result: str = ""
    self.error_message: str = ""
    self.last_expression: str = ""
    self.last_operation: str = ""

  def create_widgets(self) -> None:
    self.create_display(self.expression)
    self.create_buttons()
    self.create_layout()
    self.bind_events()

  def create_display(self, expression: str) -> None:
    self.display: CT.CTkLabel = CT.CTkLabel(
      master=self.display_frame,
      text=expression,
      anchor="e",
      font=("Arial", 20),
      justify="right",
      text_color=self.current_theme["font_color"]
    )

  def create_buttons(self) -> None:
    self.btn_texts: tuple[tuple[str, ...], ...] = (
      ("7", "8", "9", "/", "DEL"),
      ("4", "5", "6", "*", "C"),
      ("1", "2", "3", "-", "="),
      ("0", ".", "", "+", "")
    )
    
    for r, row in enumerate(self.btn_texts):
      for c, btn_text in enumerate(row):
        if btn_text == "":
            continue
        
        if btn_text in {"+", "-", "*", "/", "=", "DEL", "C"}:
          fg_color = self.current_theme["operator_button_bg"]
          hover_color = self.current_theme["operator_button_hover"]
        else:
          fg_color = self.current_theme["button_bg"]
          hover_color = self.current_theme["accent"]

        button: CT.CTkButton = CT.CTkButton(
          text=btn_text,
          master=self.btn_frame,
          width=50,
          height=50,
          font=("Arial", 16),
          fg_color=fg_color,
          text_color=self.current_theme["button_fg"],
          hover_color=hover_color,
          command=lambda text=btn_text: 
            self.on_button_click(text)
        )

        button.grid(
          row=r,
          column=c,
          padx=4,
          pady=4,
          sticky="nsew"
        )

  def create_layout(self) -> None:
    # window layout
    self.grid_rowconfigure(0, weight=5)
    self.grid_rowconfigure(1, weight=5)
    self.grid_columnconfigure(0, weight=1)

    # display layout
    self.display.grid(
      row=0,
      column=0, 
      padx=4, 
      pady=4, 
      sticky="nsew"
    )

    # display frame layout
    self.display_frame.grid_rowconfigure(0, weight=1)
    self.display_frame.grid_columnconfigure(0, weight=1)
    
    self.display_frame.grid(
      row=0, 
      column=0, 
      padx=4, 
      pady=4, 
      sticky="nsew"
    )
    
    # button frame layout
    for row in range(len(self.btn_texts)):
      self.btn_frame.grid_rowconfigure(row, weight=1)

    for column in range(len(self.btn_texts[0])):
      self.btn_frame.grid_columnconfigure(column, weight=1)

    self.btn_frame.grid(
      row=1, 
      column=0, 
      padx=4, 
      pady=4, 
      sticky="nsew"
    )

  def bind_events(self) -> None:
    self.bind(
      "<Return>", 
      lambda event: 
        self.on_button_click("=")
    )
    
    self.bind(
      "<Escape>", 
      lambda event: 
        self.on_button_click("C")
    )
    
    self.bind(
      "<BackSpace>", 
      lambda event: 
        self.on_button_click("DEL")
    )

    for key in "0123456789":
      self.bind(
        key, 
        lambda event, k=key: 
          self.on_button_click(k)
      )
    
    for key in "+-*/":
      self.bind(
        key, 
        lambda event, k=key: 
          self.on_button_click(k)
      )
  
  def on_button_click(self, btn_text: str) -> None:
    if btn_text == "=":
      self.calculate()
    
    if btn_text == "C":
      self.clear()
    
    if btn_text == "DEL":
      self.delete_last_character()
    
    if btn_text in "0123456789":
      self.input_number(btn_text)
    
    if btn_text in "+-*/":
      self.input_operator(btn_text)

  def calculate(self) -> None:
    self.update_display("result")

  def clear(self) -> None:
    self.expression = ""
    self.result = ""
    self.update_display("expression")

  def delete_last_character(self) -> None:    
    if self.expression:
      self.expression = self.expression[:-1]
      self.last_expression = (self.expression[-1] if self.expression else "")
    
    self.update_display("expression")
  
  def input_number(self, value: str) -> None:
    self.expression += value
    self.last_expression = value
    self.update_display("expression")
  
  def input_operator(self, operator: str) -> None:
    if self.last_expression in "0123456789":
      self.expression += operator
      self.last_expression = operator
      self.last_operation = operator
      self.update_display("expression")

  def show_error(self, message: str) -> None:
    self.error_message = message
    self.update_display("error")
    self.after(2000, self.clear)
  
  def update_display(self, usage: str) -> None:
    if usage == "error":
      self.display.configure(
        text=self.error_message, 
        text_color=self.current_theme["error_color"]
      )

    if usage == "result":
      self.display.configure(
        text=self.result, 
        text_color=self.current_theme["font_color"]
      )
    
    if usage == "expression":
      self.display.configure(
        text=self.expression, 
        text_color=self.current_theme["font_color"]
      )

def main() -> None:
  app = GUI()
  app.mainloop()

if __name__ == "__main__":
  main()