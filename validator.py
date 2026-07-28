class Validator:
  """Validate arithmetic expressions and token sequences.

  This class performs lexical and grammatical validation before an
  expression is evaluated. Validation is separated into multiple stages
  to ensure expressions follow the expected syntax.
  """
  
  _NUMBERS: set[str] = set("0123456789")
  _OPERATORS: set[str] = set("+-*/^")
  _PARENTHESES: set[str] = set("()")
  _ALLOWED_CHARS: set[str] = _NUMBERS | _OPERATORS | _PARENTHESES | set(".")

  # allow implicit multiplication
  _VALID_TYPE_NEXT: dict[str, set[str]] = {
    "number": {"operator","lparen", "rparen"},
    "operator": {"number", "lparen"},
    "lparen": {"number", "lparen"},
    "rparen": {"operator","lparen", "rparen"}
  }

  # VALIDATE EXPRESSION codeblock ------------------------------
  
  @classmethod
  def validate_expression(cls, expression: str) -> bool:
    """Validate the raw expression before tokenization.

    Checks whether the expression contains only supported characters.

    Args:
      expression: The arithmetic expression to validate.

    Returns:
      True if the expression is valid.

    Raises:
      ValueError: If the expression contains unsupported characters.
    """

    allowed_chars: set[str] = cls._ALLOWED_CHARS

    if not expression:
      raise ValueError("Expression cannot be empty")

    if not all(char in allowed_chars for char in expression):
      raise ValueError("Expression contain invalid character")
    
    return True

  # VALIDATE TOKENS codeblock ------------------------------
  
  @classmethod
  def validate_tokens(cls, tokens: list[str], expression: str) -> bool:
    """Validate a tokenized arithmetic expression.

    Performs lexical, structural, parenthesis, and grammar validation.

    Args:
      tokens: The list of expression tokens.
      expression: The original expression.

    Returns:
      True if all validation stages succeed.

    Raises:
      ValueError: If any validation stage fails.
    """
    
    return (
      cls._lexical_check(tokens, expression)
      and cls._start_end_check(tokens)
      and cls._parentheses_check(tokens)
      and cls._grammar_check(tokens)
    )
  
  # -- validate_tokens() method utility (private) - - - - - - - - - -
  @classmethod
  def _lexical_check(cls, tokens: list[str], expression: str) -> bool:
    """Verify that the generated tokens exactly reconstruct the expression."""
    if "".join(tokens) != expression:
      raise ValueError("Expression contain an invalid token")
    
    return True

  @classmethod
  def _start_end_check(cls, tokens: list[str]) -> bool:
    """Validate the first and last tokens of the expression."""
    operators: set[str] = cls._OPERATORS

    if not tokens:
      raise ValueError("Token list is empty")
    
    if tokens[0] in operators or tokens[-1] in operators:
      raise ValueError("Tokens cannot have an operator as a first or last token")
    elif tokens[0] == ")":
      raise ValueError("The first token contain invalid parenthesis")
    elif tokens[-1] == "(":
      raise ValueError("The last token contain invalid parenthesis")
    
    return True

  @staticmethod
  def _parentheses_check(tokens: list[str]) -> bool:
    """Validate balanced and properly ordered parentheses."""
    parentheses_count: int = 0
    prev_token: str = ""
    
    for token in tokens:
      
      if token == "(":
        parentheses_count += 1
      elif token == ")":
        parentheses_count -= 1
      
      if parentheses_count < 0:
        raise ValueError("Tokens contain invalid parentheses")
      elif prev_token == "(" and token == ")":
        raise ValueError("Tokens contain empty parentheses")
      
      prev_token = token
    
    if parentheses_count != 0:
      raise ValueError("Tokens contain invalid parentheses")
    
    return True

  @classmethod
  def _grammar_check(cls, tokens: list[str]) -> bool:
    """Validate the grammatical order of adjacent token types."""
    operator: set[str] = cls._OPERATORS
    valid_type: dict[str, set[str]] = cls._VALID_TYPE_NEXT
    prev_type: str = ""

    for token in tokens:
      curr_type: str = cls._token_type(token, operator)
      
      if prev_type and not cls._compare_type(prev_type, curr_type, valid_type):
        raise ValueError("Invalid token order")
      
      prev_type = curr_type
    
    return True
  
  # ---- gramar_check() method utility (private) -  -  -  -  -
  @staticmethod
  def _token_type(token: str, operator: set[str]) -> str:
    """Return the token category used during grammar validation."""
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
    """Return whether two consecutive token types form a valid sequence."""
    return curr_type in valid_type[prev_type]
  
  # VALIDATE EXPRESSION LENGTH codeblock ------------------------------

  @classmethod
  def validate_expression_length(cls, expression: str, max_length: int):
    """Validate expression length so it doesnt past beyond max length
       when doing input.

    Args:
      expression: The expression on display.
      max_length: The max length of the expression.

    Returns:
      True if the expression length is less than the max length.

    Raises:
      IndexError: If the expression length is more or equals to max length.
    """
    if len(expression) >= max_length:
      raise IndexError(f"Expression reached maximum length: {max_length}")

    return True

  # VALIDATE EVALUATION codeblock ------------------------------

  @classmethod
  def validate_evaluation(cls, operator: str, divisor: float) -> bool:
    """Validate math evaluation operator and divisor.

    Args:
      operator: The operator of current evaluation.
      divisor: The number that being used to divide (divide operation only).

    Raises:
      ValueError: If the operator is unsuported.
      ZeroDivisionError: If the divisor is equal to zero (0).
    """
    cls._operator_check(operator)

    if operator == "/":
      cls._divisor_check(divisor)

    return True

  # -- validate_evaluation() method utility (private) - - - - - - - - - -  
  @classmethod
  def _operator_check(cls, operator: str) -> bool:
    """Validate the operator and raise error when the operator is unsupported"""
    if operator not in cls._OPERATORS:
      raise ValueError(f"Unsupported operator: {operator}")
    
    return True

  @staticmethod
  def _divisor_check(divisor: float) -> bool:
    """Raise ZeroDivisionError if divisor is zero"""
    if divisor == 0:
      raise ZeroDivisionError("Cannot divide by zero")
    
    return True
  