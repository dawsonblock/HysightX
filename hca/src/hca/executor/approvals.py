"""Centralized approval validation for execution."""

from datetime import datetime
from typing import Any, Dict, Optional

from hca.common.types import ActionCandidate
from hca.common.time import utc_now
from hca.storage.approvals import (
    get_consumption,
    get_grant,
    get_request,
    resolve_status,
)


def require_approval(action_class: str) -> bool:
    """Determine if an action class requires approval."""
    return action_class in {"medium", "high"}


def _bindings_match(binding1: Any, binding2: Any) -> bool:
    """Compare two bindings, handling both dict and object types."""
    if binding1 is None or binding2 is None:
        return binding1 == binding2
    
    # If both have .matches() method (Pydantic models)
    if hasattr(binding1, "matches") and hasattr(binding2, "action_fingerprint"):
        return binding1.matches(binding2)
    
    # Compare fingerprints
    fp1 = binding1.get("action_fingerprint") if isinstance(binding1, dict) else getattr(binding1, "action_fingerprint", None)
    fp2 = binding2.get("action_fingerprint") if isinstance(binding2, dict) else getattr(binding2, "action_fingerprint", None)
    
    if fp1 and fp2:
        return fp1 == fp2
    
    # Fallback: compare as dicts if both are dicts
    if isinstance(binding1, dict) and isinstance(binding2, dict):
        return binding1 == binding2
    
    return False


def _candidate_matches_request(
    candidate: ActionCandidate,
    request: Any,
) -> bool:
    # Handle both dict and object access
    if isinstance(request, dict):
        request_binding = request.get("binding")
        request_action_id = request.get("action_id")
    else:
        request_binding = getattr(request, "binding", None)
        request_action_id = getattr(request, "action_id", None)
    
    candidate_binding = candidate.binding

    if request_binding is not None and candidate_binding is not None:
        # Handle binding comparison - binding could be dict or object
        if hasattr(request_binding, "matches"):
            return request_binding.matches(candidate_binding)
        # If binding is a dict, compare fingerprints
        req_fp = request_binding.get("action_fingerprint") if isinstance(request_binding, dict) else None
        cand_fp = getattr(candidate_binding, "action_fingerprint", None)
        if req_fp and cand_fp:
            return req_fp == cand_fp
        return False

    if request_binding is not None and candidate_binding is None:
        return False

    return request_action_id == candidate.action_id


def validate_resume_approval(
    run_id: str,
    approval_id: str,
    token: str,
    now: Optional[datetime] = None,
    candidate: Optional[ActionCandidate] = None,
) -> Dict[str, Any]:
    """Validate if an approval is valid for resumption."""
    now = now or utc_now()
    resolved_status = resolve_status(run_id, approval_id, now)

    result = {
        "ok": False,
        "reason": None,
        "resolved_status": resolved_status,
        "status": resolved_status,
    }

    if resolved_status == "missing":
        result["reason"] = "missing_approval"
    elif resolved_status == "denied":
        result["reason"] = "denied_approval"
    elif resolved_status == "expired":
        result["reason"] = "expired_approval"
    elif resolved_status == "consumed":
        result["reason"] = "already_consumed"
    elif resolved_status == "pending":
        result["reason"] = "pending_approval"
    elif resolved_status == "granted":
        request = get_request(run_id, approval_id)
        grant = get_grant(run_id, approval_id)
        if not request:
            result["reason"] = "request_record_missing"
        elif not grant:
            result["reason"] = "grant_record_missing"
        elif (
            # Handle both dict and object access for binding comparison
            (grant.get("binding") if isinstance(grant, dict) else getattr(grant, "binding", None)) is not None
            and (request.get("binding") if isinstance(request, dict) else getattr(request, "binding", None)) is not None
            and not _bindings_match(
                grant.get("binding") if isinstance(grant, dict) else getattr(grant, "binding", None),
                request.get("binding") if isinstance(request, dict) else getattr(request, "binding", None),
            )
        ):
            result["reason"] = "approval_binding_corrupted"
        elif get_consumption(run_id, approval_id, token=token):
            result["reason"] = "already_consumed"
        elif (grant.get("token") if isinstance(grant, dict) else getattr(grant, "token", None)) != token:
            result["reason"] = "token_mismatch"
        elif candidate is not None and not _candidate_matches_request(
            candidate,
            request,
        ):
            result["reason"] = "approved_action_mismatch"
        else:
            result["ok"] = True

    return result
