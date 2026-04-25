#!/usr/bin/env bash
# run_dev.sh — Start backend + frontend dev servers for HysightX.
#
# Usage:
#   ./run_dev.sh            # start both
#   ./run_dev.sh backend    # backend only
#   ./run_dev.sh frontend   # frontend only
#
# Both servers write logs to logs/backend.log and logs/frontend.log.
# Run 'kill $(cat logs/backend.pid) $(cat logs/frontend.pid)' to stop.

set -euo pipefail
REPO="$(cd "$(dirname "$0")" && pwd)"
LOGS="$REPO/logs"
mkdir -p "$LOGS"

# Load .env if present
if [ -f "$REPO/.env" ]; then
  set -o allexport
  # shellcheck disable=SC1091
  source "$REPO/.env"
  set +o allexport
fi

HCA_STORAGE_ROOT="${HCA_STORAGE_ROOT:-$REPO/storage}"
MEMORY_STORAGE_DIR="${MEMORY_STORAGE_DIR:-$HCA_STORAGE_ROOT/memory}"
mkdir -p "$HCA_STORAGE_ROOT" "$MEMORY_STORAGE_DIR"

export HCA_STORAGE_ROOT MEMORY_STORAGE_DIR

MODE="${1:-both}"

start_backend() {
  echo "▶ Starting backend on :${BACKEND_PORT:-8000} …"
  cd "$REPO"
  HCA_STORAGE_ROOT="$HCA_STORAGE_ROOT" \
  MEMORY_STORAGE_DIR="$MEMORY_STORAGE_DIR" \
  python3 -m uvicorn backend.server:app \
    --host 0.0.0.0 \
    --port "${BACKEND_PORT:-8000}" \
    --reload \
    >> "$LOGS/backend.log" 2>&1 &
  echo $! > "$LOGS/backend.pid"
  echo "  Backend PID $(cat "$LOGS/backend.pid") — logs at logs/backend.log"
}

start_frontend() {
  echo "▶ Starting frontend on :${FRONTEND_PORT:-3000} …"
  cd "$REPO/frontend"
  yarn dev >> "$LOGS/frontend.log" 2>&1 &
  echo $! > "$LOGS/frontend.pid"
  echo "  Frontend PID $(cat "$LOGS/frontend.pid") — logs at logs/frontend.log"
}

case "$MODE" in
  backend)  start_backend ;;
  frontend) start_frontend ;;
  *)        start_backend; sleep 2; start_frontend ;;
esac

echo ""
echo "Stack ready:"
echo "  Backend  → http://localhost:${BACKEND_PORT:-8000}/api/hca/runs"
echo "  Frontend → http://localhost:${FRONTEND_PORT:-3000}"
echo ""
echo "Stop with:  kill \$(cat logs/backend.pid logs/frontend.pid 2>/dev/null)"
