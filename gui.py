import customtkinter as CT
from calculator import Calculator

# Centralized theme configuration.
# Each theme defines the color palette used throughout the application.
THEME: dict[str, dict[str, str]] = {
  "dark_theme": {
    "bg": "#1e1e1e",
    "fg": "#ffffff",

    "button_bg": "#2e2e2e",
    "button_hover": "#464646",

    "operator_button_bg": "#0088ff",
    "operator_button_hover": "#464646",

    "utility_button_bg": "#0066FF",
    "utility_button_hover": "#464646",

    "font_color": "#ffffff",
    "error_color": "#ff0000"
  }
}

class GUI(CT.CTk):
  def __init__(self) -> None:
    super().__init__()
    self._create_variables()
    self._setup_window()
    self._create_frames()
    self._create_widgets()
    self._bind_events()

  def _create_variables(self) -> None:
    self._title: str = "KalkulatorGUI"
    self._current_theme = THEME["dark_theme"]

    self._geometry: str = "300x400"
    # minsize
    self._width: int = 300
    self._height: int = 400

    self._NUMBERS: set[str] = set("0123456789")
    self._OPERATORS: set[str] = set("+-*/^")
    self._UTILITY: set[str] = {"=", "DEL", "C"}
    self._btn_texts: list[list[str]] = [
      ["7", "8", "9", "=", "DEL", "C"],
      ["4", "5", "6", "-", "/",   "^"],
      ["1", "2", "3", "+", "*",   ""],
      ["0", ".", "(", ")", "",    ""]
    ]

    self._expression: str = ""
    self._last_expression: str = ""
    self._last_number: str = ""
    self._last_operation: str = ""
    
    self._result: str = ""
    self._error_message: str = ""

  def _setup_window(self) -> None:
    self.title(self._title)
    self.configure(bg=self._current_theme["bg"])
    self.geometry(self._geometry)
    self.minsize(self._width, self._height)

  def _create_frames(self) -> None:
    self.display_frame: CT.CTkFrame = CT.CTkFrame(
      master=self,
      fg_color=self._current_theme["bg"],
      border_color=self._current_theme["fg"]
    )

    self.btn_frame: CT.CTkFrame = CT.CTkFrame(
      master=self,
      fg_color=self._current_theme["bg"],
      border_color=self._current_theme["fg"]
    )

  def _create_widgets(self) -> None:
    self._create_display()
    self._create_buttons()
    self._create_layout()

  def _create_display(self) -> None:
    self.display: CT.CTkLabel = CT.CTkLabel(
      master=self.display_frame,
      text=self._expression,
      anchor="e",
      font=("Arial", 20),
      justify="right",
      text_color=self._current_theme["font_color"]
    )

  def _create_buttons(self) -> None:
    for r, row in enumerate(self._btn_texts):
      for c, btn_text in enumerate(row):
        if btn_text == "":
            continue
        
        if btn_text in self._OPERATORS:
          fg_color = self._current_theme["operator_button_bg"]
          hover_color = self._current_theme["operator_button_hover"]
        elif btn_text in self._UTILITY:
          fg_color = self._current_theme["utility_button_bg"]
          hover_color = self._current_theme["utility_button_hover"]
        else:
          fg_color = self._current_theme["button_bg"]
          hover_color = self._current_theme["button_hover"]

        button: CT.CTkButton = CT.CTkButton(
          text=btn_text,
          master=self.btn_frame,
          width=50,
          height=50,
          font=("Arial", 16),
          fg_color=fg_color,
          text_color=self._current_theme["font_color"],
          hover_color=hover_color,
          command=lambda text=btn_text: 
            self._on_button_click(text)
        )

        button.grid(
          row=r,
          column=c,
          padx=4,
          pady=4,
          sticky="nsew"
        )

  def _create_layout(self) -> None:
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
    self.display_frame.grid_rowconfigure(0, weight=3)
    self.display_frame.grid_columnconfigure(0, weight=1)
    
    self.display_frame.grid(
      row=0, 
      column=0, 
      padx=4, 
      pady=4, 
      sticky="nsew"
    )
    
    # button frame layout
    for row in range(len(self._btn_texts)):
      self.btn_frame.grid_rowconfigure(row, weight=1)

    for column in range(len(self._btn_texts[0])):
      self.btn_frame.grid_columnconfigure(column, weight=1)

    self.btn_frame.grid(
      row=1, 
      column=0, 
      padx=4, 
      pady=4, 
      sticky="nsew"
    )

  def _bind_events(self) -> None:
    self.bind(
      "<Return>", 
      lambda event: 
        self._on_button_click("=")
    )
    
    self.bind(
      "<Escape>", 
      lambda event: 
        self._on_button_click("C")
    )
    
    self.bind(
      "<BackSpace>", 
      lambda event: 
        self._on_button_click("DEL")
    )

    for key in {".", "(", ")"}:
      self.bind(
        key, 
        lambda event, k=key: 
          self._on_button_click(k)
      )    

    for key in self._NUMBERS:
      self.bind(
        key, 
        lambda event, k=key: 
          self._on_button_click(k)
      )
    
    for key in self._OPERATORS:
      self.bind(
        key, 
        lambda event, k=key: 
          self._on_button_click(k)
      )
  
  def _on_button_click(self, btn_text: str) -> None:
    if btn_text == "=":
      self._calculate()
    
    if btn_text == "C":
      self._clear()
    
    if btn_text == "DEL":
      self._delete_last_character()

    if btn_text == ".":
      self._input_decimal()

    if btn_text in {"(", ")"}:
      self._input_parenthesis(btn_text)

    if btn_text in self._NUMBERS:
      self._input_number(btn_text)
    
    if btn_text in self._OPERATORS:
      self._input_operator(btn_text)

  def _calculate(self) -> None:
    if (
      not self._expression
      or self._expression[-1] not in self._NUMBERS | {")"}
    ):
      return

    self._result = Calculator.calculate(expression=self._expression)
    self._update_display("result")

  def _clear(self) -> None:
    self._expression = ""
    self._result = ""
    self._update_display("expression")

  def _delete_last_character(self) -> None:    
    if not self._expression:
      return
    
    self._expression = self._expression[:-1]
    self._update_display("expression")

  def _input_decimal(self) -> None:
    if not self._expression:
      return

    if self._expression[-1] in self._NUMBERS:
      self._expression += "."
      self._update_display("expression")

  def _input_parenthesis(self, parenthesis: str) -> None:
    if not self._expression and parenthesis == ")":
      return

    self._expression += parenthesis
    self._update_display("expression")

  def _input_number(self, value: str) -> None:
    self._expression += value
    self._last_number = value
    self._update_display("expression")
  
  def _input_operator(self, operator: str) -> None:
    self._expression += operator
    self._last_operation = operator
    self._update_display("expression")

  def _show_error(self, message: str) -> None:
    self._error_message = message
    self._update_display("error")
    self.after(2000, self._clear)
  
  def _update_display(self, usage: str) -> None:
    match usage:
      case "error":
        self.display.configure(
          text=self._error_message, 
          text_color=self._current_theme["error_color"]
        )
      case "result":
        self.display.configure(
          text=self._result, 
          text_color=self._current_theme["font_color"]
        )
      case "expression":
        self.display.configure(
          text=self._expression, 
          text_color=self._current_theme["font_color"]
        )

def main() -> None:
  app = GUI()
  app.mainloop()

if __name__ == "__main__":
  main()