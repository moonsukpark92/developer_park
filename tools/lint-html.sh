#!/usr/bin/env bash
# lint-html.sh — HTML/CSS 무결성 검사
# 1) CSS 색상값 언더스코어 (#000_000)
# 2) 동일 태그 내 class 속성 중복
# 3) 깨진 한글 인코딩 시그니처 (â€, ï¿½, U+FFFD)
# 4) class 속성값 안에 다른 속성 흡수 (예: class="abc data-label="..." reveal>)
# 5) CSS 선택자 닷(.) 뒤 공백 (예: ". decomp-key")
# 6) (warn) style="" / style="; "
#
# 1~5 위반 시 exit 1, warning은 차단하지 않음.

set -euo pipefail
export LC_ALL=C.UTF-8 2>/dev/null || true

if [ "$#" -eq 0 ]; then
  set -- s1/ s2/ s3/ s4/ index.html
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

# 4. class 속성값 안에 다른 속성이 흡수된 경우 (예: class="abc data-label="...")
#    정상 class 값은 단어/하이픈/콜론/숫자/공백으로만 구성됨. 등호(=)가 들어오면 깨진 것.
TMP_OUT=$(mktemp)
if grep -rEnH --include='*.html' --exclude-dir='.git' 'class="[^"]*[ ][a-z][a-z-]*="' "$@" > "$TMP_OUT" 2>/dev/null; then
  echo ""
  echo "[lint-html] FAIL: class 속성값 안에 다른 속성이 흡수됨 (예: class=\"abc data-label=\"...)"
  cat "$TMP_OUT"
  FAIL=1
fi
rm -f "$TMP_OUT"

# 5. CSS 선택자 닷(.) 뒤 공백 — ". classname" 패턴
#    .html/.css 양쪽 검사. 정규식: 공백/세미콜론/중괄호 다음에 ". 단어"
TMP_OUT=$(mktemp)
if grep -rEnH --include='*.html' --include='*.css' --exclude-dir='.git' '(^|[[:space:];{}>])\.[[:space:]]+[a-zA-Z_][a-zA-Z0-9_-]*' "$@" > "$TMP_OUT" 2>/dev/null; then
  echo ""
  echo "[lint-html] FAIL: CSS 선택자 닷(.) 뒤 공백 (예: '. classname')"
  cat "$TMP_OUT"
  FAIL=1
fi
rm -f "$TMP_OUT"

# 6. warning: 빈 style 속성 (차단하지 않음)
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
