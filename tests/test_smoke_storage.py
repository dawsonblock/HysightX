"""
Smoke tests that verify the hca.storage and backend import contracts
are intact after the Phase 1 repairs.
"""
import importlib
import os
import sys
import tempfile
import pathlib
import pytest

HCA_SRC = pathlib.Path(__file__).parents[1] / "hca" / "src"
sys.path.insert(0, str(HCA_SRC))


@pytest.fixture()
def storage_root(tmp_path, monkeypatch):
    monkeypatch.setenv("HCA_STORAGE_ROOT", str(tmp_path))
    return tmp_path


def test_hca_storage_imports():
    import hca.storage as s
    for name in [
        "load_run", "save_run", "append_event", "iter_events", "run_operation_lock",
        "append_grant", "append_denial", "append_consumption", "append_request",
        "append_snapshot", "iter_artifacts", "iter_receipts", "load_latest_valid_snapshot",
    ]:
        assert hasattr(s, name), f"hca.storage missing: {name}"


def test_run_operation_lock_is_context_manager():
    import hca.storage as s
    with s.run_operation_lock("smoke-run-001"):
        pass


def test_run_operation_lock_is_reentrant():
    import hca.storage as s
    with s.run_operation_lock("reentrant-run"):
        with s.run_operation_lock("reentrant-run"):
            pass


def test_save_and_load_run(storage_root):
    import hca.storage as s
    from hca.paths import run_storage_dir
    run_id = "smoke-test-run-001"
    payload = {"run_id": run_id, "state": "completed", "goal": "test"}
    s.save_run(run_id, payload)
    loaded = s.load_run(run_id)
    assert loaded.run_id == run_id
    assert loaded.state == "completed"


def test_append_and_iter_events():
    import hca.storage as s
    run_id = "smoke-event-run-001"
    s.append_event(run_id, {"event_type": "test_event", "payload": "hello"})
    events = list(s.iter_events(run_id))
    assert any(e.get("event_type") == "test_event" for e in events)


def test_append_grant_denial_consumption():
    import hca.storage as s
    run_id = "smoke-approval-run-001"
    s.append_grant(run_id, {"approval_id": "a1", "token": "tok"})
    s.append_denial(run_id, "a2", reason="policy")
    s.append_consumption(run_id, {"approval_id": "a1"})


def test_backend_server_imports():
    backend_src = pathlib.Path(__file__).parents[1] / "backend"
    sys.path.insert(0, str(backend_src.parent))
    try:
        from backend.server import create_app
        app = create_app()
        assert app is not None
    finally:
        sys.path.pop(0)
