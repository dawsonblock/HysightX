"""Per-run operation lock for Hysight HCA storage."""

import threading
from contextlib import contextmanager

# Use RLock to allow reentrant locking in the same thread
_locks: dict = {}
_registry_lock = threading.Lock()


def _get_lock(run_id: str) -> threading.RLock:
    """Get or create an RLock for the given run_id."""
    with _registry_lock:
        if run_id not in _locks:
            _locks[run_id] = threading.RLock()
        return _locks[run_id]


@contextmanager
def run_operation_lock(run_id: str):
    """
    Context manager that serialises concurrent operations on a single run.
    
    This lock is reentrant - the same thread can acquire it multiple times
    without deadlocking.
    
    Usage:
        with run_operation_lock(run_id):
            # Do something with the run
            with run_operation_lock(run_id):  # Safe - reentrant
                # Do nested operation
    """
    lock = _get_lock(run_id)
    lock.acquire()
    try:
        yield
    finally:
        lock.release()
