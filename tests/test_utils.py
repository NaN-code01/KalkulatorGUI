import json

import pytest

from modules.utils import Utility


# Test validate_and_load_json() ------------------------------

def test_validate_and_load_json_success(tmp_path):
  data = {
    "word": "hello",
    "number": 17,
    "boolean": True,
    "list": [1, 2, 3],
  }

  json_file = tmp_path / "data.json"
  json_file.write_text(
    json.dumps(data),
    encoding="utf-8"
  )

  result = Utility.validate_and_load_json(str(json_file))
  assert result == data

def test_validate_and_load_json_file_not_found():
    file_path = "does_not_exist.json"

    with pytest.raises(
        FileNotFoundError,
        match=r"Error: The file at does_not_exist\.json was not found\."
    ):
      Utility.validate_and_load_json(file_path)

@pytest.mark.parametrize("content", [
  '{"a":}',
  '{"a":1,,}',
  '{"word":"Hello",}',
])
def test_validate_and_load_json_invalid_json(tmp_path, content):
  invalid_json_file = tmp_path / "invalid.json"
  invalid_json_file.write_text(content, encoding="utf-8")

  with pytest.raises(
    ValueError,
    match=r"Compatibility Error: Invalid JSON syntax\."
  ):
    Utility.validate_and_load_json(str(invalid_json_file))


# Test validate_is_number() ------------------------------

@pytest.mark.parametrize("token, expected", [
  ("1", True),
  ("2", True),
  ("0", True),
  ("10", True),
  ("100", True),
  ("1000", True),
  ("001", True),
  ("010", True),
  ("1.0", True),
  ("1.1", True),
  ("1.01", True),
  ("1.001", True),
  ("1.010", True),
  ("1.100", True),
  ("0.1", True),
  ("0.0", True),
  (".0", True),
  (".1", True),

  ("", False),
  (" ", False),
  ("..", False),
  ("1.1.1", False),
  ("1 ", False),
  (" 1", False),
  ("a", False),
])
def test_is_number(token, expected):
  assert Utility.is_number(token) == expected