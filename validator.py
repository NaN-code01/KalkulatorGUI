class Validator:
  _NUMBERS: set[str] = set("0123456789")
  _OPERATORS: set[str] = set("+-*/^")
  _PARENTHESES: set[str] = set("()")
  _ALLOWED_CHARS: set[str] = _NUMBERS | _OPERATORS | _PARENTHESES | set(".")

  _VALID_TYPE_NEXT: dict[str, set[str]] = {
    "number": {"operator", "rparen"},
    "operator": {"number", "lparen"},
    "lparen": {"number", "lparen"},
    "rparen": {"operator", "rparen"}
  }

  # VALIDATE EXPRESSION codeblock ------------------------------
  
  @classmethod
  def validate_expression(cls, expression: str) -> bool:
    allowed_chars: set[str] = cls._ALLOWED_CHARS

    if not all(char in allowed_chars for char in expression):
      raise ValueError("Expression contains invalid character")
    
    return True

  # VALIDATE TOKENS codeblock ------------------------------
  
  @classmethod
  def validate_tokens(cls, tokens: list[str], expression: str) -> bool:
    return (
      cls._lexical_check(tokens, expression)
      and cls._start_end_check(tokens)
      and cls._parentheses_check(tokens)
      and cls._grammar_check(tokens)
    )
  
  # -- validate_tokens() method utility (private) - - - - - - - - - -
  @classmethod
  def _lexical_check(cls, tokens: list[str], expression: str) -> bool:
    if "".join(tokens) != expression:
      raise ValueError("Expression contains an invalid token")
    
    return True

  @classmethod
  def _start_end_check(cls, tokens: list[str]) -> bool:
    operators: set[str] = cls._OPERATORS

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
  def _parentheses_check(tokens: list[str]) -> bool:
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
  def _grammar_check(cls, tokens: list[str]) -> bool:
    operator: set[str] = cls._OPERATORS
    valid_type: dict[str, set[str]] = cls._VALID_TYPE_NEXT
    prev_type: str = ""

    for token in tokens:
      curr_type: str = cls._token_type(token, operator)
      
      if prev_type:
        if not cls._compare_type(prev_type, curr_type, valid_type):
          raise ValueError("Token contains invalid order")
      
      prev_type = curr_type
    
    return True
  
  # ---- gramar_check() method utility (private) -  -  -  -  -
  @staticmethod
  def _token_type(token: str, operator: set[str]) -> str:
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
  
  @staticmethod
  def _compare_type(prev_type: str, curr_type: str, valid_type: dict[str, set[str]]) -> bool:
    return True if curr_type in valid_type[prev_type] else False
  
  # VALIDATE DIVISION codeblock ------------------------------

  @staticmethod
  def validate_division(value2: float) -> bool:
    if value2 == 0:
      raise ZeroDivisionError("Cannot divide by zero")
    
    return True
  
  # VALIDATE OPERATOR codeblock ------------------------------

  @classmethod
  def validate_operator(cls, operator: str) -> bool:
    if operator not in cls._OPERATORS:
      raise ValueError(f"Unsupported operator: {operator}")
    
    return True