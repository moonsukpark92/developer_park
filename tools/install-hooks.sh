#!/usr/bin/env bash
# install-hooks.sh — pre-push hook 설치 도우미
# 다른 PC / 새 클론에서 한 번 실행하면 동일한 안전망이 복원된다.
#
# 사용법:
#   bash tools/install-hooks.sh

set -euo pipefail
export LC_ALL=C.UTF-8 2>/dev/null || true

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
HOOK_DIR="$REPO_ROOT/.git/hooks"
HOOK_PATH="$HOOK_DIR/pre-push"

if [ ! -d "$HOOK_DIR" ]; then
  echo "[install-hooks] 오류: $HOOK_DIR 가 없습니다. 이 디렉토리는 git 저장소가 아닙니다." >&2
  exit 1
fi

cat > "$HOOK_PATH" <<'EOF'
#!/usr/bin/env bash
# 자동 생성된 pre-push hook (tools/install-hooks.sh).
# 직접 수정하지 말 것. 패턴 변경은 tools/lint-*.sh 수정 후 install-hooks.sh 재실행.
set -e
REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "$REPO_ROOT"
echo "[pre-push] running tools/run-all-lints.sh ..."
bash tools/run-all-lints.sh
EOF

chmod +x "$HOOK_PATH"

echo "[install-hooks] pre-push hook 설치 완료: $HOOK_PATH"
echo "[install-hooks] 우회가 필요한 비상 시: git push --no-verify (권장하지 않음)"
echo ""
echo "[install-hooks] 즉시 검증 실행..."
bash "$SCRIPT_DIR/run-all-lints.sh"
