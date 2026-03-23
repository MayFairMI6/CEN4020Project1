#!/usr/bin/env python

import pygame
import sys


# ---------------------------------------------------------------------------
# Helper widgets (local to this module)
# ---------------------------------------------------------------------------

class _InputBox:
    """Small single-line numeric input box."""

    COLOR_INACTIVE = (180, 180, 180)
    COLOR_ACTIVE   = (100, 149, 237)

    def __init__(self, x, y, width, height, font, default=""):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.text = str(default)
        self.active = False
        self.color = self.COLOR_INACTIVE
        self.cursor_visible = True
        self.cursor_timer = 0

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color = self.COLOR_ACTIVE if self.active else self.COLOR_INACTIVE

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key in (pygame.K_TAB, pygame.K_RETURN):
                return "next"
            elif event.unicode.isdigit() and len(self.text) < 5:
                self.text += event.unicode
        return None

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)
        pygame.draw.rect(screen, self.color, self.rect, 2, border_radius=5)

        display = self.text if self.text else ""
        text_color = (0, 0, 0) if self.text else (150, 150, 150)
        surf = self.font.render(display, True, text_color)
        screen.blit(surf, (self.rect.x + 8, self.rect.y + 8))

        if self.active:
            now = pygame.time.get_ticks()
            if now - self.cursor_timer > 500:
                self.cursor_visible = not self.cursor_visible
                self.cursor_timer = now
            if self.cursor_visible:
                tw = self.font.size(display)[0]
                cx = self.rect.x + 8 + tw + 2
                pygame.draw.line(screen, (0, 0, 0),
                                 (cx, self.rect.y + 6),
                                 (cx, self.rect.y + self.rect.height - 6), 2)


class _Button:
    """Simple rectangular button."""

    def __init__(self, x, y, width, height, text, font, primary=False):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.primary = primary
        self.hovered = False

    def check_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def draw(self, screen):
        if self.primary:
            color = (70, 160, 100) if not self.hovered else (90, 185, 120)
        else:
            color = (100, 150, 200) if not self.hovered else (120, 170, 220)
        pygame.draw.rect(screen, color, self.rect, border_radius=5)
        pygame.draw.rect(screen, (60, 60, 60), self.rect, 2, border_radius=5)
        surf = self.font.render(self.text, True, (255, 255, 255))
        screen.blit(surf, surf.get_rect(center=self.rect.center))


# ---------------------------------------------------------------------------
# Main screen class
# ---------------------------------------------------------------------------

