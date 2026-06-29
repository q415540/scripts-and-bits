"""Scheduling utilities for filling work log days with duration-based entries."""

import copy
import datetime

from sap_timetracking.models import WorkLogDay, WorkLogEntry, WorkLogMonth


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


def get_work_log_entry_duration(work_log_entry: WorkLogEntry) -> int | float:
    """Calculates the duration of a WorkLogEntry in hours.

    Args:
        work_log_entry:
            A WorkLogEntry object for which to calculate the duration.

    Returns:
        The duration of the work log entry in hours as a float.

    Raises:
        ValueError: If start_time or end_time is missing or not in HH:MM format.
    """
    if isinstance(work_log_entry.duration, (int, float)):
        return work_log_entry.duration

    if not work_log_entry.start_time or not work_log_entry.end_time:
        raise ValueError(
            "Both start_time and end_time must be provided to calculate duration."
        )

    try:
        fmt = "%H:%M"
        start = datetime.datetime.strptime(work_log_entry.start_time, fmt)
        end = datetime.datetime.strptime(work_log_entry.end_time, fmt)
    except ValueError as exc:
        raise ValueError(
            "start_time and end_time must be in 'HH:MM' format."
        ) from exc

    return (end - start).seconds / 3600


def fill_work_log_day_with_entries(
    work_log_day: WorkLogDay,
    entries: list[WorkLogEntry],
    default_start_time: str = "09:00",
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
