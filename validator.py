class Validator:
  @staticmethod
  def validate_chars(chars: str) -> bool:
    allowed_chars: set[str] = set("0123456789()+-*/^.")
    return all(char in allowed_chars for char in chars)