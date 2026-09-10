"""디렉터리 구조에서 pytest 마커를 자동으로 붙인다.

    exercises/week_01_linked_list/cpp/medium_reverse_in_k_groups/tests.py
                                  ^^^  ^^^^^^
                                  언어  난이도   ->  @pytest.mark.cpp @pytest.mark.medium

덕분에 `pytest -m c`, `pytest -m "cpp and easy"` 같은 필터가 그대로 먹는다.
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
