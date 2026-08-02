import re
from pathlib import Path
from typing import TypedDict
from .validator import Validator


class OperatorInfo(TypedDict):
  prec: int
  assoc: str


class PathConstants:
  ROOT_DIR: Path = Path(__file__).resolve().parent.parent
  ASSETS_DIR: Path = ROOT_DIR / "assets"
  ICON_PATH: Path = ASSETS_DIR / "icon64.png"
  THEME_PATH: Path = ASSETS_DIR / "theme.json"


class GlobalConstants:                      # called by:
  NUMBERS: set[str] = set("0123456789")     # gui
  OPERATORS: set[str] = set("+-*/^")        # gui validator
  UNARY_OPERATOR: set[str] = {"u+", "u-"}   #     validator
  PARENTHESES: set[str] = set("()")         # gui validator


class GuiConstants:
  ICON_PATH_STR: str = str(PathConstants.ICON_PATH)
  TITLE: str = "KalkulatorGUI"

  THEME: dict[str, dict[str, str]] = (
    Validator.validate_and_load_json(
      str(PathConstants.THEME_PATH)
    )
  )

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