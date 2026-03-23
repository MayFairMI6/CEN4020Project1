"""conftest.py – add src/ to sys.path so all test modules can import
game source files directly (e.g. ``from level_timer import LevelTimer``)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
