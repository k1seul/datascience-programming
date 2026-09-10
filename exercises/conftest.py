"""Derive pytest markers from the directory layout.

    exercises/week_01_linked_list/cpp/medium_reverse_in_k_groups/tests.py
                                  ^^^  ^^^^^^
                              language  difficulty  ->  @pytest.mark.cpp @pytest.mark.medium

This is what makes `pytest -m c` and `pytest -m "cpp and easy"` work without any
per-file boilerplate.
"""

from pathlib import Path

import pytest

LANGUAGES = {"c", "cpp", "python"}
DIFFICULTIES = {"impl", "easy", "medium", "hard"}


def pytest_collection_modifyitems(config, items):
    for item in items:
        task_dir = Path(str(item.fspath)).parent
        language = task_dir.parent.name
        difficulty = task_dir.name.partition("_")[0]
        if language in LANGUAGES:
            item.add_marker(getattr(pytest.mark, language))
        if difficulty in DIFFICULTIES:
            item.add_marker(getattr(pytest.mark, difficulty))
