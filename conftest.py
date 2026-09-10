"""리포지터리 루트를 import 경로에 올려 각 주차 테스트가 harness를 쓸 수 있게 한다."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
