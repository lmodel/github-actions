"""Data model package for github-actions."""

from pathlib import Path
from .github_actions import *  # noqa: F403

THIS_PATH = Path(__file__).parent

SCHEMA_DIRECTORY = THIS_PATH.parent / "schema"
MAIN_SCHEMA_PATH = SCHEMA_DIRECTORY / "github_actions.yaml"
