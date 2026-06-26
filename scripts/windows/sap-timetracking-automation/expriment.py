"""Module for typing text as keyboard input using pyautogui."""

import copy
import re
import time
import datetime

from dataclasses import dataclass
from pprint import pprint
from typing import Optional

import pyautogui


@dataclass
class WorkLogEntry:
    """Represents a single work log entry with start time, end time, and description.

    Attributes:
        start_time: The start time of the entry in HH:MM format.
        end_time: The end time of the entry in HH:MM format.
        description: A short description of the work performed.
        order_number: The SAP order number associated with this entry.
        order_type: The SAP order type code associated with this entry.
        duration: Optional; the duration of the work log entry in hours. If not provided, it can be calculated from start_time and end_time.
    """

    start_time: str
    end_time: str
    description: str
    order_number: str
    order_type: str
    duration: Optional[int | float] = None  # Duration in hours, optional


@dataclass
class Meeting(WorkLogEntry):
    """Represents a meeting entry in the work log.

    Attributes:
        order_number: Defaults to the SAP order number for meetings.
        order_type: Defaults to the SAP order type for meetings.
    """

    order_number: str = "900000009680"
    order_type: str = "HR0074"


@dataclass
class AdminTask(WorkLogEntry):
    """Represents an administrative task entry in the work log.

    Attributes:
        order_number: Defaults to the SAP order number for admin tasks.
        order_type: Defaults to the SAP order type for admin tasks.
    """

    order_number: str = "900000009681"
    order_type: str = "HR0074"


@dataclass
class Course(WorkLogEntry):
    """Represents a training or course entry in the work log.

    Attributes:
        order_number: Defaults to the SAP order number for courses.
        order_type: Defaults to the SAP order type for courses.
    """

    order_number: str = "900000009684"
    order_type: str = "HR0074"


@dataclass
class OpsTicketSNOW(WorkLogEntry):
    """Represents a `Operation` -> `Ticket Based` -> `RT_TB_SHARED_0000` entry in the work log.

    Attributes:
        order_number: Defaults to the SAP order number for RT_TB_SHARED_0000 ticket-based ops.
        order_type: Defaults to the SAP order type for ticket-based ops.
    """

    order_number: str = "900000009965"  # RT_TB_SHARED_0000
    order_type: str = "HR0016"  #


@dataclass
class OpsNoTicketMultipleCustomers(WorkLogEntry):
    """Represents an `Operation` -> `No Ticket` -> `Multiple Customers` entry in the work log.

    Attributes:
        order_number: Defaults to the SAP order number for RT_SHARED_0000 no-ticket ops.
        order_type: Defaults to the SAP order type for A1 Managed DC no-ticket ops.
    """

    order_number: str = "900000009658"  # RT_SHARED_0000
    order_type: str = "HR0323"  # A1 Managed DC


@dataclass
class OpsNoTicketA1OnPrem(WorkLogEntry):
    """Represents an `Operation` -> `No Ticket` -> `A1` -> `OnPrem` -> `A1_RT` entry in the work log.

    Attributes:
        order_number: Defaults to the SAP order number for A1_RT on-prem no-ticket ops.
        order_type: Defaults to the SAP order type for Intern IT-Services no-ticket ops.
    """

    order_number: str = "900000009658"  # A1_RT
    order_type: str = "HR0344"  # Intern IT-Services


@dataclass
class WorkLogDay:
    """Represents a work log for a single day, containing multiple work log entries.

    Attributes:
        weekday: The name of the weekday (e.g. 'Monday'), or None if not set.
        entries: The list of work log entries for this day.
    """

    entries: list[WorkLogEntry]
    weekday: Optional[str] = None


