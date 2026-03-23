import pygame

class Timer:
    def __init__(self):
        self.timer_limit = 0
        self.start_ticks = 0
        self.running = False
        self._elapsed_at_stop = 0

    def start(self, seconds):
        self.timer_limit = seconds
        self.start_ticks = pygame.time.get_ticks()
        self.running = True
        self._elapsed_at_stop = 0

    def elapsed(self):
        if not self.running:
            return self._elapsed_at_stop
        return (pygame.time.get_ticks() - self.start_ticks) // 1000

    def left(self):
        if self.timer_limit == 0:
            return None  # no limit
        return max(self.timer_limit - self.elapsed(), 0)

    def overtime(self):
        if self.timer_limit == 0:
            return 0
        return max(self.elapsed() - self.timer_limit, 0)

    def calculate_score(self):
        if self.timer_limit == 0:
            return 0  # no time limit, no bonus or penalty
        elapsed = self.elapsed()
        if elapsed <= self.timer_limit:
            return self.timer_limit - elapsed  # remaining time bonus
        else:
            return -(elapsed - self.timer_limit)  # overtime penalty

    def stop(self):
        if self.running:
            self._elapsed_at_stop = (pygame.time.get_ticks() - self.start_ticks) // 1000
        self.running = False

    def has_run(self) -> bool:
        """Return True if the timer was started at least once."""
        return self.running or self._elapsed_at_stop > 0