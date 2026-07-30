from pathlib import Path

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

class Variable:
  # icon path finding
  ROOT_DIR = Path(__file__).resolve().parent.parent
  ASSETS_DIR = ROOT_DIR / "assets"
  ICON_PATH: str = str(ASSETS_DIR / "icon64.png")

  TITle: str = "KalkulatorGUI"
  THEME: dict[str, dict[str, str]] = THEME

  GEOMETRY: str = "300x400"
  # minsize
  MIN_WIDTH: int = 300
  MIN_HEIGHT: int = 400

  NUMBERS: set[str] = set("0123456789")
  OPERATORS: set[str] = set("+-*/^")
  PARENTHESIS: set[str] = set("()")
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