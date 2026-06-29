"""Utilities for formatting work log entries into SAP-compatible input strings."""

from sap_timetracking.models import WorkLogEntry


def create_work_log_entries(work_log_entries: list[WorkLogEntry]) -> str:
    """Creates a formatted string for work log entries.

    The resulting string encodes SAP field navigation via ``{tab}`` tokens and
    inserts ``{pause}`` markers where a UI reaction must be awaited. It is
    intended to be passed directly to ``type_text()``.

    Args:
        work_log_entries:
            A list of WorkLogEntry objects representing individual work log entries.

    Returns:
        A formatted string containing all work log entries joined by ``{tab}{tab}``.
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
