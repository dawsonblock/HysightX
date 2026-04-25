"""
Run metadata persistence for Hysight HCA.
Implements load_run, save_run as required by imports and tests.
"""

import json
import uuid
import tempfile
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Union

from hca.paths import run_storage_dir
from hca.common.types import RunContext
from hca.common.enums import RuntimeState


def run_path(run_id: str) -> Path:
    """Return the path to run.json for the given run_id."""
    return run_storage_dir(run_id) / "run.json"


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


def _serialize_for_storage(obj: Any) -> Dict[str, Any]:
    """Convert an object to a JSON-serializable dict."""
    if hasattr(obj, "model_dump"):
        return obj.model_dump(mode="json")
    if hasattr(obj, "dict"):
        return obj.dict()
    if isinstance(obj, dict):
        return obj
    return vars(obj)


def load_run(run_id: str) -> Union[RunContext, None]:
    """
    Load a run from storage and return as a RunContext model.
    
    Returns None if the run doesn't exist.
    """
    path = run_path(run_id)
    if not path.exists():
        return None
    
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Ensure run_id is set
    data["run_id"] = run_id
    
    # Convert state string to RuntimeState enum if needed
    if "state" in data and isinstance(data["state"], str):
        try:
            data["state"] = RuntimeState(data["state"])
        except ValueError:
            pass  # Keep as string if not a valid enum value
    
    return RunContext.model_validate(data)


def save_run(*args, **kwargs) -> None:
    """
    Persist run data to storage.
    
    Supports both signatures:
    - save_run(context) - where context has run_id attribute
    - save_run(run_id, payload) - direct save
    """
    if len(args) == 1:
        # Called as save_run(context)
        context = args[0]
        run_id = getattr(context, "run_id", None)
        if run_id is None:
            raise ValueError("Context object must have a run_id attribute")
        data = _serialize_for_storage(context)
    elif len(args) == 2:
        run_id, data = args
        data = _serialize_for_storage(data)
    else:
        raise TypeError("save_run expects (run_id, data) or (context)")
    
    path = run_path(run_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    # Serialize all values
    serialized = _serialize_value(data)
    serialized["run_id"] = run_id
    
    # Atomic write: write to temp file, then rename
    temp_path = path.with_suffix(f".tmp.{uuid.uuid4().hex}")
    try:
        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(serialized, f, sort_keys=True, separators=(",", ":"))
            f.flush()
            os.fsync(f.fileno())
        os.rename(temp_path, path)
    except Exception:
        # Clean up temp file on failure
        if temp_path.exists():
            temp_path.unlink()
        raise
