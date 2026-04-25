"""hca.storage — public API for all run/event/artifact persistence."""

from .approvals import (
    append_consumption,
    append_denial,
    append_grant,
    append_request,
    get_approval_status,
    get_consumption,
    get_grant,
    get_latest_decision,
    get_pending_requests,
    get_request,
    iter_records,
    resolve_status,
)
from .artifacts import append_artifact, iter_artifacts
from .event_log import append_event, iter_events, read_events
from .locks import run_operation_lock
from .receipts import append_receipt, iter_receipts
from .runs import load_run, save_run
from .snapshots import (
    append_snapshot,
    iter_snapshots,
    load_latest_snapshot,
    load_latest_valid_snapshot,
)

__all__ = [
    "append_artifact",
    "append_consumption",
    "append_denial",
    "append_event",
    "append_grant",
    "append_receipt",
    "append_request",
    "append_snapshot",
    "get_approval_status",
    "get_consumption",
    "get_grant",
    "get_latest_decision",
    "get_pending_requests",
    "get_request",
    "iter_artifacts",
    "iter_events",
    "iter_receipts",
    "iter_records",
    "iter_snapshots",
    "load_latest_snapshot",
    "load_latest_valid_snapshot",
    "load_run",
    "read_events",
    "resolve_status",
    "run_operation_lock",
    "save_run",
]
