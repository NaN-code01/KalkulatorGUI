from pathlib import Path

class Variable:

  # icon path finding
  ROOT_DIR = Path(__file__).resolve().parent.parent
  ASSETS_DIR = ROOT_DIR / "assets"
  ICON_PATH: str = str(ASSETS_DIR / "icon64.png")