import pytest

from modules.calculator import Calculator


# Test calculate() ------------------------------

@pytest.mark.parametrize("expression, expected", [
  ("1+2",        "3"),
  ("--5",        "5"),
  ("-(-5)",      "5"),
  ("-3+--4",     "1"),
  ("(2)(3)",     "6"),
  ("2(3+4)",     "14"),
  ("2^3^2",      "512"),
  ("8(9^(1+2))", "5832"),
  ("1/-2",       "-0.5"),
  ("4.5-6*7",    "-37.5"),
])
def test_calculate_success(expression, expected):
  """Test successful arithmetic expression evaluation."""
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
  """Test that invalid expressions raise ValueError."""
  with pytest.raises(ValueError):
    Calculator.calculate(expression=invalid_expression)


# Test _tokenize() ------------------------------

@pytest.mark.parametrize("expression, expected", [
  ("",        []),
  ("1+1",     ["1", "+", "1"]),
  ("1.1+1.1", ["1.1", "+", "1.1"]),
  (
    "-1(1.1*1)/-1.1^(1)",
    ["-", "1", "(", "1.1", "*", "1", ")", "/", "-", "1.1", "^", "(", "1", ")"]
  ),
])
def test__tokenize(expression, expected):
  """Test that an expression is split into individual tokens."""
  assert Calculator._tokenize(expression) == expected


# Test _normalize_unary_operators() ------------------------------

@pytest.mark.parametrize("tokens, expected", [
  (["-", "1"],                ["u-", "1"]),
  (["+", "1"],                ["u+", "1"]),
  (["-", "-", "2"],           ["u-", "u-", "2"]),
  (["1", "+", "-", "2"],      ["1", "+", "u-", "2"]),
  (["1", "*", "-", "2"],      ["1", "*", "u-", "2"]),
  (["(", "-", "2", ")"],      ["(", "u-", "2", ")"]),
  (["1", "/", "-", "2"],      ["1", "/", "u-", "2"]),
  (["1", "^", "-", "2"],      ["1", "^", "u-", "2"]),
  (["1", "+", "-", "-", "1"], ["1", "+", "u-", "u-", "1"]),
])
def test__normalize_unary_operators(tokens, expected):
  """Test that unary operators are normalized correctly."""
  assert Calculator._normalize_unary_operators(tokens) == expected


# Test _insert_implicit_multiplication() ------------------------------

@pytest.mark.parametrize("tokens, expected", [
  (["1", "1"],                     ["1", "*", "1"]),
  (["1", "(", "1", ")"],           ["1", "*", "(", "1", ")"]),
  (["(", "1", ")", "1"],           ["(", "1", ")", "*", "1"]),
  (["(", "1", ")", "(", "1", ")"], ["(", "1", ")", "*", "(", "1", ")"]),
])
def test__insert_implicit_multiplication(tokens, expected):
  """Test that implicit multiplication operators are inserted."""
  assert Calculator._insert_implicit_multiplication(tokens) == expected


# Test _infix_to_postfix() ------------------------------

@pytest.mark.parametrize("tokens, expected", [
  (["1", "+", "2"],                     ["1", "2", "+"]),
  (["u-", "2"],                         ["2", "u-"]),
  (["1", "+", "2", "*", "3"],           ["1", "2", "3", "*", "+"]),
  (["1", "*", "(", "2", "+", "3", ")"], ["1", "2", "3", "+", "*"]),
  (["2", "^", "3", "^", "2"],           ["2", "3", "2", "^", "^"]),
  (["2", "^", "u-", "3"],               ["2", "3", "u-", "^"]),
])
def test__infix_to_postfix(tokens, expected):
  """Test that infix tokens are converted to postfix notation."""
  assert Calculator._infix_to_postfix(tokens) == expected


# Test _handle_close_parenthesis() ------------------------------

def test__handle_close_parenthesis():
  """Test that operators are popped up to the opening parenthesis."""
  operator_stack = ["(", "+", "*"]
  output_queue = ["1"]

  Calculator._handle_close_parenthesis(operator_stack, output_queue)

  assert operator_stack == []
  assert output_queue == ["1", "*", "+"]


# Test _handle_operator() ------------------------------

def test__handle_operator():
  """Test that an operator is handled by precedence and associativity."""
  operator_stack = ["*"]
  output_queue = ["1", "2"]

  Calculator._handle_operator("+", operator_stack, output_queue)

  assert operator_stack == ["+"]
  assert output_queue == ["1", "2", "*"]


# Test _should_pop() ------------------------------

@pytest.mark.parametrize("incoming, stack_top, expected", [
  ("+", "*", True),
  ("*", "+", False),
  ("^", "^", False),
  ("*", "^", True),
  ("+", "^", True),
])
def test__should_pop(incoming, stack_top, expected):
  """Test whether the stack operator should be popped."""
  assert Calculator._should_pop(incoming, stack_top) is expected


# Test _evaluate_postfix() ------------------------------

@pytest.mark.parametrize("postfix, expected", [
  (["1", "2", "+"],           "3"),
  (["2", "3", "^"],           "8"),
  (["1", "2", "+", "3", "*"], "9"),
  (["3", "1", "u-", "+"],     "2"),
  (["2.0", "2.0", "+"],       "4"),
  (["10", "4", "/"],          "2.5"),
  (["2", "3", "/"],           "0.666666667"),
])
def test__evaluate_postfix(postfix, expected):
  """Test that postfix expressions are evaluated and formatted."""
  assert Calculator._evaluate_postfix(postfix) == expected


# Test _binary_eval() ------------------------------

@pytest.mark.parametrize("value1, value2, operator, expected", [
  (2.0, 3.0, "+", 5.0),
  (2.0, 3.0, "-", 1.0),
  (2.0, 3.0, "*", 6.0),
  (3.0, 6.0, "/", 2.0),
  (2.0, 3.0, "^", 9.0),
])
def test__binary_eval_success(value1, value2, operator, expected):
  """Test successful evaluation of binary arithmetic operations."""
  assert Calculator._binary_eval(value1, value2, operator) == expected

def test__binary_eval_zero_division():
  """Test that division by zero raises ZeroDivisionError."""
  with pytest.raises(ZeroDivisionError):
    Calculator._binary_eval(0.0, 1.0, "/")

@pytest.mark.parametrize("value1, value2, operator", [
  (10000.0, 2.0,          "^"),   # triggers OverflowError
  (1.0,     float("inf"), "+"),   # triggers non-finite result
])
def test__binary_eval_valueerror(value1, value2, operator):
  """Test that numerical errors raise ValueError."""
  with pytest.raises(ValueError, match="Numerical result out of range"):
    Calculator._binary_eval(value1, value2, operator)