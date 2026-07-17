class Validator:
  NUMBERS: set[str] = set("0123456789")
  OPERATORS: set[str] = set("+-*/^")
  PARENTHESES: set[str] = set("()")
  ALLOWED_CHARS: set[str] = NUMBERS | OPERATORS | PARENTHESES | set(".")

  VALID_TYPE_NEXT: dict[str, set[str]] = {
    "number": {"operator", "rparen"},
    "operator": {"number", "lparen"},
    "lparen": {"number", "lparen"},
    "rparen": {"operator", "rparen"}
  }

  @classmethod
  def validate_expression(cls, expression: str) -> bool:
    allowed_chars: set[str] = cls.ALLOWED_CHARS

    if all(char in allowed_chars for char in expression):
      return True
    else:
      raise ValueError("Expression contains invalid character")

  @classmethod
  def validate_tokens(cls, tokens: list[str], expression: str) -> bool:
    return (
      cls.lexical_check(tokens, expression)
      and cls.start_end_check(tokens)
      and cls.parentheses_check(tokens)
      and cls.grammar_check(tokens)
    )
  
  @classmethod
  def lexical_check(cls, tokens: list[str], expression: str) -> bool:
    if "".join(tokens) != expression:
      raise ValueError("Expression contains an invalid token")
    
    return True

  @classmethod
  def start_end_check(cls, tokens: list[str]) -> bool:
    operators: set[str] = cls.OPERATORS

    if not tokens:
      raise ValueError("Token list is empty")
    
    if tokens[0] in operators or tokens[-1] in operators:
      raise ValueError("Tokens cannot have an operator as a first or last token")
    elif tokens[0] == ")":
      raise ValueError("Tokens's first token contains invalid parenthesis")
    elif tokens[-1] == "(":
      raise ValueError("Tokens's last token contains invalid parenthesis")
    
    return True

  @staticmethod
  def parentheses_check(tokens: list[str]) -> bool:
    parentheses_count: int = 0
    prev_token: str = ""
    
    for token in tokens:
      
      if token == "(":
        parentheses_count += 1
      elif token == ")":
        parentheses_count -= 1
      
      if parentheses_count < 0:
        raise ValueError("Tokens contains invalid parentheses")
      elif prev_token == "(" and token == ")":
        raise ValueError("Tokens contains empty parentheses")
      
      prev_token = token
    
    if parentheses_count != 0:
      raise ValueError("Tokens contains invalid parentheses")
    
    return True

  @classmethod
  def grammar_check(cls, tokens: list[str]) -> bool:
    operator: set[str] = cls.OPERATORS
    prev_type: str = ""

    for token in tokens:
      curr_type: str = cls.token_type(token, operator)

  
  @staticmethod
  def token_type(token: str, operator: set[str]) -> str:
    if token.replace(".", "", 1).isdigit():
      return "number"
    elif token in operator:
      return "operator"
    elif token == "(":
      return "lparen"
    elif token == ")":
      return "rparen"
    else:
      raise ValueError("Token typing is invalid")