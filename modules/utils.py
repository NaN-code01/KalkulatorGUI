import json
from typing import Any


class Utility:

  @staticmethod
  def validate_and_load_json(file_path: str) -> dict[str, Any]:
    """Load a JSON file and return its contents as a dictionary.

    The file is opened using UTF-8 encoding to ensure
    consistent behavior across operating systems.
    If the file cannot be found or contains invalid JSON syntax,
    an appropriate exception is raised.

    Args:
        file_path: Path to the JSON file.

    Returns:
        A dictionary containing the parsed JSON data.

    Raises:
        FileNotFoundError:
            If the specified file does not exist.
        ValueError:
            If the file contains invalid JSON syntax.
        Exception:
            If an unexpected error occurs while loading the file.
    """

    try:
      # specify encoding='utf-8' to prevent OS-specific character bugs
      with open(file_path, 'r', encoding='utf-8') as file:
        data: dict[str, Any] = json.load(file)
        return data
      
    except FileNotFoundError:
        raise FileNotFoundError(
          f"Error: The file at {file_path} was not found."
        )
    except json.JSONDecodeError as e:
        raise ValueError(
          f"Compatibility Error: Invalid JSON syntax.\nDetails: {e}"
        ) from e
    except Exception as e:
        raise Exception(
          f"An unexpected error occurred: {e}"
        ) from e

  @staticmethod
  def is_number(token: str) -> bool:
    """Return whether a token represents a numeric value.

    A token is considered numeric if it contains only digits or a
    single decimal point.

    Args:
      token: The token to check.

    Returns:
      True if the token represents a valid integer or decimal number,
      otherwise False.
    """
    
    # .replace() for decimal number checked by .isdigit()
    return token.replace(".", "", 1).isdigit()
