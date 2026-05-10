#!/usr/bin/env bash
# lint-html.sh — HTML/CSS 무결성 검사
# 1) CSS 색상값 언더스코어 (#000_000)
# 2) 동일 태그 내 class 속성 중복
# 3) 깨진 한글 인코딩 시그니처 (â€, ï¿½, U+FFFD)
# 4) (warn) style="" / style="; "
#
# 1~3 위반 시 exit 1, warning은 차단하지 않음.

set -euo pipefail
export LC_ALL=C.UTF-8 2>/dev/null || true

if [ "$#" -eq 0 ]; then
  set -- s1/ s2/ s3/ index.html
fi

FAIL=0

echo "[lint-html] 검사 시작: $*"

# 1. CSS 색상값 언더스코어 (#aabbcc_xx)
TMP_OUT=$(mktemp)
if grep -rEnH --include='*.html' --include='*.css' --exclude-dir='.git' '#[0-9a-fA-F]+_[0-9a-fA-F]*' "$@" > "$TMP_OUT" 2>/dev/null; then
  echo ""
  echo "[lint-html] FAIL: CSS 색상값에 언더스코어(_) 사용 금지"
  cat "$TMP_OUT"
  FAIL=1
fi
rm -f "$TMP_OUT"

# 2. class 속성 중복 (한 태그 내) — 한 줄 단위 검사 (대부분의 태그는 한 줄)
TMP_OUT=$(mktemp)
if grep -rEnH --include='*.html' --exclude-dir='.git' '<[^>]*[[:space:]]class="[^"]*"[^>]*[[:space:]]class="' "$@" > "$TMP_OUT" 2>/dev/null; then
  echo ""
  echo "[lint-html] FAIL: 동일 태그 내 class 속성 중복 선언"
  cat "$TMP_OUT"
  FAIL=1
fi
rm -f "$TMP_OUT"

# 3. 깨진 한글 인코딩 시그니처
TMP_OUT=$(mktemp)
if grep -rEnH --include='*.html' --include='*.md' --exclude-dir='.git' '(â€|ï¿½|�)' "$@" > "$TMP_OUT" 2>/dev/null; then
  echo ""
  echo "[lint-html] FAIL: UTF-8 인코딩 오류 흔적(â€/ï¿½/U+FFFD)"
  cat "$TMP_OUT"
  FAIL=1
fi
rm -f "$TMP_OUT"

# 4. warning: 빈 style 속성 (차단하지 않음)
TMP_OUT=$(mktemp)
grep -rEnH --include='*.html' --exclude-dir='.git' 'style="[[:space:]]*;?[[:space:]]*"' "$@" 2>/dev/null > "$TMP_OUT" || true
if [ -s "$TMP_OUT" ]; then
  echo ""
  echo "[lint-html WARN] 빈 style 속성 발견 (차단하지 않음)"
  sed 's/^/  /' "$TMP_OUT"
fi
rm -f "$TMP_OUT"

if [ $FAIL -eq 0 ]; then
  echo "[lint-html] OK"
fi
exit $FAIL