class TimeLimitScreen:
    """
    Pre-game screen where an administrator (or player) can preset a time
    limit for each level.  Returns a dict ``{1: int, 2: int, 3: int}``
    where 0 means "no time limit".
    """

    DEFAULT_LIMITS = {1: 60, 2: 60, 3: 60}

    # (label, seconds_value) pairs for the quick-preset row
    PRESETS = [
        ("30 sec", 30),
        ("60 sec", 60),
        ("80 sec", 80),
        ("No Limit", 0),
    ]

    WIDTH  = 480
    HEIGHT = 500

    def __init__(self):
        self.limits = dict(self.DEFAULT_LIMITS)
        self.running = True
        self.screen = None
        self.clock  = None
        self.message = ""
        self.message_color = (200, 50, 50)

    # ------------------------------------------------------------------
    def run(self) -> dict:
        """Display the screen and return validated time-limit settings."""
        self._init_pygame()

        while self.running:
            self._handle_events()
            self._draw()
            self.clock.tick(60)

        pygame.quit()
        return self.limits

    # ------------------------------------------------------------------
    def _init_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Matrix Game - Set Time Limits")
        self.clock = pygame.time.Clock()

        self.title_font = pygame.font.Font(None, 42)
        self.font       = pygame.font.Font(None, 28)
        self.small_font = pygame.font.Font(None, 24)

        cx = self.WIDTH // 2

        # Three input boxes – one per level
        box_w, box_h = 90, 38
        label_x = 90
        box_x   = 240
        row_y   = [170, 245, 320]
        self.level_rows_y  = row_y
        self.level_labels  = ["Level 1:", "Level 2:", "Level 3:"]

        self.inputs = []
        for i, y in enumerate(row_y):
            box = _InputBox(box_x, y, box_w, box_h, self.font,
                            str(self.DEFAULT_LIMITS[i + 1]))
            self.inputs.append(box)

        # Quick-preset buttons (apply the chosen value to all three inputs)
        pb_w, pb_h = 88, 30
        total_w = len(self.PRESETS) * pb_w + (len(self.PRESETS) - 1) * 6
        pb_x0 = (self.WIDTH - total_w) // 2
        pb_y  = 115

        self.preset_buttons = []
        for i, (label, val) in enumerate(self.PRESETS):
            x = pb_x0 + i * (pb_w + 6)
            btn = _Button(x, pb_y, pb_w, pb_h, label, self.small_font)
            self.preset_buttons.append((btn, val))

        # "Start Game" button
        sb_w, sb_h = 200, 45
        self.start_btn = _Button(
            (self.WIDTH - sb_w) // 2, 395,
            sb_w, sb_h, "Start Game", self.font, primary=True
        )

    # ------------------------------------------------------------------
    def _handle_events(self):
        mouse_pos = pygame.mouse.get_pos()
        self.start_btn.check_hover(mouse_pos)
        for btn, _ in self.preset_buttons:
            btn.check_hover(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Use defaults and continue
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_RETURN:
                    self._submit()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Preset buttons – apply to all inputs
                for btn, val in self.preset_buttons:
                    if btn.is_clicked(mouse_pos):
                        for inp in self.inputs:
                            inp.text = str(val)
                        self.message = ""
                        break

                if self.start_btn.is_clicked(mouse_pos):
                    self._submit()

            # Forward to input boxes
            for inp in self.inputs:
                inp.handle_event(event)

    # ------------------------------------------------------------------
    def _submit(self):
        """Validate the inputs and close the screen if they are valid."""
        limits = {}
        for i, inp in enumerate(self.inputs):
            text = inp.text.strip()
            if text == "" or text == "0":
                limits[i + 1] = 0
            else:
                try:
                    val = int(text)
                    if val < 0:
                        self.message = "Time limits must be 0 or positive"
                        return
                    limits[i + 1] = val
                except ValueError:
                    self.message = f"Level {i + 1}: please enter a valid number"
                    return

        self.limits  = limits
        self.running = False

    # ------------------------------------------------------------------
    def _draw(self):
        self.screen.fill((240, 245, 250))
        cx = self.WIDTH // 2

        # Title
        title = self.title_font.render("Set Time Limits", True, (50, 50, 80))
        self.screen.blit(title, title.get_rect(center=(cx, 40)))

        subtitle = self.small_font.render(
            "Preset time for each level  (0 = unlimited)", True, (120, 120, 130))
        self.screen.blit(subtitle, subtitle.get_rect(center=(cx, 72)))

        # Preset-button label
        lbl = self.small_font.render(
            "Quick presets (apply to all levels):", True, (80, 80, 100))
        self.screen.blit(lbl, lbl.get_rect(center=(cx, 100)))

        for btn, _ in self.preset_buttons:
            btn.draw(self.screen)

        # Per-level rows
        for i, (label_text, y) in enumerate(
                zip(self.level_labels, self.level_rows_y)):
            lbl = self.font.render(label_text, True, (60, 60, 80))
            self.screen.blit(lbl, (90, y + 8))

            suffix = self.small_font.render("sec  (0 = unlimited)", True, (140, 140, 150))
            self.screen.blit(suffix, (340, y + 12))

            self.inputs[i].draw(self.screen)

        self.start_btn.draw(self.screen)

        if self.message:
            msg = self.small_font.render(self.message, True, self.message_color)
            self.screen.blit(msg, msg.get_rect(center=(cx, 455)))

        pygame.display.flip()
