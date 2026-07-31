import re
from pathlib import Path
from typing import TypedDict

class OperatorInfo(TypedDict):
  prec: int
  assoc: str

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

class PathConstants:
  ROOT_DIR: Path = Path(__file__).resolve().parent.parent
  ASSETS_DIR: Path = ROOT_DIR / "assets"
  ICON_PATH: Path = ASSETS_DIR / "icon64.png"

class GlobalConstants:                      # called by:
  NUMBERS: set[str] = set("0123456789")     # gui
  OPERATORS: set[str] = set("+-*/^")        # gui validator
  UNARY_OPERATOR: set[str] = {"u+", "u-"}   #     validator
  PARENTHESES: set[str] = set("()")         # gui validator

class GuiConstants:
  ICON_PATH_STR: str = str(PathConstants.ICON_PATH)
  TITLE: str = "KalkulatorGUI"
  THEME: dict[str, dict[str, str]] = THEME

  GEOMETRY: str = "300x400"
  # minsize
  MIN_WIDTH: int = 300
  MIN_HEIGHT: int = 400

  UTILITY: set[str] = {"=", "DEL", "C"}
  BTN_TEXTS: list[list[str]] = [
    ["C", "DEL", "",  "(", ")"],
    ["7", "8",   "9", "/", "^"],
    ["4", "5",   "6", "*", "="],
    ["1", "2",   "3", "-", ""],
    ["0", "",    ".", "+", ""]
  ]

  MAX_EXPRESSION_LENGTH: int = 50
  NUMPAD_OPERATORS: dict[str, str] = {
    "<KP_Add>": "+",
    "<KP_Subtract>": "-",
    "<KP_Multiply>": "*",
    "<KP_Divide>": "/"
  }

class CalculatorConstants:
  # Define token pattern for regex
  TOKEN_PATTERN = re.compile(
    r"""
    \d+(?:\.\d+)?   # number
    |               # or
    [+\-*/^()]      # operator or parenthesis
    """,
    re.VERBOSE
  )

  # Define operator precedence and associativity: "L" for Left, "R" for Right
  OPERATOR_INFO: dict[str, OperatorInfo] = {
    "+": {"prec": 1, "assoc": "L"},
    "-": {"prec": 1, "assoc": "L"},
    "*": {"prec": 2, "assoc": "L"},
    "/": {"prec": 2, "assoc": "L"},
    "^": {"prec": 3, "assoc": "R"},

    # unary operator
    "u-": {"prec": 3, "assoc": "R"},
    "u+": {"prec": 3, "assoc": "R"},
  }

  PREV_UNARY_INDICATOR: set[str] = {
    "(", "+", "-", "*", 
    "/", "^", "u+", "u-"
  }

class ValidatorConstants:
  ALLOWED_CHARS: set[str] = (
    GlobalConstants.NUMBERS 
    | GlobalConstants.OPERATORS 
    | GlobalConstants.PARENTHESES 
    | set(".")
  )

  # allow implicit multiplication and unary operator
  VALID_TYPE_NEXT: dict[str, set[str]] = {
    "number":   {"operator","lparen", "rparen"},
    "operator": {"number",  "lparen", "unary"},
    "lparen":   {"number",  "lparen", "unary"},
    "rparen":   {"operator","lparen", "rparen"},
    "unary":    {"number",  "lparen", "unary"}
  }