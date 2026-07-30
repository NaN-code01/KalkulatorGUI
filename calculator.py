import re
import math
from typing import TypedDict
from validator import Validator

class OperatorInfo(TypedDict):
  prec: int
  assoc: str

class Calculator:
  """Evaluate mathematical expressions using the Shunting Yard algorithm.

  Expressions are converted from infix notation to postfix notation before
  being evaluated. Input validation is delegated to the Validator class.
  """

  # Define operator precedence and associativity: "L" for Left, "R" for Right
  _OPERATORS: dict[str, OperatorInfo] = {
    "+": {"prec": 1, "assoc": "L"},
    "-": {"prec": 1, "assoc": "L"},
    "*": {"prec": 2, "assoc": "L"},
    "/": {"prec": 2, "assoc": "L"},
    "^": {"prec": 3, "assoc": "R"},

    # unary operator
    "u-": {"prec": 3, "assoc": "R"},
    "u+": {"prec": 3, "assoc": "R"},
  }

  # Define token pattern for regex
  _TOKEN_PATTERN = re.compile(
    r"""
    \d+(?:\.\d+)?   # number
    |               # or
    [+\-*/^()]      # operator or parenthesis
    """,
    re.VERBOSE
  )

  _PREV_UNARY_INDICATOR: set[str] = {"(", "+", "-", "*", "/", "^", "u+", "u-"}

  # CALCULATE codeblock ------------------------------

  @classmethod
  def calculate(cls, expression: str) -> str:
    """Evaluate an arithmetic expression.

    The expression is validated, tokenized, converted to postfix notation,
    and evaluated. The result is returned as a formatted string.

    Args:
      expression: The arithmetic expression in infix notation.

    Returns:
      The evaluated result as a formatted string.

    Raises:
      ValueError: If the expression or generated tokens are invalid,
                  or the operator is unsuported,
                  or the evaluation result is out of range.
      ZeroDivisionError: If division by zero occurs.
    """

    Validator.validate_expression(expression=expression)
    
    tokens: list[str] = cls._tokenize(expression)
    Validator.tokens_lexical_check(tokens=tokens, expression=expression)

    tokens_with_unary: list[str] = cls._normalize_unary_operators(tokens)
    tokens_with_mult: list[str] = cls._insert_implicit_multiplication(tokens_with_unary)
    Validator.validate_tokens(tokens=tokens_with_mult)

    postfix: list[str] = cls._infix_to_postfix(tokens_with_mult)
    result: str = cls._evaluate_postfix(postfix)
    return result

  # -- calculate() method utility (private) - - - - - - - - - -
  @classmethod
  def _tokenize(cls, expression: str) -> list[str]:
    """Split an arithmetic expression into individual tokens."""
    tokens: list[str] = cls._TOKEN_PATTERN.findall(expression)
    return tokens

  # ---- tokenize() method utility (private) -  -  -  -  -
  @classmethod
  def _normalize_unary_operators(cls, tokens: list[str]) -> list[str]:
    """Turn unary + or - into its own unary tokens"""
    prev_unary_indicator: set[str] = cls._PREV_UNARY_INDICATOR
    result: list[str] = []
    prev: str | None = None

    for token in tokens:
      is_plusmin: bool = token in {"+", "-"}
      is_prevforunary: bool = prev is None or prev in prev_unary_indicator
      is_unary: bool = is_plusmin and is_prevforunary

      if is_unary:
        result.append(f"u{token}")
      else:
        result.append(token)

      prev = result[-1]

    return result
    
  @classmethod
  def _insert_implicit_multiplication(cls, tokens: list[str]) -> list[str]:
    """Insert '*' where multiplication is implied. (parenthesis multipication)"""
    result: list[str] = []

    for token in tokens:
      if result:
        prev: str = result[-1]

        # when a value is followed by another value or an opening parenthesis
        prev_is_value: bool = cls._is_number(prev) or prev == ")"
        curr_is_value: bool = cls._is_number(token) or token == "("

        if prev_is_value and curr_is_value:
          result.append("*")

      result.append(token)

    return result
  # -  -  -  -  -
  
  @classmethod
  def _infix_to_postfix(cls, tokens: list[str]) -> list[str]:
    """Convert infix tokens to postfix notation using the Shunting Yard algorithm."""
    operators = cls._OPERATORS
    operator_stack: list[str] = []
    output_queue: list[str] = []

    # Shunting Yard Algorithm
    for token in tokens:

      # number handling
      if cls._is_number(token):
        output_queue.append(token)
        continue
      
      # parentheses handling
      if token == "(":
        operator_stack.append(token)
        continue
      
      if token == ")":
        cls._handle_close_parenthesis(operator_stack, output_queue)
        continue
      
      # operator handling
      if token in operators:
        cls._handle_operator(token, operator_stack, output_queue)
        continue
    
    # .pop() remaining operators to output
    while operator_stack:
      output_queue.append(operator_stack.pop())
    
    return output_queue

  # ---- infix_to_postfix() method utility (private) -  -  -  -  -
  @classmethod
  def _handle_close_parenthesis(
      cls, 
      operator_stack: list[str], 
      output_queue: list[str]
    ) -> None:
    """Pop operators until the matching opening parenthesis is reached."""

    while operator_stack and operator_stack[-1] != "(":
      output_queue.append(operator_stack.pop())
    
    if operator_stack:
      operator_stack.pop()

  @classmethod
  def _handle_operator(
      cls, 
      token: str, 
      operator_stack: list[str], 
      output_queue: list[str]
    ) -> None:
    """Process an operator token according to precedence and associativity rules."""

    while operator_stack and operator_stack[-1] != "(":
      if not cls._should_pop(token, operator_stack[-1]):
        break

      output_queue.append(operator_stack.pop())
    
    operator_stack.append(token)
  
  @classmethod
  def _should_pop(cls, incoming: str, stack_top: str) -> bool:
    """Determine whether the top operator should be popped before pushing another."""
    incoming_prec = cls._OPERATORS[incoming]["prec"]
    incoming_assoc = cls._OPERATORS[incoming]["assoc"]
    stack_prec = cls._OPERATORS[stack_top]["prec"]

    return (
      (incoming_assoc == "L" and incoming_prec <= stack_prec)
      or (incoming_assoc == "R" and incoming_prec < stack_prec)
    )
  # -  -  -  -  -

  @classmethod
  def _evaluate_postfix(cls, postfix: list[str]) -> str:
    """Evaluate a postfix expression and return the formatted result."""
    stack: list[float] = []
    
    for token in postfix:
      if cls._is_number(token):
        stack.append(float(token))
      elif token == "u-":
        stack.append(-stack.pop())
      elif token == "u+":
        stack.append(stack.pop())
      else:
        value1: float = stack.pop()
        value2: float = stack.pop()
        stack.append(cls._binary_eval(value1, value2, operator=token))
    
    result: float = stack.pop()

    # return formatted integer string if the float value is close to rounded int
    if math.isclose(result, round(result)):
      return str(int(round(result)))
    
    # return formatted float string with up to 9 significant digits
    return f"{result:.9g}"

  # ---- evaluate_postfix() method utility (private) -  -  -  -  -
  @staticmethod
  def _binary_eval(value1: float, value2: float, operator: str) -> float:
    """Apply a binary arithmetic operator to two operands."""
    Validator.validate_evaluation(operator=operator, divisor=value1)

    try:
      match operator:
        # value2 then value1 order following postfix expression
        case "+": result = value2 + value1
        case "-": result = value2 - value1
        case "*": result = value2 * value1
        case "/": result = value2 / value1
        case "^": result = value2 ** value1
        case _: result = float(0)

    except OverflowError:
      raise ValueError(f"Numerical result out of range: {value2} {operator} {value1}")

    if not math.isfinite(result):
      raise ValueError(f"Numerical result out of range: {value2} {operator} {value1}")

    return result

  # UTILITY METHOD (private) ------------------------------

  @staticmethod
  def _is_number(token: str) -> bool:
    """Return True if the token represents a numeric value."""
    # .replace() for decimal number checked by .isdigit()
    return token.replace(".", "", 1).isdigit()
