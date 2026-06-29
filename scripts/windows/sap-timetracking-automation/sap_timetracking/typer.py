"""Keyboard automation utilities for typing text into other applications."""

import re
import time

import pyautogui


def type_text(
    text: str,
    delay_before_start: int | float = 3,
    interval_between_keys: float = 0.05,
    pause_duration: int | float = 1,
) -> None:
    """Types the given text as keyboard input with support for special keys.

    Special keys can be included using curly braces, e.g., {tab}, {enter}, {backspace}.
    Supported special keys include: enter, tab, esc, backspace, delete, up, down,
    left, right, home, end, pageup, pagedown, f1-f12, shift, ctrl, alt, and more.

    Args:
        text:
            The text to type. Can include special keys in {key} format.
        delay_before_start:
            Time in seconds before typing begins. Defaults to 3.
        interval_between_keys:
            Delay between each character typed. Defaults to 0.05.
        pause_duration:
            Duration in seconds to pause when {pause} is encountered. Defaults to 1.

    Example:
        >>> type_text("Hello{tab}World{enter}")
        >>> type_text("Name: John Doe", delay_before_start=5)
    """
    print(
        f"Typing will start in {delay_before_start} seconds... "
        "Switch to your target window."
    )
    time.sleep(delay_before_start)

    # Parse text for special keys in {key} format
    pattern = r"\{([^}]+)\}"
    parts = re.split(pattern, text)

    for i, part in enumerate(parts):
        if i % 2 == 0:
            if part:
                pyautogui.typewrite(part, interval=interval_between_keys)
        else:
            if part.lower() == "pause":
                time.sleep(pause_duration)
                continue
            else:
                pyautogui.press(part.lower())
                time.sleep(interval_between_keys)

    print("Finished typing.")
