import tkinter as Tk

import customtkinter as CT

from .constants import GuiConstants, GlobalConstants
from .validator import Validator
from .calculator import Calculator


class GUI(CT.CTk):
  """Main calculator application window.

  Manages the user interface, user interactions, calculator state,
  and communication with the validation and calculation modules.
  """

  def __init__(self) -> None:
    """Initialize the calculator GUI and all its components."""
    super().__init__()
    self._create_variables()
    self._setup_window()
    self._create_frames()
    self._create_widgets()
    self._bind_events()


  # Initialize ------------------------------

  def _create_variables(self) -> None:
    """Initialize constants, application state, and runtime variables."""
    # constants call for checking - - - - - - - - - -
    self._NUMBERS: set[str] = GlobalConstants.NUMBERS
    self._OPERATORS: set[str] = GlobalConstants.OPERATORS
    self._PARENTHESES: set[str] = GlobalConstants.PARENTHESES


    # constants call for set up gui - - - - - - - - - -
    self._TITLE: str = GuiConstants.TITLE

    # icon issue, TODO: fix the issue when packaging process
    self._ICON_PATH_STR: str = GuiConstants.ICON_PATH_STR
    self._ICON = Tk.PhotoImage(file=self._ICON_PATH_STR)

    self._THEME: dict[str, dict[str, str]] = GuiConstants.THEME

    self._GEOMETRY: str = GuiConstants.GEOMETRY
    # minsize
    self._MIN_WIDTH: int = GuiConstants.MIN_WIDTH
    self._MIN_HEIGHT: int = GuiConstants.MIN_HEIGHT

    self._UTILITY: set[str] = GuiConstants.UTILITY
    self._BTN_TEXTS: list[list[str]] = GuiConstants.BTN_TEXTS

    self._MAX_EXPRESSION_LENGTH: int = GuiConstants.MAX_EXPRESSION_LENGTH
    self._NUMPAD_OPERATORS: dict[str, str] = GuiConstants.NUMPAD_OPERATORS


    # variables set up - - - - - - - - - -
    self._current_theme = self._THEME["dark_theme"]
    self._calculator_buttons: dict[str, CT.CTkButton] = {}

    self._expression: str = ""
    self._result: str = ""
    self._error_message: str = ""

    self._has_done_btn_click: bool = False
    self._has_error: bool = False
    self._last_number: str = ""
    self._last_operation: str = ""


  def _setup_window(self) -> None:
    """Configure the main window properties and appearance."""
    self.title(self._TITLE)
    self.iconphoto(True, self._ICON)
    self.configure(bg=self._current_theme["bg"])
    self.geometry(self._GEOMETRY)
    self.minsize(self._MIN_WIDTH, self._MIN_HEIGHT)


  def _create_frames(self) -> None:
    """Create the main container frames for the display and buttons."""
    self._display_frame: CT.CTkFrame = CT.CTkFrame(
      master=self,
      fg_color=self._current_theme["bg"],
      border_color=self._current_theme["bg"]
    )

    self._btn_frame: CT.CTkFrame = CT.CTkFrame(
      master=self,
      fg_color=self._current_theme["bg"],
      border_color=self._current_theme["bg"]
    )


  def _create_widgets(self) -> None:
    """Create all widgets used by the calculator interface."""
    self._create_display()
    self._create_buttons()
    self._create_layout()


  def _bind_events(self) -> None:
    """Bind keyboard and mouse events to their corresponding handlers."""
    # bind mouse scroll
    self._main_display.bind("<Button-4>", self._scroll_display)
    self._main_display.bind("<Button-5>", self._scroll_display)


    # bind utility keys
    self.bind("<Escape>", lambda event: self._on_button_click("C"))
    self.bind("<BackSpace>", lambda event: self._on_button_click("DEL"))

    for key in {"<Return>", "<KP_Enter>", "="}:
      self.bind(key, lambda event: self._on_button_click("="))


    # bind input keys
    for key in {"<KP_Decimal>", "."}:
      self.bind(key, lambda event: self._on_button_click("."))

    for key in {"(", ")"}:
      self.bind(key, lambda event, k=key: self._on_button_click(k))


    # number bind
    for key in self._NUMBERS:
      self.bind(key, lambda event, k=key: self._on_button_click(k))
      self.bind(f"<KP_{key}>", lambda event, k=key: self._on_button_click(k))


    # operator bind    
    for key in self._OPERATORS:
      self.bind(key, lambda event, k=key: self._on_button_click(k))

    for key, value in self._NUMPAD_OPERATORS.items():
      self.bind(key, lambda event, v=value: self._on_button_click(v))



  # -- create_widget() - - - - - - - - - -

  def _create_display(self) -> None:
    """Create the calculator display and error message widgets."""
    self._main_display = CT.CTkEntry(
      master=self._display_frame,
      state="readonly",
      justify="right",
      font=("Arial", 20),
      text_color=self._current_theme["font_color"],
      fg_color=self._current_theme["bg"],
      border_color=self._current_theme["bg"]
    )

    self._error_display = CT.CTkLabel(
      master=self._display_frame,
      text=self._error_message,
      anchor="w",
      justify="left",
      wraplength=200,
      font=("Arial", 16),
      text_color=self._current_theme["error_color"],
      fg_color=self._current_theme["bg"]
    )


  def _create_buttons(self) -> None:
    """Create the calculator buttons and theme selector."""
    self._create_calculator_buttons()
    self._create_theme_selector()


  def _create_layout(self) -> None:
    """Arrange all frames and widgets using the grid layout."""
    # window layout
    self.grid_rowconfigure(0, weight=5)
    self.grid_rowconfigure(1, weight=5)
    self.grid_columnconfigure(0, weight=1)

    # display frame layout
    self._display_frame.grid_rowconfigure(0, weight=1)
    self._display_frame.grid_rowconfigure(1, weight=0)
    self._display_frame.grid_rowconfigure(2, weight=1)
    self._display_frame.grid_columnconfigure(0, weight=1)
    
    self._display_frame.grid(
      row=0, 
      column=0,
      sticky="nsew"
    )
    
    # display layout
    self._main_display.grid(
      row=0,
      column=0, 
      padx=4, 
      pady=4, 
      sticky="nsew"
    )

    self._error_display.grid(
      row=1,
      column=0,
      padx=8,
      pady=(2, 4),
      sticky="nsew"
    )

    self._theme_selector.grid(
      row=2,
      column=0,
      padx=4, 
      pady=4, 
      sticky="sw"
    )
    
    # button frame layout
    self._btn_frame.grid(
      row=1, 
      column=0, 
      sticky="nsew"
    )

    for row in range(len(self._BTN_TEXTS)):
      self._btn_frame.grid_rowconfigure(row, weight=1)

    for column in range(len(self._BTN_TEXTS[0])):
      self._btn_frame.grid_columnconfigure(column, weight=1)



  # ---- create_buttons() -  -  -  -  -


  def _create_theme_selector(self) -> None:
    """Create the light and dark theme selector."""
    self._theme_selector = CT.CTkSegmentedButton(
      master=self._display_frame,
      values=["Light", "Dark"],
      command=self._on_theme_changed,
      font=("Arial", 12),
      text_color=self._current_theme["font_color"],
      fg_color=self._current_theme["button_bg"],
      selected_color=self._current_theme["accent"],
      selected_hover_color=self._current_theme["button_hover"],
      unselected_color=self._current_theme["button_bg"],
      unselected_hover_color=self._current_theme["button_hover"]
    )

    self._theme_selector.set(value="Dark")

  #     ---- theme utility

  def _on_theme_changed(self, value: str) -> None:
    """Handle theme selection changes."""
    match value:
      case "Light": self._set_theme("light_theme")
      case "Dark": self._set_theme("dark_theme")

  def _set_theme(self, theme_name: str) -> None:
    """Apply the specified theme and refresh the interface."""
    self._current_theme = self._THEME[theme_name]
    self._update_theme()

  def _update_theme(self) -> None:
    """Update widget colors to match the active theme."""
    self.configure(bg=self._current_theme["bg"])

    self._display_frame.configure(
      fg_color=self._current_theme["bg"],
      border_color=self._current_theme["bg"]
    )
    self._btn_frame.configure(
      fg_color=self._current_theme["bg"],
      border_color=self._current_theme["bg"]
    )

    self._main_display.configure(
      text_color=self._current_theme["font_color"],
      fg_color=self._current_theme["bg"],
      border_color=self._current_theme["bg"]
    )
    self._error_display.configure(
      text_color=self._current_theme["error_color"],
      fg_color=self._current_theme["bg"]
    )

    self._theme_selector.configure(
      text_color=self._current_theme["font_color"],
      fg_color=self._current_theme["button_bg"],
      selected_color=self._current_theme["accent"],
      selected_hover_color=self._current_theme["button_hover"],
      unselected_color=self._current_theme["button_bg"],
      unselected_hover_color=self._current_theme["button_hover"]
    )

    for btn_text, button in self._calculator_buttons.items():
      btn_color: dict[str, str] = self._get_button_color(btn_text)

      button.configure(
        text_color=self._current_theme["font_color"],
        fg_color=btn_color["fg_color"],
        hover_color=btn_color["hover_color"]
      )

  def _get_button_color(self, btn_text: str) -> dict[str, str]:
    """Return the foreground and hover colors for a button."""
    btn_color: dict[str, str] = {}

    if btn_text in self._OPERATORS or btn_text in self._PARENTHESES:
      fg_color = self._current_theme["operator_button_bg"]
      hover_color = self._current_theme["operator_button_hover"]

    elif btn_text in self._UTILITY:
      fg_color = self._current_theme["utility_button_bg"]
      hover_color = self._current_theme["utility_button_hover"]

    else:
      fg_color = self._current_theme["button_bg"]
      hover_color = self._current_theme["button_hover"]

    btn_color["fg_color"] = fg_color
    btn_color["hover_color"] = hover_color

    return btn_color

  #     ----


  def _create_calculator_buttons(self) -> None:
    """Create and position all calculator buttons."""
    for r, row in enumerate(self._BTN_TEXTS):
      for c, btn_text in enumerate(row):
        if btn_text == "":
            continue
        
        btn_color: dict[str, str] = self._get_button_color(btn_text)

        button: CT.CTkButton = CT.CTkButton(
          master=self._btn_frame,
          command=lambda text=btn_text: 
            self._on_button_click(text),
          width=50,
          height=50,
          text=btn_text,
          font=("Arial", 16),
          text_color=self._current_theme["font_color"],
          fg_color=btn_color["fg_color"],
          hover_color=btn_color["hover_color"]
        )

        if btn_text == "DEL":
          button.grid(
            row=r, 
            column=c,
            columnspan=2,
            padx=4, 
            pady=4, 
            sticky="nsew"
          )
        elif btn_text == "0":
          button.grid(
            row=r, 
            column=c,
            columnspan=2,
            padx=4, 
            pady=4, 
            sticky="nsew"
          )
        elif btn_text == "=":
          button.grid(
            row=r, 
            column=c,
            rowspan=3,
            padx=4, 
            pady=4, 
            sticky="nsew"
          )
        else:
          button.grid(
            row=r, 
            column=c,
            padx=4, 
            pady=4, 
            sticky="nsew"
          )

        self._calculator_buttons[btn_text] = button



  # -- bind_events() - - - - - - - - - -

  def _scroll_display(self, event) -> None:
    """Scroll the display horizontally using the mouse wheel."""
    if event.num == 4:
        self._main_display.xview_scroll(-1, "units")
    elif event.num == 5:
        self._main_display.xview_scroll(1, "units")

  def _on_button_click(self, btn_text: str) -> None:
    """Handle calculator button presses and dispatch the appropriate action."""
    self._clear_error()

    # utility button - - - - -
        
    if btn_text == "C":
      self._clear()
      self._has_done_btn_click = False
    
    if btn_text == "DEL":
      self._has_done_btn_click = True
      self._delete_last_character()
    
    if btn_text == "=":
      self._calculate()
      self._has_done_btn_click = False


    # input button - - - - -

    try:
      Validator.validate_expression_length(
        expression=self._expression,
        max_length=self._MAX_EXPRESSION_LENGTH
      )

    except Exception as e:
      self._show_error(str(e))
      return
    
    if btn_text == ".":
      self._has_done_btn_click = True
      self._input_decimal()

    if btn_text in {"(", ")"}:
      self._has_done_btn_click = True
      self._input_parenthesis(btn_text)

    if btn_text in self._NUMBERS:
      self._has_done_btn_click = True
      self._input_number(btn_text)
    
    if btn_text in self._OPERATORS:
      self._has_done_btn_click = True
      self._input_operator(btn_text)



