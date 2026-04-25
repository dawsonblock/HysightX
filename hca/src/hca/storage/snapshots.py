"""
Snapshot storage for Hysight HCA.
Implements append_snapshot, iter_snapshots, load_latest_snapshot, load_latest_valid_snapshot.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, Iterator, Optional

from hca.paths import storage_root


def _snapshots_file_path(run_id: str) -> Path:
    """Return the path to snapshots.jsonl for the given run_id."""
    return storage_root() / "runs" / run_id / "snapshots.jsonl"


def _serialize_value(obj: Any) -> Any:
    """Serialize a value for JSON, handling enums and datetime."""
    if hasattr(obj, "value"):  # Enum
        return obj.value
    if hasattr(obj, "model_dump"):  # Pydantic v2
        return obj.model_dump(mode="json")
    if hasattr(obj, "dict"):  # Pydantic v1
        return obj.dict()
    if isinstance(obj, dict):
        return {k: _serialize_value(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_serialize_value(v) for v in obj]
    return obj


def append_snapshot(run_id: str, snapshot: Dict[str, Any]) -> None:
    """Persist a snapshot to the snapshots log."""
    path = _snapshots_file_path(run_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    serialized = _serialize_value(snapshot)
    serialized["run_id"] = run_id
    
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(serialized, sort_keys=True, separators=(",", ":")) + "\n")
        f.flush()
        os.fsync(f.fileno())


def iter_snapshots(run_id: str) -> Iterator[Dict[str, Any]]:
    """Iterate over all snapshots for a run in order."""
    path = _snapshots_file_path(run_id)
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


def load_latest_snapshot(run_id: str) -> Optional[Dict[str, Any]]:
    """
    Load the latest snapshot for a run.
    
    Returns None if no snapshots exist.
    """
    latest = None
    for snapshot in iter_snapshots(run_id):
        latest = snapshot
    return latest


def load_latest_valid_snapshot(run_id: str) -> Optional[Dict[str, Any]]:
    """
    Load the latest valid (parseable) snapshot for a run.
    
    Skips malformed snapshots. Returns None if no valid snapshots exist.
    """
    path = _snapshots_file_path(run_id)
    if not path.exists():
        return None
    
    # Read all lines and find the last valid one
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except (IOError, OSError):
        return None
    
    # Iterate in reverse to find the last valid snapshot
    for line in reversed(lines):
        line = line.strip()
        if not line:
            continue
        try:
            return json.loads(line)
        except json.JSONDecodeError:
            continue  # Skip malformed snapshots
    
    return None
