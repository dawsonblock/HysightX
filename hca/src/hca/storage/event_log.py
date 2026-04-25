"""
Event log storage for Hysight HCA.
Implements append_event, iter_events, read_events as required by imports and tests.
"""

import json
import uuid
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterator, List, Tuple, Union

from hca.paths import storage_root


def events_file_path(run_id: str) -> Path:
    """Return the path to events.jsonl for the given run_id."""
    return storage_root() / "runs" / run_id / "events.jsonl"


def _serialize_value(obj: Any) -> Any:
    """Serialize a value for JSON, handling enums and datetime."""
    if hasattr(obj, "value"):  # Enum
        return obj.value
    if hasattr(obj, "model_dump"):  # Pydantic v2
        return obj.model_dump(mode="json")
    if hasattr(obj, "dict"):  # Pydantic v1
        return obj.dict()
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, dict):
        return {k: _serialize_value(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_serialize_value(v) for v in obj]
    return obj


def _generate_event_id() -> str:
    """Generate a unique event ID."""
    return str(uuid.uuid4())


def append_event(*args, **kwargs) -> None:
    """
    Append an event to the event log.
    
    Supports both signatures:
    - append_event(context, event_type, source, payload, prior_state=None, next_state=None)
    - append_event(run_id, event_dict)
    """
    # Determine run_id and build event dict based on call signature
    if len(args) >= 4:
        # Expanded signature: (context, event_type, source, payload, ...)
        context = args[0]
        event_type = args[1]
        source = args[2]
        payload = args[3]
        
        # Extract run_id from context
        run_id = getattr(context, "run_id", None)
        if run_id is None and isinstance(context, dict):
            run_id = context.get("run_id")
        if run_id is None:
            raise ValueError("Cannot determine run_id for event logging")
        
        # Build event dict
        timestamp = kwargs.get("timestamp")
        if timestamp is None:
            # Try to get from context
            timestamp = getattr(context, "timestamp", None) or getattr(context, "created_at", None)
        if timestamp is None:
            timestamp = datetime.utcnow().isoformat()
        elif hasattr(timestamp, "isoformat"):
            timestamp = timestamp.isoformat()
        
        event = {
            "event_id": _generate_event_id(),
            "run_id": run_id,
            "event_type": event_type.value if hasattr(event_type, "value") else event_type,
            "timestamp": timestamp,
            "actor": source,
            "source": source,
            "payload": _serialize_value(payload),
        }
        
        # Add prior_state and next_state if provided
        if "prior_state" in kwargs:
            prior = kwargs["prior_state"]
            event["prior_state"] = prior.value if hasattr(prior, "value") else prior
        if "next_state" in kwargs:
            next_s = kwargs["next_state"]
            event["next_state"] = next_s.value if hasattr(next_s, "value") else next_s
            
    elif len(args) == 2:
        # Legacy signature: (run_id, event)
        run_id, event = args
        # Ensure event has required fields
        if not isinstance(event, dict):
            raise TypeError("Event must be a dict")
        event = dict(event)  # Copy to avoid modifying original
        if "event_id" not in event:
            event["event_id"] = _generate_event_id()
        if "run_id" not in event:
            event["run_id"] = run_id
        # Serialize all values
        event = _serialize_value(event)
    else:
        raise TypeError(
            "append_event expects either (run_id, event) or "
            "(context, event_type, source, payload, ...) arguments"
        )
    
    # Write to file
    path = events_file_path(run_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(event, sort_keys=True, separators=(",", ":")) + "\n")
        f.flush()
        os.fsync(f.fileno())


def iter_events(run_id: str) -> Iterator[Dict[str, Any]]:
    """Iterate over events for a run in append order."""
    path = events_file_path(run_id)
    if not path.exists():
        return iter([])
    
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    yield json.loads(line)
                except json.JSONDecodeError:
                    continue  # Skip malformed lines


def read_events(run_id: str, offset: int = 0) -> Tuple[List[Dict[str, Any]], int]:
    """
    Read events for a run, optionally starting from an offset.
    
    Returns:
        Tuple of (events_list, new_offset)
    """
    events = list(iter_events(run_id))
    if offset >= len(events):
        return [], offset
    new_events = events[offset:]
    new_offset = len(events)
    return new_events, new_offset
