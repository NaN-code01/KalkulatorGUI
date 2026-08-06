import pytest

from modules.validator import Validator

# Test validate_expression() ------------------------------

@pytest.mark.parametrize("expression", [
  ("12340"),
  ("+-*/^"),
  ("()"),
  ("."),
  ("12340+-*/^()."),
  ("1.2+3-(4*0)/1^2"),
])
def test_validate_expression_success(expression):
  assert Validator.validate_expression(expression)

def test_validate_expression_empty():
  empty_expression = ""

  with pytest.raises(
    ValueError,
    match="Expression cannot be empty"
  ):
    Validator.validate_expression(expression=empty_expression)

@pytest.mark.parametrize("invalid_expression", [
  (" 1+1"),
  ("e1+1"),
  ("1+1 "),
  ("1+1e"),
  ("1+1:"),
  ("1+1,"),
  ("1+1>"),
  ("1+1?"),
])
def test_validate_expression_invalid(invalid_expression):
  with pytest.raises(
    ValueError,
    match="Expression contain invalid character"
  ):
    Validator.validate_expression(expression=invalid_expression)