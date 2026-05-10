#!/usr/bin/env bash
# lint-sensitive.sh — 민감정보(직원 실명/이메일/금융/내부 URL) 검출
# 위반 발견 시 exit 1, 통과 시 exit 0.
#
# 사용법:
#   bash tools/lint-sensitive.sh                      # s1/ s2/ s3/ index.html 전체
#   bash tools/lint-sensitive.sh path1 path2 ...      # 명시한 경로만
#
# 박문석(CEO/작가)은 화이트리스트 — 마스킹 제외.

set -euo pipefail
export LC_ALL=C.UTF-8 2>/dev/null || true

# 인자가 없으면 기본 타깃
if [ "$#" -eq 0 ]; then
  set -- s1/ s2/ s3/ index.html
fi

# 검출 대상 직원 명단 (14명, 마스킹되지 않은 형태)
EMPLOYEES="최종현|조은진|임나영|정하윤|한병주|조성범|신다혜|허상민|이상우|서인표|오이벡|김민|박세연|강민구"

# 내부 URL / 시스템 주소
INTERNAL_URLS="j3\.jtranet\.co\.kr|decoceo\.gabia\.io|decopave\.taskworld\.com"

# 이메일 정규식
EMAIL_RE='[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.(co\.kr|com|net|org|io)'

# 이메일 화이트리스트 (시스템/플랫폼)
EMAIL_WHITELIST="noreply@anthropic\.com|noreply@github\.com|info@github\.com|moonsukpark92@gmail\.com"

# 한국 은행명 + 계좌번호 패턴
BANK_RE='(국민|신한|우리|하나|기업|농협|새마을|카카오|외환)\s*[은행]*\s*[0-9]{2,}-[0-9]+'

FAIL=0

echo "[lint-sensitive] 검사 시작: $*"

# 1. 직원 실명 검출
TMP_OUT=$(mktemp)
if grep -rEnH --include='*.html' --include='*.md' --exclude-dir='.git' --exclude-dir='node_modules' "$EMPLOYEES" "$@" > "$TMP_OUT" 2>/dev/null; then
  echo ""
  echo "[lint-sensitive] FAIL: 직원 실명(마스킹되지 않음) 검출"
  cat "$TMP_OUT"
  FAIL=1
fi
rm -f "$TMP_OUT"

# 2. 내부 URL 검출
TMP_OUT=$(mktemp)
if grep -rEnH --include='*.html' --include='*.md' --exclude-dir='.git' --exclude-dir='node_modules' "$INTERNAL_URLS" "$@" > "$TMP_OUT" 2>/dev/null; then
  echo ""
  echo "[lint-sensitive] FAIL: 내부 시스템 URL 검출 (마스킹 필요)"
  cat "$TMP_OUT"
  FAIL=1
fi
rm -f "$TMP_OUT"

# 3. 이메일 검출 (화이트리스트 + 마스킹된 형태 제외)
TMP_OUT=$(mktemp)
grep -rEnH --include='*.html' --include='*.md' --exclude-dir='.git' --exclude-dir='node_modules' "$EMAIL_RE" "$@" 2>/dev/null \
  | grep -vE "$EMAIL_WHITELIST" \
  | grep -v '\*\*\*\*' \
  | grep -v '\*\*\*' \
  > "$TMP_OUT" || true
if [ -s "$TMP_OUT" ]; then
  echo ""
  echo "[lint-sensitive] FAIL: 마스킹되지 않은 이메일 검출"
  cat "$TMP_OUT"
  FAIL=1
fi
rm -f "$TMP_OUT"

# 4. 금융정보 (은행 + 계좌)
TMP_OUT=$(mktemp)
if grep -rEnH --include='*.html' --include='*.md' --exclude-dir='.git' --exclude-dir='node_modules' "$BANK_RE" "$@" > "$TMP_OUT" 2>/dev/null; then
  echo ""
  echo "[lint-sensitive] FAIL: 금융정보(은행 + 계좌번호) 검출"
  cat "$TMP_OUT"
  FAIL=1
fi
rm -f "$TMP_OUT"

if [ $FAIL -eq 0 ]; then
  echo "[lint-sensitive] OK"
fi
exit $FAIL