@dataclass
class WorkLogMonth:
    """Represents a work log for a month, containing daily work log entries.

    Attributes:
        month: The month number (1-12).
        year: The four-digit year.
        daily_entries: A mapping from day-of-month (1-31) to the corresponding WorkLogDay.
    """

    month: int
    year: int
    daily_entries: dict[int, WorkLogDay]


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
        work_log_entries:
            A list of WorkLogEntry objects representing individual work log entries.

    Returns:
        A formatted string containing all work log entries.
    """
    formatted_entries: list[str] = []
    for i, entry in enumerate(work_log_entries):
        if i > 0 and work_log_entries[i - 1].end_time != entry.start_time:
            print(
                f"Warning: Gap detected between entry {i-1} and {i}. "
                f"Previous end time ({work_log_entries[i-1].end_time}) "
                f"does not match current start time ({entry.start_time})"
            )

        formatted_entry: str = (
            f"{entry.start_time}{{tab}}{entry.end_time}{{tab}}{{tab}}{{tab}}"
            f"{entry.order_number}{{tab}}{entry.order_type}{{tab}}N{{pause}}{{tab}}"
            f"{entry.description}"
        )
        formatted_entries.append(formatted_entry)
    return "{tab}{tab}".join(formatted_entries)


def get_weekday_name(day: int, month: int, year: int) -> str:
    """Returns the name of the weekday for a given date.

    Args:
        day:
            The day of the month (1-31).
        month:
            The month (1-12).
        year:
            The year (four digits).
    Returns:
        The name of the weekday (e.g., 'monday', 'tuesday', etc.).
    """
    return datetime.date(year, month, day).strftime("%A").lower()


def add_weekday_names_to_work_log(work_log_month: WorkLogMonth) -> None:
    """Adds weekday names to each WorkLogDay in the WorkLogMonth.

    Args:
        work_log_month:
            A WorkLogMonth object containing daily work log entries.
    """
    for day, work_log_day in work_log_month.daily_entries.items():
        weekday_name = get_weekday_name(day, work_log_month.month, work_log_month.year)
        work_log_day.weekday = weekday_name
    return

def get_work_log_entry_duration(work_log_entry: WorkLogEntry) -> int | float:
    """Calculates the duration of a WorkLogEntry in hours.

    Args:
        work_log_entry:
            A WorkLogEntry object for which to calculate the duration.

    Returns:
        The duration of the work log entry in hours as a float.
    """
    if isinstance(work_log_entry.duration, (int, float)):
        return work_log_entry.duration

    if not work_log_entry.start_time or not work_log_entry.end_time:
        raise ValueError("Both start_time and end_time must be provided to calculate duration.")

    try:
        fmt = "%H:%M"
        start = datetime.datetime.strptime(work_log_entry.start_time, fmt)
        end = datetime.datetime.strptime(work_log_entry.end_time, fmt)
    except ValueError as exc:
        raise ValueError("start_time and end_time must be in 'HH:MM' format.") from exc

    return (end - start).seconds / 3600


def fill_work_log_day_with_entries(
    work_log_day: WorkLogDay,
    entries: list[WorkLogEntry],
    default_start_time: Optional[str] = "09:00",
) -> None:
    """Fills a WorkLogDay with duration-based entries, scheduling them into free gaps.

    Existing entries in ``work_log_day`` act as fixed anchors. New entries (which
    must carry a ``duration``) are slotted into the free time slots between anchored
    entries, starting at ``default_start_time``. An entry whose required duration
    exceeds a single gap is split across consecutive gaps. Any remaining time is
    appended after the last anchor.

    The ``work_log_day.entries`` list is replaced in-place with the merged,
    chronologically sorted result.

    Args:
        work_log_day:
            The WorkLogDay to fill. Existing entries are treated as immovable
            anchors whose ``start_time`` and ``end_time`` are already set.
        entries:
            New WorkLogEntry objects to schedule. Each must have a ``duration``
            (in hours). Their ``start_time`` and ``end_time`` fields are ignored
            and will be overwritten.
        default_start_time:
            The earliest time (``HH:MM``) from which scheduling begins.
            Defaults to ``"09:00"``.

    Raises:
        ValueError: If any entry in ``entries`` has no ``duration`` set.
    """
    fmt = "%H:%M"

    def to_dt(t: str) -> datetime.datetime:
        return datetime.datetime.strptime(t, fmt)

    def to_str(dt: datetime.datetime) -> str:
        return dt.strftime(fmt)

    def hours_to_td(h: int | float) -> datetime.timedelta:
        return datetime.timedelta(hours=h)

    # Validate that all new entries carry a duration.
    for entry in entries:
        if entry.duration is None:
            raise ValueError(
                f"Entry '{entry.description}' has no duration set. "
                "All entries passed to fill_work_log_day_with_entries must have a duration."
            )

    # Sort existing anchors by start time.
    anchors = sorted(work_log_day.entries, key=lambda e: to_dt(e.start_time))

    # Build a list of free gaps: (gap_start, gap_end) as datetime objects.
    # Gaps are found between default_start_time and the first anchor,
    # between consecutive anchors, and after the last anchor (unbounded → use
    # a sentinel far in the future).
    day_start = to_dt(default_start_time)
    sentinel = datetime.datetime(1900, 1, 1, 23, 59)  # effectively end-of-day

    gap_boundaries: list[tuple[datetime.datetime, datetime.datetime]] = []
    cursor = day_start
    for anchor in anchors:
        anchor_start = to_dt(anchor.start_time)
        if cursor < anchor_start:
            gap_boundaries.append((cursor, anchor_start))
        cursor = to_dt(anchor.end_time)
    # Gap after the last anchor (or the whole day if there are no anchors).
    gap_boundaries.append((cursor, sentinel))

    # Schedule new entries into the gaps, splitting as needed.
    scheduled: list[WorkLogEntry] = []
    gap_idx = 0
    gap_cursor = gap_boundaries[0][0] if gap_boundaries else day_start

    for entry in entries:
        remaining_hours = entry.duration  # guaranteed non-None

        while remaining_hours > 0:
            # Advance to a gap that still has room.
            while gap_idx < len(gap_boundaries):
                gap_start, gap_end = gap_boundaries[gap_idx]
                if gap_cursor < gap_start:
                    gap_cursor = gap_start
                available = (gap_end - gap_cursor).total_seconds() / 3600
                if available > 0:
                    break
                gap_idx += 1
                if gap_idx < len(gap_boundaries):
                    gap_cursor = gap_boundaries[gap_idx][0]
            else:
                # No more gaps — append remaining time after all anchors.
                slot_start = gap_cursor
                slot_end = gap_cursor + hours_to_td(remaining_hours)
                chunk = copy.copy(entry)
                chunk.start_time = to_str(slot_start)
                chunk.end_time = to_str(slot_end)
                chunk.duration = remaining_hours
                scheduled.append(chunk)
                gap_cursor = slot_end
                remaining_hours = 0
                break

            gap_start, gap_end = gap_boundaries[gap_idx]
            available = (gap_end - gap_cursor).total_seconds() / 3600
            slot_hours = min(remaining_hours, available)
            slot_start = gap_cursor
            slot_end = gap_cursor + hours_to_td(slot_hours)

            chunk = copy.copy(entry)
            chunk.start_time = to_str(slot_start)
            chunk.end_time = to_str(slot_end)
            chunk.duration = slot_hours
            scheduled.append(chunk)

            gap_cursor = slot_end
            remaining_hours -= slot_hours

            # Move to the next gap if the current one is exhausted.
            if gap_cursor >= gap_end and gap_idx + 1 < len(gap_boundaries):
                gap_idx += 1
                gap_cursor = gap_boundaries[gap_idx][0]

    # Merge anchors and scheduled chunks, sort by start time.
    work_log_day.entries = sorted(
        anchors + scheduled,
        key=lambda e: to_dt(e.start_time),
    )
    return


if __name__ == "__main__":
    W = WorkLogEntry
    M = Meeting
    A = AdminTask
    C = Course
    T_OTSNOW = OpsTicketSNOW
    T_ONTMC = OpsNoTicketMultipleCustomers
    T_ONOAOP = OpsNoTicketA1OnPrem

    # work log entries
    wle: list[WorkLogEntry]

    # description string
    desc_gl: str = "GitLab production ready deployment experimentation"
    desc_osc: str = "OpenShift experimental cluster setup and testing"
    desc_wsl: str = "WSL custom kernel patch (security: copy-fail, etc.)"
    desc_km: str = "Kubernetes (Tanzu) monitoring solution evaluation"
    desc_cks: str = (
        "CKS course - Certified Kubernetes Security Specialist course (Linux Foundation)"
    )
    desc_wuejfx: str = "Weekly Unified Enterprise JFX"
    desc_aatc: str = "A&AP Team Call"

    M_WUEJFX = Meeting("10:00", "11:00", desc_wuejfx)
    M_AATC = Meeting("14:00", "14:30", desc_aatc)

    work_log_month_entires: WorkLogMonth = WorkLogMonth(
        month=6, year=2026, daily_entries={}
    )

    formatted_work_log: str = create_work_log_entries(wle)
    # print(formatted_work_log)
    type_text(formatted_work_log, 3, 0.01, 1)
