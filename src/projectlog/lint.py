import re

PROJECT_NAME_RE = re.compile(r"^[A-Z][a-zA-Z]+_[A-Za-z0-9]+_[0-9]{4}$")


def validate_project_name(name):
    if not PROJECT_NAME_RE.match(name):
        raise ValueError(
            f"Invalid project name '{name}'. "
            "Expected format: PIName_BriefDescription_Year"
        )