# ---- on_button_click() -  -  -  -  -

  def _clear(self) -> None:
    """Reset the calculator state and clear the display."""
    self._expression = ""
    self._result = ""

    self._last_number = ""
    self._last_operation = ""

    self._has_error = False
    self._update_display("expression")

  def _clear_error(self) -> None:
    """Clear the current error message."""
    self._error_message = ""
    self._error_display.configure(text=self._error_message)

  def _delete_last_character(self) -> None:
    """Remove the last character from the current expression."""
    if not self._expression:
      return

    if len(self._expression) == 1:
      self._last_number = ""
      self._last_operation = ""
    
    if len(self._expression) >= 2:
      self._handle_last_number()
      self._handle_last_operation()

    self._expression = self._expression[:-1]
    self._update_display("expression")


  def _calculate(self) -> None:
    """Evaluate the current expression and display the result."""
    not_valid_to_calculate: bool = (
      not self._expression
      or self._expression[-1] not in self._NUMBERS | {")"}
    )

    can_do_constant_chain_calculation: bool = (
      len(self._expression) < self._MAX_EXPRESSION_LENGTH
      and not self._has_done_btn_click
      and not self._has_error
      and self._last_number != ""
      and self._last_operation != ""
    )

    if not_valid_to_calculate:
      return

    if can_do_constant_chain_calculation:
      self._expression += self._last_operation
      self._expression += self._last_number

    try:
      self._result = Calculator.calculate(expression=self._expression)
    except Exception as e:
      self._show_error(str(e))
      return

    self._expression = self._result
    self._update_display("result")


  def _input_decimal(self) -> None:
    """Append a decimal point when the current input is valid."""
    if not self._expression:
      return

    if self._expression[-1] in self._NUMBERS:
      self._expression += "."
      self._update_display("expression")

  def _input_parenthesis(self, parenthesis: str) -> None:
    """Append a parenthesis if it produces a valid expression."""
    if self._expression and self._expression[-1] == ".":
      return

    if parenthesis == ")":
      if not self._expression:
        return
      elif self._expression[-1] == "(":
        return

    self._expression += parenthesis
    self._update_display("expression")


  def _input_number(self, value: str) -> None:
    """Append a numeric digit to the current expression."""
    self._expression += value
    self._handle_last_number()
    self._update_display("expression")
  
  def _input_operator(self, operator: str) -> None:
    """Append an operator to the current expression when valid."""
    if operator not in {"+", "-"}:
      if not self._expression:
        return
      elif self._expression[-1] in self._OPERATORS:
        return
    
    self._expression += operator
    self._handle_last_operation()
    self._update_display("expression")


  #     ---- update display utility

  def _show_error(self, message: str) -> None:
    """Display an error message and mark the calculator as being in an error state."""
    self._error_message = message
    self._has_error = True
    self._update_display("error")
  
  def _update_display(self, usage: str) -> None:
    """Update the expression, result, or error display."""
    if usage == "error":
      self._error_display.configure(text=self._error_message)
      self.after(10000, self._clear_error)
      return

    self._main_display.configure(state="normal")
    self._main_display.delete(0, "end")

    if usage == "expression":
      self._main_display.insert(0, self._expression)
      self._main_display.icursor("end")
      self._main_display.xview_moveto(1.0)
      self._main_display.configure(
        justify="right",
        text_color=self._current_theme["font_color"]
      )
    elif usage == "result":
      self._main_display.insert(0, self._result)
      self._main_display.icursor("end")
      self._main_display.xview_moveto(1.0)
      self._main_display.configure(
        justify="right",
        text_color=self._current_theme["font_color"]
      )

    self._main_display.configure(state="readonly")

  #     ----


  #     ---- handle last input

  def _handle_last_number(self) -> None:
    """Extract and store the most recent numeric operand from the expression."""
    if not self._expression:
      return
    
    self._last_number = ""
    last_number_reversed: str = ""
    expression_reversed: str = self._expression[::-1]

    for char in expression_reversed:
      if char in self._OPERATORS or char in self._PARENTHESES:
        break
      elif char in self._NUMBERS or char == ".":
        last_number_reversed += char

    if last_number_reversed:
      self._last_number = last_number_reversed[::-1]

  def _handle_last_operation(self) -> None:
    """Extract and store the most recent operator from the expression."""
    if not self._expression:
      return
    
    self._last_operation = ""
    expression_reversed: str = self._expression[::-1]

    for char in expression_reversed:
      if char in self._OPERATORS:
        self._last_operation = char
        break

  #     -----