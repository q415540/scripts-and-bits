"""Dataclasses representing SAP time-tracking work log entities."""

from dataclasses import dataclass


@dataclass
class WorkLogEntry:
    """Represents a single work log entry with start time, end time, and description.

    Attributes:
        start_time: The start time of the entry in HH:MM format.
        end_time: The end time of the entry in HH:MM format.
        description: A short description of the work performed.
        order_number: The SAP order number associated with this entry.
        order_type: The SAP order type code associated with this entry.
        duration: Optional; the duration of the work log entry in hours. If not
            provided, it can be calculated from start_time and end_time.
    """

    start_time: str
    end_time: str
    description: str
    order_number: str
    order_type: str
    duration: int | float | None = None  # Duration in hours, optional


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
    order_type: str = "HR0016"


@dataclass
class OpsNoTicketMultipleCustomers(WorkLogEntry):
    """Represents an `Operation` -> `No Ticket` -> `Multiple Customers` entry in the work log.

    Attributes:
        order_number: Defaults to the SAP order number for RT_SHARED_0000 no-ticket ops.
        order_type: Defaults to the SAP order type for A1 Managed DC no-ticket ops.
    """

    order_number: str = "900000009964"  # RT_SHARED_0000
    order_type: str = "HR0323"  # A1 Managed DC
    # TODO: create different entries for multiple order types
    # order_type: str = "HR0291"  # Application Services


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
        entries: The list of work log entries for this day.
        weekday: The name of the weekday (e.g. 'Monday'), or None if not set.
    """

    entries: list[WorkLogEntry]
    weekday: str | None = None


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
