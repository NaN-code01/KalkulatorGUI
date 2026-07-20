import re
import math
from typing import TypedDict
from validator import Validator

class OperatorInfo(TypedDict):
  prec: int
  assoc: str

class Calculator:
  # Define operator precedence and associativity: "L" for Left, "R" for Right
  OPERATORS: dict[str, OperatorInfo] = {
    "+": {"prec": 1, "assoc": "L"},
    "-": {"prec": 1, "assoc": "L"},
    "*": {"prec": 2, "assoc": "L"},
    "/": {"prec": 2, "assoc": "L"},
    "^": {"prec": 3, "assoc": "R"}
  }

  # Define token pattern for regex
  TOKEN_PATTERN = re.compile(
    r"""
    \d+(?:\.\d+)?   # number
    |               # or
    [+\-*/^()]      # operator or parenthesis
    """,
    re.VERBOSE
  )

  @classmethod
  def tokenize(cls, expression: str) -> list[str] | None:
    if not Validator.validate_expression(expression=expression):
      return

    return cls.TOKEN_PATTERN.findall(expression)

  @classmethod
  def infix_to_postfix(cls, tokens: list[str]) -> list[str] | None:
    if not Validator.validate_tokens(tokens=tokens, expression=""):
      return

    operators: dict = cls.OPERATORS
    output_queue: list[str] = []
    operator_stack: list[str] = []

    # Shunting Yard Algorithm
    for token in tokens:

      # number handling
      if cls._is_number(token):
        output_queue.append(token)
      
      # parentheses handling
      elif token == "(":
        operator_stack.append(token)
      elif token == ")":
        while operator_stack and operator_stack[-1] != "(":
          output_queue.append(operator_stack.pop())
        
        if operator_stack:
          operator_stack.pop()
      
      # operator handling
      elif token in operators:
        token_prec: int = operators[token]["prec"]
        token_assoc: str = operators[token]["assoc"] 
        
        while operator_stack and operator_stack[-1] != "(":
          operator_prec: int = operators[operator_stack[-1]]["prec"]
          
          # Apply precedence and associativity rules
          if (
            (token_assoc == "L" and token_prec <= operator_prec) or
            (token_assoc == "R" and token_prec < operator_prec)
          ):
            output_queue.append(operator_stack.pop())
          else:
            break
        
        operator_stack.append(token)
    
    # .pop() remaining operators to outpuut
    while operator_stack:
      output_queue.append(operator_stack.pop())
    
    return output_queue

  @classmethod
  def _should_pop(cls, incoming: str, stack_top: str) -> bool:
    incoming_prec = cls.OPERATORS[incoming]["prec"]
    incoming_assoc = cls.OPERATORS[incoming]["assoc"]
    stack_prec = cls.OPERATORS[stack_top]["prec"]

    return (
      (incoming_assoc == "L" and incoming_prec <= stack_prec)
      or
      (incoming_assoc == "R" and incoming_prec < stack_prec)
    )

  @classmethod
  def evaluate_postfix(cls, postfix: list[str]) -> str:
    stack: list[float] = []
    
    for token in postfix:
      if cls._is_number(token):
        stack.append(float(token))
      
      else:
        value1: float = stack.pop()
        value2: float = stack.pop()
        stack.append(cls.basic_eval(value1, value2, operator=token))
    
    result: float = stack.pop()

    # return str formated int if the float value is close to rounded int
    if math.isclose(result, round(result)):
      return str(int(round(result)))
    
    # return str formated float with up to 9 significant digits
    return f"{result:.9g}"

  @staticmethod
  def basic_eval(value1: float, value2: float, operator: str) -> float:
    match(operator):
      # value2 then value1 order following postfix expression
      case "+": return value2 + value1
      case "-": return value2 - value1
      case "*": return value2 * value1
      case "/": return value2 / value1
      case "^": return value2 ** value1
      case _: return float(0)

  # UTILITY METHOD (private) ------------------------------

  @staticmethod
  def _is_number(string: str) -> bool:
    # .replace() for decimal number checked by .isdigit()
    return string.replace(".", "", 1).isdigit()

def main() -> None:
  pass

if __name__ == "__main__":
  main()