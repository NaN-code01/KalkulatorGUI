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

  with pytest.raises(ValueError, match="Expression cannot be empty"):
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
    match="Expression contains an invalid character"
  ):
    Validator.validate_expression(expression=invalid_expression)


# Test tokens_lexical_check() ------------------------------

@pytest.mark.parametrize("tokens, expression", [
  (["0"],                  "0"     ),
  (["1", "+"],             "1+"    ),
  (["2", "-", "3"],        "2-3"   ),
  (["*", "4.5", "(", ")"], "*4.5()"),
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
  with pytest.raises(ValueError, match="Expression contains an invalid token"):
    Validator.tokens_lexical_check(tokens, expression)


# Test validate_tokens() ------------------------------

@pytest.mark.parametrize("tokens", [
  (["0"]),
  (["1", "+", "2"]),
  (["3", "-", "(", "4", "*", "5", ")", "/", "u-", "6", "^", "7.8"]),
])
def test_validate_tokens_success(tokens):
  assert Validator.validate_tokens(tokens)

@pytest.mark.parametrize("tokens", [
  ["u-", "1"],
  ["u+", "1"],
  ["u-", "u-", "1"],
  ["u+", "u-", "1"],
  ["u-", "(", "1", "+", "2", ")"],
])
def test_validate_tokens_unary_success(tokens):
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

@pytest.mark.parametrize("tokens", [
  ["1"],
  ["1", "+", "2"],
  ["(", "1", ")"],
  ["u-", "1"],
  ["u+", "(", "1", ")"],
])
def test__start_end_check_success(tokens):
  assert Validator._start_end_check(tokens)

@pytest.mark.parametrize("invalid_tokens, error_message", [
  ([],          "Token list is empty"                            ),
  (["+"],       "Tokens cannot have an operator as a first token"),
  ([")"],       "The first token contains an invalid parenthesis"),
  (["1", "+"],  "Tokens cannot have an operator as a last token" ),
  (["1", "("],  "The last token contains an invalid parenthesis" ),
  (["1", "u+"], "The last token contains an unary operator"      ),
])
def test__start_end_check_invalid(invalid_tokens, error_message):
  with pytest.raises(ValueError, match=error_message):
    Validator._start_end_check(tokens=invalid_tokens)


# Test _parentheses_check() ------------------------------

@pytest.mark.parametrize("tokens", [
  ["1"],
  ["(", "1", ")"],
  ["(", "1", "+", "2", ")"],
  ["(", "(", "1", "+", "2", ")", "*", "3", ")"],
  ["1", "+", "(", "2", "*", "3", ")"],
])
def test__parentheses_check_success(tokens):
  assert Validator._parentheses_check(tokens)

@pytest.mark.parametrize("invalid_tokens, error_message", [
  (["(", ")"],           "Tokens has an empty parentheses"),
  (["(", "1", ")", ")"], "Tokens contains an invalid parentheses"),
  (["(", "(", "1", ")"], "Tokens contains an invalid parentheses"),
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


# Test _token_type() ------------------------------

@pytest.mark.parametrize("token, expected", [
  ("0",       "number"),
  ("1",       "number"),
  ("234",     "number"),
  ("1.1",     "number"),
  ("356.789", "number"),

  ("+", "operator"),
  ("-", "operator"),
  ("*", "operator"),
  ("/", "operator"),
  ("^", "operator"),

  ("(", "lparen"),
  (")", "rparen"),

  ("u+", "unary"),
  ("u-", "unary"),
])
def test__token_type_success(token, expected):
  assert Validator._token_type(token) == expected

@pytest.mark.parametrize("invalid_token", [
  (""),
  (" "),
  ("  "),
  ("."),
  (".."),
  ("1.1.1"),
  ("a"),
  (","),
  (":"),
  (">"),
])
def test__token_type_invalid(invalid_token):
  with pytest.raises(ValueError, match="Token typing is invalid"):
    Validator._token_type(token=invalid_token)


# Test _compare_type() ------------------------------

@pytest.mark.parametrize("prev_type, curr_type, expected", [
 ("number", "operator", True),
 ("number", "lparen", True),
 ("number", "rparen", True),

 ("operator", "number", True),
 ("operator", "lparen", True),
 ("operator", "unary", True),

 ("lparen", "number", True),
 ("lparen", "lparen", True),
 ("lparen", "unary", True),

 ("rparen", "operator", True),
 ("rparen", "lparen", True),
 ("rparen", "rparen", True),

 ("unary", "number", True),
 ("unary", "lparen", True),
 ("unary", "unary", True),

 ("number", "unary", False),
 ("operator", "rparen", False),
 ("lparen", "rparen", False),
 ("rparen", "unary", False),
 ("unary", "rparen", False),
])
def test__compare_type(prev_type, curr_type, expected):
  assert Validator._compare_type(prev_type, curr_type) == expected 


# Test validate_expression_length() ------------------------------

@pytest.mark.parametrize("expression, max_length", [
  ("1", 2),
  ("1", 200000),
  ("123", 4),
  ("123456789", 10),
  ("123456789abcdefghij", 20),
])
def test_validate_expression_length_success(expression, max_length):
  assert Validator.validate_expression_length(expression, max_length)

@pytest.mark.parametrize("expression, max_length", [
  ("", 0),
  ("1", 0),
  ("1234567890", 10),
  ("123456789abcdefghij", 10),
])
def test_validate_expression_length_max_exceed(expression, max_length):
  with pytest.raises(
    IndexError, 
    match=(
      f"Maximum length of {max_length} reached.\n"
      f"Current length: {len(expression)}"
    )
  ):
    Validator.validate_expression_length(expression, max_length)


# Test validate_evaluation() ------------------------------

@pytest.mark.parametrize("operator, divisor", [
  ("+", 0.0),
  ("+", 1.0),
  ("-", 0.0),
  ("-", 1.0),
  ("*", 0.0),
  ("*", 1.0),
  ("/", 1.0),
  ("^", 0.0),
  ("^", 1.0),
])
def test_validate_evaluation_success(operator, divisor):
  assert Validator.validate_evaluation(operator, divisor)

@pytest.mark.parametrize("unsupported_operator, divisor", [
  ("", 1.0),
  (" ", 1.0),
  ("<", 1.0),
  (">", 1.0),
  ("%", 1.0),
  ("&", 1.0),
  ("!", 1.0),
])
def test_validate_evaluation_unsupported_operator(
  unsupported_operator, 
  divisor
):
  with pytest.raises(
    ValueError,
    match=f"Unsupported operator: {unsupported_operator}"
  ):
    Validator.validate_evaluation(
      operator=unsupported_operator, 
      divisor=divisor
    )

def test_validate_evaluation_zero_division():
  with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
    Validator.validate_evaluation(operator="/", divisor=0.0)