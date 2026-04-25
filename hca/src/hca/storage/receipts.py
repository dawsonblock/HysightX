"""
Receipt storage for Hysight HCA.
Implements append_receipt, iter_receipts as required by imports and tests.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, Iterator

from hca.paths import storage_root


def _receipts_file_path(run_id: str) -> Path:
    """Return the path to receipts.jsonl for the given run_id."""
    return storage_root() / "runs" / run_id / "receipts.jsonl"


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


def append_receipt(run_id: str, receipt: Dict[str, Any]) -> None:
    """Persist a receipt to the receipts log."""
    path = _receipts_file_path(run_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    serialized = _serialize_value(receipt)
    
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(serialized, sort_keys=True, separators=(",", ":")) + "\n")
        f.flush()
        os.fsync(f.fileno())


def iter_receipts(run_id: str) -> Iterator[Dict[str, Any]]:
    """Iterate over all receipts for a run in order."""
    path = _receipts_file_path(run_id)
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
