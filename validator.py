class Validator:
  NUMBERS: str = "0123456789"
  OPERATORS: str = "+-*/^"
  PARENTHESES: str = "()"
  ALLOWED_CHARS: set[str] = set(NUMBERS + OPERATORS + PARENTHESES + ".")
  ALLOWED_START: set[str] = set(NUMBERS + PARENTHESES[0])
  ALLOWED_END: set[str] = set(NUMBERS + PARENTHESES[1])

  @classmethod
  def validate_chars(cls, chars: str) -> bool:
    allowed_chars: set[str] = cls.ALLOWED_CHARS
    return all(char in allowed_chars for char in chars)
  
  @classmethod
  def validate_tokens(cls, tokens: list[str]) -> bool:
    return (
      cls.start_end_check(tokens)
      and cls.parentheses_check(tokens)
      and cls.decimal_check(tokens)
      and cls.operator_check(tokens)
    )
  
  @classmethod
  def start_end_check(cls, tokens: list[str]) -> bool:
    allowed_start: set[str] = cls.ALLOWED_START
    allowed_end: set[str] = cls.ALLOWED_END
    
    if tokens[0] in allowed_start and tokens[-1] in allowed_end:
      return True
    else:
      return False
  
  @classmethod
  def parentheses_check(cls, tokens: list[str]) -> bool:
    pass

  @classmethod
  def decimal_check(cls, tokens: list[str]) -> bool:
    pass

  @classmethod
  def operator_check(cls, tokens: list[str]) -> bool:
    pass