"""Entry point for the SAP time-tracking automation."""

from sap_timetracking.formatter import create_work_log_entries
from sap_timetracking.models import (
    AdminTask,
    Course,
    Meeting,
    OpsNoTicketA1OnPrem,
    OpsNoTicketMultipleCustomers,
    OpsTicketSNOW,
    WorkLogEntry,
    WorkLogMonth,
)
from sap_timetracking.typer import type_text


def main() -> None:
    # Aliases for convenience
    W = WorkLogEntry
    M = Meeting
    A = AdminTask
    C = Course
    T_OTSNOW = OpsTicketSNOW
    T_ONTMC = OpsNoTicketMultipleCustomers
    T_ONTAOP = OpsNoTicketA1OnPrem

    # work log entries
    wle: list[WorkLogEntry]

    # description strings
    desc_gl: str = "GitLab production ready deployment experimentation"
    desc_osc: str = "OpenShift experimental cluster setup and testing"
    desc_wsl: str = "WSL custom kernel patch (security: copy-fail, etc.)"
    desc_km: str = "Kubernetes (Tanzu) monitoring solution evaluation"
    desc_cks: str = (
        "CKS course - Certified Kubernetes Security Specialist course (Linux Foundation)"
    )
    desc_wuejfx: str = "Weekly Unified Enterprise JFX"
    desc_aatc: str = "A&AP Team Call"

    work_log_month_entries: WorkLogMonth = WorkLogMonth(
        month=6, year=2026, daily_entries={}
    )

    # 01.06.2026 - monday - 8h
    wle = [
        T_ONTAOP(start_time="09:00", end_time="17:00", description=desc_km),
    ]

    # 02.06.2026 - tuesday - 8h
    wle = [
        T_ONTAOP(start_time="09:00", end_time="10:00", description=desc_km),
        M(start_time="10:00", end_time="10:30", description=desc_aatc),
        T_ONTAOP(start_time="10:30", end_time="17:00", description=desc_km),
    ]

    # 03.06.2026 - firday - 9.5h
    wle = [
        T_ONTAOP(start_time="09:00", end_time="18:30", description=desc_km),
    ]

    # 08.06.2026 - monday - 7.5h
    wle = [
        T_ONTAOP(start_time="09:00", end_time="13:30", description=desc_km),
        M(start_time="13:30", end_time="14:30", description="Monitoring concept for Tanzu/K8s - alignment/update"),
        T_ONTAOP(start_time="14:30", end_time="16:30", description=desc_km),
    ]

    # 09.06.2026 - tuesday - 8h
    wle = [
        T_ONTAOP(start_time="09:00", end_time="10:00", description=desc_km),
        M(start_time="10:00", end_time="11:00", description=desc_aatc),
        T_ONTAOP(start_time="11:00", end_time="17:00", description=desc_km),
    ]

    # 11.06.2026 - thursday - 7.5h
    wle = [
        T_ONTAOP(start_time="09:00", end_time="13:30", description=desc_km),
        M(start_time="13:30", end_time="14:00", description=desc_aatc),
        T_ONTAOP(start_time="14:00", end_time="16:30", description=desc_km),
    ]

    # 12.06.2026 - friday - 7.50
    wle = [
        T_ONTAOP(start_time="09:00", end_time="16:30", description=desc_km),
    ]

    # 15.06.2026 - monday - 7.00
    wle = [
        T_ONTAOP(start_time="09:00", end_time="16:00", description=desc_km),
    ]

    # 16.06.2026 - tuesday - 8.00
    wle = [
        T_ONTAOP(start_time="09:00", end_time="10:00", description=desc_km),
        M(start_time="10:00", end_time="10:30", description=desc_aatc),
        T_ONTAOP(start_time="10:30", end_time="17:00", description=desc_km),
    ]

    # 18.06.2026 - thursday - 8.50
    wle = [
        T_ONTAOP(start_time="09:00", end_time="13:30", description=desc_km),
        M(start_time="13:30", end_time="14:00", description=desc_aatc),
        T_ONTAOP(start_time="14:00", end_time="17:30", description=desc_km),
    ]

    # 19.06.2026 - friday - 7.50
    wle = [
        T_ONTAOP(start_time="09:00", end_time="16:30", description=desc_km),
    ]

    # 22.06.2026 - monday - 9.00
    wle = [
        T_ONTAOP(start_time="09:00", end_time="18:00", description=desc_km),
    ]

    # 23.06.2026 - tuesday - 8.00
    wle = [
        M(start_time="09:00", end_time="10:00", description="A1 Live Update | Transforming our ways of working"),
        M(start_time="10:00", end_time="10:30", description=desc_aatc),
        T_ONTAOP(start_time="10:30", end_time="17:00", description=desc_km),
    ]

    # 25.06.2026 - thursday - 8.50
    wle = [
        T_ONTAOP(start_time="09:00", end_time="13:30", description=desc_km),
        M(start_time="13:30", end_time="14:00", description=desc_aatc),
        T_ONTAOP(start_time="14:00", end_time="17:30", description=desc_km),
    ]

    # 26.06.2026 - friday - 8.00
    wle = [
        T_ONTAOP(start_time="09:00", end_time="17:00", description=desc_km),
    ]

    # 29.06.2026 - monday - 8.00
    wle = [
        T_ONTAOP(start_time="09:00", end_time="17:00", description=desc_km),
    ]

    # 30.06.2026 - tuesday - 7.50
    wle = [
        T_ONTAOP(start_time="09:00", end_time="10:00", description=desc_km),
        M(start_time="10:00", end_time="10:30", description=desc_aatc),
        T_ONTAOP(start_time="10:30", end_time="16:30", description=desc_km),
    ]

    formatted_work_log: str = create_work_log_entries(wle)
    # print(formatted_work_log)
    type_text(formatted_work_log, 3, 0.01, 1)


if __name__ == "__main__":
    main()
