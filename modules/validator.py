import json
from typing import Any
from .constants import ValidatorConstants, GlobalConstants, PathConstants


class Validator:
  """Validate arithmetic expressions and token sequences.

  This class performs lexical and grammatical validation before an
  expression is evaluated. Validation is separated into multiple stages
  to ensure expressions follow the expected syntax.
  """

  # constant call - - - - - - - - - -
  _OPERATORS: set[str] = GlobalConstants.OPERATORS
  _UNARY_OPERATOR: set[str] = GlobalConstants.UNARY_OPERATOR
  _PARENTHESES: set[str] = GlobalConstants.PARENTHESES
  _ALLOWED_CHARS: set[str] = ValidatorConstants.ALLOWED_CHARS

  # allow implicit multiplication and unary operator
  _VALID_TYPE_NEXT: dict[str, set[str]] = ValidatorConstants.VALID_TYPE_NEXT

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
  def tokens_lexical_check(cls, tokens: list[str], expression: str) -> bool:
    """Verify that the generated tokens exactly reconstruct the expression.
    
    Args:
      tokens: The list of expression tokens.
      expression: The original expression beffore tokenizing process.
    
    Return:
      True if combined tokens is exacly like the original expression.

    Raise:
      VallueError: if combined token is ended up different from original expression.
    """
    
    if "".join(tokens) != expression:
      raise ValueError("Expression contain an invalid token")
    
    return True

  @classmethod
  def validate_tokens(cls, tokens: list[str]) -> bool:
    """Validate a tokenized arithmetic expression.

    Performs structural, parenthesis, and grammar validation.

    Args:
      tokens: The list of expression tokens.

    Returns:
      True if all validation stages succeed.

    Raises:
      ValueError: If any validation stage fails.
    """
    
    return (
      cls._start_end_check(tokens)
      and cls._parentheses_check(tokens)
      and cls._grammar_check(tokens)
    )
  
  # -- validate_tokens() method utility (private) - - - - - - - - - -
  @classmethod
  def _start_end_check(cls, tokens: list[str]) -> bool:
    """Validate the first and last tokens of the expression."""
    if not tokens:
      raise ValueError("Token list is empty")
    
    if tokens[0] in cls._OPERATORS:
      raise ValueError("Tokens cannot have an operator as a first token")
    elif tokens[0] == ")":
      raise ValueError("The first token contain invalid parenthesis")
    elif tokens[-1] in cls._OPERATORS:
      raise ValueError("Tokens cannot have an operator as a last token")
    elif tokens[-1] == "(":
      raise ValueError("The last token contain invalid parenthesis")
    elif tokens[-1] in cls._UNARY_OPERATOR:
      raise ValueError("The last token contain unary operator")
        
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
    prev_type: str = ""

    for token in tokens:
      curr_type: str = cls._token_type(token)
      
      if prev_type and not cls._compare_type(prev_type, curr_type):
        raise ValueError("Invalid token order")
      
      prev_type = curr_type
    
    return True
  
  # ---- gramar_check() method utility (private) -  -  -  -  -
  @classmethod
  def _token_type(cls, token: str) -> str:
    """Return the token category used during grammar validation."""
    if token.replace(".", "", 1).isdigit():
      return "number"
    elif token in cls._OPERATORS:
      return "operator"
    elif token == "(":
      return "lparen"
    elif token == ")":
      return "rparen"
    elif token in cls._UNARY_OPERATOR:
      return "unary"
    else:
      raise ValueError("Token typing is invalid")
  
  @classmethod
  def _compare_type(cls, prev_type: str, curr_type: str) -> bool:
    """Return whether two consecutive token types form a valid sequence."""
    return curr_type in cls._VALID_TYPE_NEXT[prev_type]
  

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


  # VALIDATE AND LOAD JSON codeblock ------------------------------

  @classmethod
  def validate_and_load_json(cls, file_path: str) -> dict[str, Any]:
    """Load a JSON file and return its contents as a dictionary.

    The file is opened using UTF-8 encoding to ensure consistent behavior
    across operating systems. If the file cannot be found or contains
    invalid JSON syntax, an appropriate exception is raised.

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
