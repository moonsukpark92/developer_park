#!/usr/bin/env bash
# run-all-lints.sh — 3개 lint 일괄 실행 (CI 대용 / pre-push 진입점)
# 하나라도 실패하면 즉시 중단.

set -e
export LC_ALL=C.UTF-8 2>/dev/null || true

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

echo "==> [run-all-lints] repo: $REPO_ROOT"

bash "$SCRIPT_DIR/lint-sensitive.sh" s1/ s2/ s3/ s4/ index.html
echo ""
bash "$SCRIPT_DIR/lint-company.sh"   s1/ s2/ s3/ s4/ index.html
echo ""
bash "$SCRIPT_DIR/lint-html.sh"      s1/ s2/ s3/ s4/ index.html
echo ""
echo "==> [run-all-lints] all checks passed"
