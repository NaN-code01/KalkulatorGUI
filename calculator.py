import re

class Calculator:
  def __init__(self) -> None:
    self.allowed_chars: set[str] = set("0123456789()+-*/.")
    
    # Define operator precedence and associativity: "L" for Left, "R" for Right
    self.operators: dict[str, dict[str, int | str]] = {
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

    for token in tokens:
      if token.replace(".", "", 1).isdigit():
        output_queue.append(token)

  def evaluate_postfix(self) -> float:
    pass

def main() -> None:
  pass

if __name__ == "__main__":
  main()