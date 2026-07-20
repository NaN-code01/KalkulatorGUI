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
    "^": {"prec": 3, "assoc": "R"}
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
      ValueError: If the expression or generated tokens are invalid.
      ZeroDivisionError: If division by zero occurs.
    """

    Validator.validate_expression(expression=expression)
    
    tokens: list[str] = cls._tokenize(expression)
    Validator.validate_tokens(tokens=tokens, expression=expression)

    postfix: list[str] = cls._infix_to_postfix(tokens)
    result: str = cls._evaluate_postfix(postfix)
    return result

  # -- calculate() method utility (private) - - - - - - - - - -
  @classmethod
  def _tokenize(cls, expression: str) -> list[str]:
    return cls._TOKEN_PATTERN.findall(expression)

  @classmethod
  def _infix_to_postfix(cls, tokens: list[str]) -> list[str]:
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

    while operator_stack and operator_stack[-1] != "(":
      if not cls._should_pop(token, operator_stack[-1]):
        break

      output_queue.append(operator_stack.pop())
    
    operator_stack.append(token)
  
  @classmethod
  def _should_pop(cls, incoming: str, stack_top: str) -> bool:
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
    stack: list[float] = []
    
    for token in postfix:
      if cls._is_number(token):
        stack.append(float(token))
      
      else:
        value1: float = stack.pop()
        value2: float = stack.pop()
        stack.append(cls._basic_eval(value1, value2, operator=token))
    
    result: float = stack.pop()

    # return formatted integer string if the float value is close to rounded int
    if math.isclose(result, round(result)):
      return str(int(round(result)))
    
    # return formatted float string with up to 9 significant digits
    return f"{result:.9g}"

  # ---- evaluate_postfix() method utility (private) -  -  -  -  -
  @staticmethod
  def _basic_eval(value1: float, value2: float, operator: str) -> float:
    match operator:
      # value2 then value1 order following postfix expression
      case "+": 
        return value2 + value1
      case "-": 
        return value2 - value1
      case "*": 
        return value2 * value1
      case "/": 
        Validator.validate_division(value2=value1)
        return value2 / value1
      case "^": 
        return value2 ** value1
      case _: 
        Validator.validate_operator(operator=operator)
        return float(0)

  # UTILITY METHOD (private) ------------------------------

  @staticmethod
  def _is_number(token: str) -> bool:
    # .replace() for decimal number checked by .isdigit()
    return token.replace(".", "", 1).isdigit()
