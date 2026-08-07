import re
from pathlib import Path
from typing import TypedDict

from .utils import Utility


class OperatorInfo(TypedDict):
  """Type definition describing an operator's precedence
     and associativity.
  """
  
  prec: int
  assoc: str


class PathConstants:
  """Store filesystem paths used throughout the application."""
  ROOT_DIR: Path = Path(__file__).resolve().parent.parent
  ASSETS_DIR: Path = ROOT_DIR / "assets"
  ICON_PATH: Path = ASSETS_DIR / "icon64.png"
  THEME_PATH: Path = ASSETS_DIR / "theme.json"


class GlobalConstants:
  """Store shared constants used by multiple application modules."""
                                            # called by:
  NUMBERS: set[str] = set("0123456789")     # gui
  OPERATORS: set[str] = set("+-*/^")        # gui validator
  UNARY_OPERATOR: set[str] = {"u+", "u-"}   #     validator
  PARENTHESES: set[str] = set("()")         # gui validator


class GuiConstants:
  """Store constants for the graphical user interface,
     including window settings, themes, layouts, and input mappings.
  """

  TITLE: str = "KalkulatorGUI"
  ICON_PATH_STR: str = str(PathConstants.ICON_PATH)

  THEME: dict[str, dict[str, str]] = (
    Utility.validate_and_load_json(
      file_path=str(PathConstants.THEME_PATH)
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
  """Store constants required for expression tokenization
     and evaluation.
  """

  # Define token pattern for regex
  TOKEN_PATTERN = re.compile(
    r"""
    \d+(?:\.\d+)?   # number
    |               # or
    [+\-*/^()]      # operator or parenthesis
    """,
    re.VERBOSE
  )

  # Define operator precedence and associativity:
  # "L" for Left, "R" for Right
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
  """Store constants used for expression validation
     and syntax checking.
  """

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