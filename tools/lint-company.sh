#!/usr/bin/env bash
# lint-company.sh — 회사명 정규화 / ㈜ 인코딩 오류 검출
# 정상: '데코페이브㈜' 또는 '데코페이브 ㈜' 또는 '&#x321C;'
# 잘못: '데코페이브 주식회사', '데코페이브(주)', '&#x338E;'(㎎), '&#xAC8C;'(게)
#
# 위반 시 exit 1.

set -euo pipefail
export LC_ALL=C.UTF-8 2>/dev/null || true

if [ "$#" -eq 0 ]; then
  set -- s1/ s2/ s3/ s4/ index.html
fi

# ㈜로 사용되어서는 안 되는 인코딩
BAD_HEX_ENTITIES="&#x338E;|&#xAC8C;"

# 회사명 변종
COMPANY_VARIANTS="데코페이브 주식회사|데코페이브\(주\)"

# 회사명 인근 깨진 인코딩 시그니처
BROKEN_NEAR_COMPANY="데코페이브.{0,5}(â€|ï¿½|�)"

FAIL=0

echo "[lint-company] 검사 시작: $*"

# 1. 잘못된 HTML 엔티티 (㎎, 게 등을 ㈜ 대신 사용)
TMP_OUT=$(mktemp)
if grep -rEnH --include='*.html' --include='*.md' --exclude-dir='.git' "$BAD_HEX_ENTITIES" "$@" > "$TMP_OUT" 2>/dev/null; then
  echo ""
  echo "[lint-company] FAIL: ㈜ 자리에 잘못된 HTML 엔티티 사용"
  echo "  &#x338E;는 '㎎'(밀리그램), &#xAC8C;는 '게'입니다."
  echo "  올바른 표기: ㈜ 또는 &#x321C;"
  cat "$TMP_OUT"
  FAIL=1
fi
rm -f "$TMP_OUT"

# 2. 회사명 변종
TMP_OUT=$(mktemp)
if grep -rEnH --include='*.html' --include='*.md' --exclude-dir='.git' "$COMPANY_VARIANTS" "$@" > "$TMP_OUT" 2>/dev/null; then
  echo ""
  echo "[lint-company] FAIL: 회사명 변종 발견"
  echo "  '데코페이브㈜' 또는 '(주)데코페이브'로 통일하세요."
  cat "$TMP_OUT"
  FAIL=1
fi
rm -f "$TMP_OUT"

# 3. 회사명 인근 깨진 인코딩
TMP_OUT=$(mktemp)
if grep -rEPnH --include='*.html' --include='*.md' --exclude-dir='.git' "$BROKEN_NEAR_COMPANY" "$@" > "$TMP_OUT" 2>/dev/null; then
  echo ""
  echo "[lint-company] FAIL: 회사명 인근 깨진 인코딩(â€/ï¿½/U+FFFD) 발견"
  cat "$TMP_OUT"
  FAIL=1
fi
rm -f "$TMP_OUT"

if [ $FAIL -eq 0 ]; then
  echo "[lint-company] OK"
fi
exit $FAIL
