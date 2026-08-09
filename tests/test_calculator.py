import pytest

from modules.calculator import Calculator


# Test calculate() ------------------------------

@pytest.mark.parametrize("expression, expected", [
  ("1+2", "3"),
  ("4.5-6*7", "-37.5"),
  ("8(9^(1+2))", "5832"),
  ("-3+--4", "1"),
])
def test_calculate_success(expression, expected):
  assert Calculator.calculate(expression) == expected

@pytest.mark.parametrize("invalid_expression", [
  (""),
  ("1a"),
  ("*1"),
  (")1"),
  ("1()"),
  ("(1))"),
  ("1%1"),
  ("10000^10000"),
])
def test_calculate_valueerror(invalid_expression):
  with pytest.raises(ValueError):
    Calculator.calculate(expression=invalid_expression)


# Test _tokenize() ------------------------------

@pytest.mark.parametrize("expression, expected", [
  ("", []),
  ("1+1", ["1", "+", "1"]),
  ("1.1+1.1", ["1.1", "+", "1.1"]),
  (
    "-1(1.1*1)/-1.1^(1)", 
    ["-", "1", "(", "1.1", "*", "1", ")", "/", "-", "1.1", "^", "(", "1", ")"]
  ),
])
def test__tokenize(expression, expected):
  assert Calculator._tokenize(expression) == expected


# Test _normalize_unary_operators() ------------------------------

@pytest.mark.parametrize("tokens, expected", [
  (["+", "1"], ["u+", "1"]),
  (["-", "1"], ["u-", "1"]),
  (["1", "+", "-", "-", "1"], ["1", "+", "u-", "u-", "1"]),
])
def test__normalize_unary_operators(tokens, expected):
  assert Calculator._normalize_unary_operators(tokens) == expected