"""Module for typing text as keyboard input using pyautogui."""

import re
import time
from dataclasses import dataclass
from pprint import pprint

import pyautogui

@dataclass
class WorkLogEntry:
    """Represents a single work log entry with start time, end time, and description."""
    start_time: str
    end_time: str
    description: str
    order_number: str
    order_type: str

@dataclass
class Meeting(WorkLogEntry):
    """Represents a meeting entry in the work log."""
    order_number: str = "900000009680"
    order_type: str = "HR0074"

@dataclass
class Task(WorkLogEntry):
    """Represents a task entry in the work log."""
    order_number: str = "900000009965"
    order_type: str = "HR0016"

@dataclass
class AdminTask(WorkLogEntry):
    order_number: str = "900000009681"
    order_type: str = "HR0074"

@dataclass
class Course(WorkLogEntry):
    order_number: str = "900000009684"
    order_type: str = "HR0074"

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
        text: The text to type. Can include special keys in {key} format.
        delay_before_start: Time in seconds before typing begins. Defaults to 3.
        interval_between_keys: Delay between each character typed. Defaults to 0.05.
        pause_duration: Duration in seconds to pause when {pause} is encountered. Defaults to 1.

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
    # print(f"Parsed text into parts: {parts}")

    for i, part in enumerate(parts):
        # print(f"Processing part: '{part}' (index {i})")
        if i % 2 == 0:
            # print(f"Typing regular text: '{part}'")
            if part:
                pyautogui.typewrite(part, interval=interval_between_keys)
                # for char in part:
                #     pyautogui.write(char)
                #     # time.sleep(interval_between_keys)
        else:
            if part.lower() == "pause":
                # print(f"Pausing for {pause_duration} seconds...")
                time.sleep(pause_duration)
                continue
            else:
                # print(f"Typing special key: '{part}'")
                # Special key
                pyautogui.press(part.lower())
                time.sleep(interval_between_keys)

    print("Finished typing.")

def create_work_log_entries(work_log_entries: list[WorkLogEntry]) -> str:
    """Creates a formatted string for work log entries.

    Args:
        work_log_entries: A list of WorkLogEntry objects representing individual work log entries.

    Returns:
        A formatted string containing all work log entries.

    Example:
    """
    formatted_entries: list[str] = []
    for i, entry in enumerate(work_log_entries):
        if i > 0 and work_log_entries[i-1].end_time != entry.start_time:
            print(f"Warning: Gap detected between entry {i-1} and {i}. "
                f"Previous end time ({work_log_entries[i-1].end_time}) "
                f"does not match current start time ({entry.start_time})")

        formatted_entry: str = (
            f"{entry.start_time}{{tab}}{entry.end_time}{{tab}}{{tab}}{{tab}}"
            f"{entry.order_number}{{tab}}{entry.order_type}{{tab}}N{{pause}}{{tab}}"
            f"{entry.description}"
        )
        formatted_entries.append(formatted_entry)
    return "{tab}{tab}".join(formatted_entries)

if __name__ == "__main__":
    W = WorkLogEntry
    T = Task
    M = Meeting
    A = AdminTask
    C = Course

    # work log entries
    wle: list[WorkLogEntry]

    # current task
    cr: str

    # cr = "GitLab production ready deployment experimentation"
    # cr = "OpenShift experimental cluster setup and testing"
    cr_wsl = "WSL custom kernel patch (security: copy-fail, etc.)"
    cr_km = "Kubernetes (Tanzu) monitoring solution evaluation"
    cr_cks = "CKS course - Certified Kubernetes Security Specialist course (Linux Foundation)"


        # M("10:00","11:00","Weekly Unified Enterprise JFX"),
        # M("14:00","14:30","A&AP Team Call"),


    # 04.05 monday - 4h
    wle = [
        T("09:00","13:00",cr_wsl),
    ]

    # 05.05 tuesday - 7h
    wle = [
        T("09:00","09:30",cr_wsl),
        M("09:30","11:00","A&AP Team Call"),
        T("11:00","11:30",cr_wsl),
        T("11:30","16:00",cr_wsl),
    ]

    # 07.05 thursday - 9h
    wle = [
        T("09:00","13:00",cr_wsl),
        M("13:00","13:30","Monitoring-Konzept für Tanzu K8s - Intro/Update"),
        M("13:30","14:00","A&AP Team Call"),
        T("14:00","18:00",cr_wsl),
    ]

    # 08.05 friday - 6h
    wle = [
        T("09:00","15:00",cr_wsl),
    ]

    # 11.05 monday - 9h
    wle = [
        T("09:00","13:00",cr_wsl),
        T("13:00","18:00",cr_km),
    ]

    # 12.05 tuesday - 8.5h
    wle = [
        T("09:00","09:30",cr_wsl),
        M("09:30","10:00","A&AP Team Call"),
        T("10:00","17:30",cr_wsl),
    ]

    # 15.05 friday - 6h
    wle = [
        T("09:00","13:00",cr_wsl),
        T("13:00","15:00",cr_km),
    ]

    # 18.05 monday - 7.5h
    wle = [
        T("09:00","12:30",cr_wsl),
        T("12:30","16:30",cr_km),
    ]

    # 19.05 tuesday - 9h
    wle = [
        T("09:00","10:00",cr_wsl),
        M("10:00","10:30","A&AP Team Call"),
        T("10:30","18:00",cr_km),
    ]

    # 21.05 thursday - 7.5h
    wle = [
        T("09:00","13:30",cr_km),
        M("13:30","14:00","A&AP Team Call"),
        T("14:00","16:30",cr_km),
    ]

    # 22.05 friday - 5h
    wle = [
        T("09:00","14:00",cr_wsl),
    ]

    # 26.05 tuesday - 8h
    wle = [
        C("09:00","17:00",cr_cks),
    ]

    # 27.05 wednesday - 9h
    wle = [
        C("09:00","17:00",cr_cks),
        T("17:00","18:00",cr_km),
    ]

    # 28.05 thursday - 8.5h
    wle = [
        C("09:00","17:30",cr_cks),
        T("17:00","17:30",cr_km),
    ]

    # 29.05 friday - 8h
    wle = [
        C("09:00","17:00",cr_cks),
    ]




    formatted_work_log: str = create_work_log_entries(wle)
    # print(formatted_work_log)
    type_text(formatted_work_log, 3, 0.01, 1)
