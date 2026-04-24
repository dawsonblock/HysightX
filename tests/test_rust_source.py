"""
Source-level regression test: assert MemoryRecord in the Rust sidecar
does not have duplicate struct fields (compile blocker).
"""
import pathlib
import re


MAIN_RS = pathlib.Path(__file__).parents[1] / "memvid_service" / "src" / "main.rs"


def _extract_struct_block(source: str, struct_name: str) -> str:
    """Return the body of the named struct, or empty string if not found."""
    pattern = rf"struct\s+{re.escape(struct_name)}\s*\{{([^}}]*)\}}"
    m = re.search(pattern, source, re.DOTALL)
    return m.group(1) if m else ""


def test_memory_record_no_duplicate_fields():
    assert MAIN_RS.exists(), f"Rust source not found: {MAIN_RS}"
    source = MAIN_RS.read_text(encoding="utf-8")
    body = _extract_struct_block(source, "MemoryRecord")
    assert body, "MemoryRecord struct not found in main.rs"

    field_names = re.findall(r"^\s+(\w+)\s*:", body, re.MULTILINE)
    seen = set()
    duplicates = []
    for name in field_names:
        if name in seen:
            duplicates.append(name)
        seen.add(name)

    assert not duplicates, (
        f"MemoryRecord has duplicate fields: {duplicates}. "
        "Remove the duplicates to fix the compile blocker."
    )
