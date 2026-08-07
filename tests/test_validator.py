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


# Test tokens_lexical_check() ------------------------------

@pytest.mark.parametrize("tokens, expression", [
  (["0"],           "0"  ),
  (["1", "+"],      "1+" ),
  (["2", "-", "3"], "2-3"),
  (["*"],           "*"  ),
  (["(", " ", "/"], "( /"),
])
def test_tokens_lexical_check_success(tokens, expression):
  assert Validator.tokens_lexical_check(tokens, expression)

@pytest.mark.parametrize("tokens, expression", [
  (["0"],           "0 " ),
  (["1", "+"],      "1 +"),
  (["2", "3"],      "-23"),
  (["^", "4", ")"], "^)" ),
])
def test_tokens_lexical_check_invalid(tokens, expression):
  with pytest.raises(
    ValueError,
    match="Expression contain an invalid token"
  ):
    Validator.tokens_lexical_check(tokens, expression)


# Test validate_tokens() ------------------------------

@pytest.mark.parametrize("tokens", [
  (["0"]),
  (["1", "+", "2"]),
  (["3", "-", "(", "4", "*", "5", ")", "/", "u-", "6", "^", "7.8"]),
])
def test_validate_tokens_success(tokens):
  assert Validator.validate_tokens(tokens)

@pytest.mark.parametrize("failed_tokens", [
  (["+", ")", "-", "(", "u+"]),
  (["(", "0", "(", ")"]),
  (["1", "u-", "*", "/", ")", "2.3"]),
])
def test_validate_tokens_failed(failed_tokens):
  with pytest.raises(ValueError):
    Validator.validate_tokens(tokens=failed_tokens)


# Test _start_end_check() ------------------------------

@pytest.mark.parametrize("invalid_tokens, error_message", [
  ([],          "Token list is empty"                            ),
  (["+"],       "Tokens cannot have an operator as a first token"),
  ([")"],       "The first token contain invalid parenthesis"    ),
  (["1", "+"],  "Tokens cannot have an operator as a last token" ),
  (["1", "("],  "The last token contain invalid parenthesis"     ),
  (["1", "u+"], "The last token contain unary operator"          ),
])
def test__start_end_check_invalid(invalid_tokens, error_message):
  with pytest.raises(ValueError, match=error_message):
    Validator._start_end_check(tokens=invalid_tokens)


# Test _parentheses_check() ------------------------------

@pytest.mark.parametrize("invalid_tokens, error_message", [
  (["(", ")"],           "Tokens contain empty parentheses"),
  (["(", "1", ")", ")"], "Tokens contain invalid parentheses"),
  (["(", "(", "1", ")"], "Tokens contain invalid parentheses"),
])
def test__parentheses_check_invalid(invalid_tokens, error_message):
  with pytest.raises(ValueError, match=error_message):
    Validator._parentheses_check(tokens=invalid_tokens)


# Test _grammar_check() ------------------------------

@pytest.mark.parametrize("invalid_tokens", [
  (["1", "u+"]),
  (["+", ")"]),
  (["(", "+"]),
  ([")", "1"]),
  (["u+", "+"]),
])
def test__grammar_check_invalid(invalid_tokens):
  with pytest.raises(ValueError, match="Invalid token order"):
    Validator._grammar_check(tokens=invalid_tokens)