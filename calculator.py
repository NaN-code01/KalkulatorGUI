import re
from typing import TypedDict

class OperatorInfo(TypedDict):
  prec: int
  assoc: str

class Calculator:
  def __init__(self) -> None:
    self.allowed_chars: set[str] = set("0123456789()+-*/.")
    
    # Define operator precedence and associativity: "L" for Left, "R" for Right
    self.operators: dict[str, OperatorInfo] = {
      "+": {"prec": 1, "assoc": "L"},
      "-": {"prec": 1, "assoc": "L"},
      "*": {"prec": 2, "assoc": "L"},
      "/": {"prec": 2, "assoc": "L"},
      "^": {"prec": 3, "assoc": "R"}
    }
  
  def tokenize(self, expression: str) -> list[str]:
    token_pattern = re.compile(r"\d+ (?:\.\d+)? | [+\-*/^()]")
    return token_pattern.findall(expression)

  def infix_to_postfix(self, tokens: list[str]) -> list[str]:
    output_queue: list[str] = []
    operator_stack: list[str] = []

    # Shunting Yard Algorithm
    for token in tokens:

      # number handling
      # .replace() for decimal number checked by .isdigit()
      if token.replace(".", "", 1).isdigit():
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
      elif token in self.operators:
        token_prec: int = self.operators[token]["prec"]
        token_assoc: str = self.operators[token]["assoc"] 
        
        while operator_stack and operator_stack[-1] != "(":
          operator_prec: int = self.operators[operator_stack[-1]]["prec"]
          
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

  def evaluate_postfix(self) -> float:
    pass

def main() -> None:
  pass

if __name__ == "__main__":
  main()