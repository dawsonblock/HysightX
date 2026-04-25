"""
Approval storage for Hysight HCA.
Implements approval request/grant/denial/consumption persistence.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional, Union

from hca.paths import storage_root


def _approvals_file_path(run_id: str) -> Path:
    """Return the path to approvals.jsonl for the given run_id."""
    return storage_root() / "runs" / run_id / "approvals.jsonl"


def _serialize_value(obj: Any) -> Any:
    """Serialize a value for JSON, handling enums and datetime."""
    if hasattr(obj, "value"):  # Enum
        return obj.value
    if hasattr(obj, "model_dump"):  # Pydantic v2
        return obj.model_dump(mode="json")
    if hasattr(obj, "dict"):  # Pydantic v1
        return obj.dict()
    if hasattr(obj, "_asdict"):  # NamedTuple
        return obj._asdict()
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, dict):
        return {k: _serialize_value(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_serialize_value(v) for v in obj]
    return obj


def _to_dict(obj: Any) -> Dict[str, Any]:
    """Convert an object to a dict for storage."""
    if isinstance(obj, dict):
        return obj
    if hasattr(obj, "model_dump"):
        return obj.model_dump(mode="json")
    if hasattr(obj, "dict"):
        return obj.dict()
    if hasattr(obj, "_asdict"):
        return obj._asdict()
    return vars(obj)


def _write_record(run_id: str, data: Dict[str, Any]) -> None:
    """Write a record to the approvals log."""
    path = _approvals_file_path(run_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    serialized = _serialize_value(data)
    
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(serialized, sort_keys=True, separators=(",", ":")) + "\n")
        f.flush()
        os.fsync(f.fileno())


def iter_records(run_id: str) -> Iterator[Dict[str, Any]]:
    """Iterate over all approval records for a run."""
    path = _approvals_file_path(run_id)
    if not path.exists():
        return iter([])
    
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    yield json.loads(line)
                except json.JSONDecodeError:
                    continue


def get_pending_requests(run_id: str) -> List[Dict[str, Any]]:
    """
    Return all pending approval requests for a run.
    
    A request is pending if no grant, denial, or consumption record exists for it.
    """
    # Collect all requests
    requests_by_id: Dict[str, Dict[str, Any]] = {}
    decisions_by_id: Dict[str, str] = {}
    
    for record in iter_records(run_id):
        approval_id = record.get("approval_id")
        if not isinstance(approval_id, str):
            continue
        
        record_type = record.get("record_type", "")
        
        if record_type == "request":
            requests_by_id[approval_id] = record
        elif record_type in ("grant", "denial", "consumption"):
            decisions_by_id[approval_id] = record_type
    
    # Return requests that haven't been decided
    pending = []
    for approval_id, request in requests_by_id.items():
        if approval_id not in decisions_by_id:
            pending.append(request)
    
    return pending


def get_request(run_id: str, approval_id: str) -> Optional[Dict[str, Any]]:
    """Return the latest approval request for a given run and approval_id."""
    latest = None
    for record in iter_records(run_id):
        if record.get("approval_id") == approval_id and record.get("record_type") == "request":
            latest = record
    return latest


def get_latest_decision(run_id: str, approval_id: str) -> Optional[Dict[str, Any]]:
    """Return the latest decision (grant or denial) for an approval."""
    latest = None
    for record in iter_records(run_id):
        if record.get("approval_id") == approval_id:
            record_type = record.get("record_type", "")
            # Only grant and denial are decisions - consumption is a separate lifecycle event
            if record_type in ("grant", "denial"):
                latest = record
    return latest


def get_grant(run_id: str, approval_id: str) -> Optional[Dict[str, Any]]:
    """Return the grant record for an approval, if any."""
    for record in iter_records(run_id):
        if record.get("approval_id") == approval_id and record.get("record_type") == "grant":
            return record
    return None


def get_consumption(run_id: str, approval_id: str, token: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Return the consumption record for an approval, optionally filtered by token."""
    for record in iter_records(run_id):
        if record.get("approval_id") == approval_id and record.get("record_type") == "consumption":
            if token is None or record.get("token") == token:
                return record
    return None


def get_approval_status(run_id: str, approval_id: str) -> Dict[str, Any]:
    """
    Return the current status for a given approval_id.
    
    Returns a dict with status info including:
    - approval_id
    - status: "pending", "granted", "denied", "consumed"
    """
    status = "pending"
    
    for record in iter_records(run_id):
        if record.get("approval_id") == approval_id:
            record_type = record.get("record_type", "")
            if record_type == "grant":
                status = "granted"
            elif record_type == "denial":
                status = "denied"
                break  # Denial is final
            elif record_type == "consumption":
                status = "consumed"
    
    return {
        "approval_id": approval_id,
        "status": status,
    }


def resolve_status(*args, **kwargs) -> str:
    """Alias for get_approval_status that returns just the status string."""
    # Handle different call signatures
    if len(args) >= 2:
        run_id, approval_id = args[0], args[1]
    elif "run_id" in kwargs and "approval_id" in kwargs:
        run_id = kwargs["run_id"]
        approval_id = kwargs["approval_id"]
    else:
        raise TypeError("resolve_status requires run_id and approval_id")
    
    return get_approval_status(run_id, approval_id)["status"]


def append_request(run_id: str, request: Any) -> None:
    """Persist an approval request record."""
    data = _to_dict(request)
    data.setdefault("record_type", "request")
    data.setdefault("approval_id", data.get("approval_id"))
    _write_record(run_id, data)


def append_grant(run_id: str, grant: Any) -> None:
    """Persist an approval grant record."""
    data = _to_dict(grant)
    data.setdefault("record_type", "grant")
    data.setdefault("status", "granted")
    _write_record(run_id, data)


def append_denial(
    run_id: str,
    approval_id_or_record: Union[str, Any],
    reason: Optional[str] = None,
    actor: str = "user"
) -> None:
    """
    Persist an approval denial record.
    
    Supports:
    - append_denial(run_id, approval_id, reason="...", actor="user")
    - append_denial(run_id, record_dict)
    """
    if isinstance(approval_id_or_record, str):
        # Called with approval_id and reason
        data = {
            "record_type": "denial",
            "approval_id": approval_id_or_record,
            "reason": reason or "",
            "actor": actor,
        }
    else:
        # Called with a record object
        data = _to_dict(approval_id_or_record)
        data.setdefault("record_type", "denial")
    
    _write_record(run_id, data)


def append_consumption(run_id: str, consumption: Any) -> None:
    """Persist an approval consumption record."""
    data = _to_dict(consumption)
    data.setdefault("record_type", "consumption")
    data.setdefault("status", "consumed")
    _write_record(run_id, data)
