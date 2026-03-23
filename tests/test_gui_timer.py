# tests/test_gui_timer.py
#
# Unit tests for src/gui/timer.py (Timer class).
# pygame.time.get_ticks is mocked so no display is needed.

import pytest
from unittest.mock import patch


# ---------------------------------------------------------------------------
# elapsed() tests
# ---------------------------------------------------------------------------

def test_elapsed_before_start_is_zero():
    from gui.timer import Timer
    t = Timer()
    with patch("gui.timer.pygame.time.get_ticks", return_value=0):
        assert t.elapsed() == 0


def test_elapsed_returns_seconds_since_start():
    from gui.timer import Timer
    t = Timer()
    with patch("gui.timer.pygame.time.get_ticks", return_value=0):
        t.start(60)
    with patch("gui.timer.pygame.time.get_ticks", return_value=15_000):
        assert t.elapsed() == 15


def test_elapsed_frozen_after_stop():
    """elapsed() must stay fixed after stop(), regardless of further ticks."""
    from gui.timer import Timer
    t = Timer()
    with patch("gui.timer.pygame.time.get_ticks", return_value=0):
        t.start(60)
    with patch("gui.timer.pygame.time.get_ticks", return_value=20_000):
        t.stop()
    # time advances further – elapsed must not change
    with patch("gui.timer.pygame.time.get_ticks", return_value=99_999):
        assert t.elapsed() == 20


# ---------------------------------------------------------------------------
# left() / overtime() tests
# ---------------------------------------------------------------------------

def test_left_decreases_over_time():
    from gui.timer import Timer
    t = Timer()
    with patch("gui.timer.pygame.time.get_ticks", return_value=0):
        t.start(60)
    with patch("gui.timer.pygame.time.get_ticks", return_value=25_000):
        assert t.left() == 35


def test_left_never_goes_below_zero():
    from gui.timer import Timer
    t = Timer()
    with patch("gui.timer.pygame.time.get_ticks", return_value=0):
        t.start(30)
    with patch("gui.timer.pygame.time.get_ticks", return_value=50_000):
        assert t.left() == 0


def test_left_returns_none_when_no_limit():
    from gui.timer import Timer
    t = Timer()
    with patch("gui.timer.pygame.time.get_ticks", return_value=0):
        t.start(0)
    with patch("gui.timer.pygame.time.get_ticks", return_value=10_000):
        assert t.left() is None


def test_overtime_positive_when_past_limit():
    from gui.timer import Timer
    t = Timer()
    with patch("gui.timer.pygame.time.get_ticks", return_value=0):
        t.start(30)
    with patch("gui.timer.pygame.time.get_ticks", return_value=45_000):
        assert t.overtime() == 15


def test_overtime_zero_within_limit():
    from gui.timer import Timer
    t = Timer()
    with patch("gui.timer.pygame.time.get_ticks", return_value=0):
        t.start(60)
    with patch("gui.timer.pygame.time.get_ticks", return_value=10_000):
        assert t.overtime() == 0


# ---------------------------------------------------------------------------
# calculate_score() tests
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("limit, elapsed_ms, expected_delta", [
    (60,  40_000,  20),   # 20 s unused  → +20
    (60,  60_000,   0),   # exactly on time → 0
    (60,  70_000, -10),   # 10 s over     → -10
    (30,   0,      30),   # all time left  → +30
    (80,  80_000,   0),   # 80 s limit, 80 s used → 0
])
def test_calculate_score(limit, elapsed_ms, expected_delta):
    from gui.timer import Timer
    t = Timer()
    with patch("gui.timer.pygame.time.get_ticks", return_value=0):
        t.start(limit)
    with patch("gui.timer.pygame.time.get_ticks", return_value=elapsed_ms):
        t.stop()
    assert t.calculate_score() == expected_delta


def test_calculate_score_no_limit_returns_zero():
    from gui.timer import Timer
    t = Timer()
    with patch("gui.timer.pygame.time.get_ticks", return_value=0):
        t.start(0)
    with patch("gui.timer.pygame.time.get_ticks", return_value=120_000):
        t.stop()
    assert t.calculate_score() == 0


# ---------------------------------------------------------------------------
# stop() idempotency
# ---------------------------------------------------------------------------

def test_stop_when_not_running_does_not_raise():
    from gui.timer import Timer
    t = Timer()
    # never started – stop should be a no-op
    t.stop()
    assert t.elapsed() == 0
