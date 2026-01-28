import pytest
from projectlog.lint import validate_project_name


def test_valid_name():
    validate_project_name("Smith_TestProject_2024")


def test_invalid_name():
    with pytest.raises(ValueError):
        validate_project_name("badname")
