---
phase: phase-1-quality-automation
phase_number: 1
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - developer_park_repo/tools/lint-sensitive.sh
  - developer_park_repo/tools/lint-company.sh
  - developer_park_repo/tools/lint-html.sh
  - developer_park_repo/tools/install-hooks.sh
  - developer_park_repo/tools/run-all-lints.sh
  - developer_park_repo/.git/hooks/pre-push
  - C:/Users/moons/.claude/projects/c--Users-moons-Downloads------------/memory/project_developer_park.md
  - C:/Users/moons/.claude/projects/c--Users-moons-Downloads------------/memory/project_devpark_pending_fixes.md
  - 개발자 박대표 시리즈/.planning/audits/2026-05-10-full-sweep.md
  - 개발자 박대표 시리즈/.planning/audits/2026-05-10-github-account.md
autonomous: false
estimated_hours: 4-6
requirements: [P0-1, P0-2, P0-3, P0-4, P0-5, P0-6, P0-7]

must_haves:
  truths:
    - "민감정보(직원 실명/이메일/금융/내부 URL)가 포함된 커밋은 git push 시 차단된다"
    - "회사명 변종(데코페이브 주식회사, 데코페이브(주), ㎎ 인코딩 오류 등)이 포함된 파일은 push 전에 감지된다"
    - "CSS 색상 언더스코어(#xxx_xx), class 속성 중복, 깨진 한글 인코딩(â€, ï¿½ 등)이 push 전에 감지된다"
    - "사용자가 새 PC/새 클론에서도 한 줄 명령(install-hooks.sh)으로 동일한 안전망을 복원할 수 있다"
    - "메모리 인덱스(MEMORY.md가 가리키는 두 파일)가 현재 35편 상태와 일치한다"
    - "GitHub 계정에 2FA가 활성화되어 있고 복구코드가 별도 위치에 보관됨이 audit 파일로 증명된다"
    - "35편 전체에 대한 1차 점검 결과가 단일 audit 파일로 존재하며, 발견된 이슈가 카테고리별로 분류되어 있다"
  artifacts:
    - path: "developer_park_repo/tools/lint-sensitive.sh"
      provides: "직원 실명/이메일/금융/내부 URL grep 검출"
      contains: "최종현|조은진|임나영|정하윤|한병주|조성범|신다혜|허상민|이상우|서인표|오이벡|김민|박세연|강민구"
    - path: "developer_park_repo/tools/lint-company.sh"
      provides: "회사명 정규화 검출 (데코페이브㈜ 외 변종)"
      contains: "데코페이브 주식회사|데코페이브\\(주\\)|㎎"
    - path: "developer_park_repo/tools/lint-html.sh"
      provides: "CSS/HTML 무결성 검사"
      contains: "#[0-9a-fA-F]+_|class=\"[^\"]*\".*class=\""
    - path: "developer_park_repo/tools/install-hooks.sh"
      provides: "한 줄 hook 설치 스크립트"
    - path: "developer_park_repo/.git/hooks/pre-push"
      provides: "push 시 3개 lint를 순차 실행하는 git hook"
    - path: "developer_park_repo/tools/run-all-lints.sh"
      provides: "수동 일괄 실행용 진입점 (CI 대용)"
    - path: "개발자 박대표 시리즈/.planning/audits/2026-05-10-full-sweep.md"
      provides: "35편 전수 1차 점검 리포트"
    - path: "개발자 박대표 시리즈/.planning/audits/2026-05-10-github-account.md"
      provides: "GitHub 계정 안전성 점검 기록 (2FA + 복구코드)"
  key_links:
    - from: ".git/hooks/pre-push"
      to: "tools/lint-sensitive.sh, lint-company.sh, lint-html.sh"
      via: "bash script invocation, exit code 1 → push 중단"
      pattern: "tools/lint-.*\\.sh"
    - from: "tools/install-hooks.sh"
      to: ".git/hooks/pre-push"
      via: "cp/symlink + chmod +x"
    - from: "MEMORY.md"
      to: "project_developer_park.md, project_devpark_pending_fixes.md"
      via: "마크다운 링크, 갱신 날짜 일치"
---

<objective>
콘텐츠 자산을 보호하기 위한 자동화 안전망 구축.

**Purpose:** 35편 분량의 정적 HTML 자산이 늘어남에 따라 사람의 검수만으로는 (1) 민감정보 누출, (2) 회사명/특수문자 인코딩 오류, (3) HTML/CSS 렌더링 버그를 잡을 수 없게 되었다. push 단계에서 자동으로 차단하는 grep 기반 안전망을 만들어 "한 번 만들고 영구히 작동"하는 보호막을 둔다.

**Output:**
- 3개 lint 스크립트 + 1개 hook 설치 스크립트 + 1개 일괄 실행기
- pre-push git hook (실제 설치)
- 메모리 갱신 (현재 시리즈 상태 동기화)
- GitHub 계정 안전성 audit
- 35편 전수 점검 audit

**Phase 완료 시 보장되는 것 (goal-backward):**
1. 박대표가 실수로 직원 실명을 포함한 에피소드를 push해도 → 자동 차단
2. ㈜를 ㎎로 잘못 입력해도 → 자동 차단
3. CSS에 `#000_000` 같은 언더스코어 오타를 내도 → 자동 차단
4. PC가 바뀌어도 한 명령(`tools/install-hooks.sh`)으로 보호막 복원
5. 다음 세션이 시작되면 메모리에서 정확한 현재 상태(35편, S3 ep001~ep015 + epilogue2/2_2/interlude/prologue)를 즉시 인지
6. GitHub 계정 탈취 위험이 audit으로 평가됨
7. 현재 35편의 상태(렌더링 버그/맞춤법 잔여) 단일 진실 소스 확보
</objective>

<execution_context>
이 PLAN은 단일 Phase 단일 PLAN으로 운영된다 (이 프로젝트는 정적 블로그라 plan 분할의 이득이 없음).
실행자는 Wave 단위로 task를 진행하며, P0-4는 P0-1/2/3 완료 후, P0-7은 P0-1/2/3 완료 후 실행해야 한다.
</execution_context>

<context>
**프로젝트 규칙 (CLAUDE.md 발췌):**
- 직원 실명: `홍*동` 형태로 마스킹 (중간 글자 `*`)
- 이메일: `m****@*****.co.kr`
- 금융정보, 내부 URL: `**` / `***` 마스킹
- 박문석(CEO): 마스킹 안 함 (예외)
- ㈜는 반드시 `&#x321C;` 또는 `㈜` 사용, `&#x338E;`(㎎) 금지
- CSS 색상값에 언더스코어(_) 금지
- HTML class 중복 선언 금지

**검출 대상 직원 명단 (14명, 마스킹 처리되어야 할 이름):**
최종현, 조은진, 임나영, 정하윤, 한병주, 조성범, 신다혜, 허상민, 이상우, 서인표, 오이벡, 김민, 박세연, 강민구

**환경 제약:**
- Windows 11 + Git Bash (또는 WSL). bash 스크립트는 LF 라인엔딩.
- grep은 Git Bash 기본 grep (GNU grep 호환).
- 한글이 포함된 정규표현식은 UTF-8로 저장.

**기존 자산:**
- `developer_park_repo/tools/` 폴더는 존재하지 않음 (생성 필요).
- `.git/hooks/pre-push`는 미설치 상태 (sample만 존재).
- `.planning/intel/`, `.planning/roadmap/`, `.planning/PROJECT_IDENTITY.md`는 사용자가 언급했으나 실 파일은 아직 부재 → 이 PLAN에서는 ROADMAP P0 항목 7개를 권위 있는 소스로 간주.
</context>

<tasks>

<task type="auto" id="P0-1">
  <name>Task P0-1: 민감정보 grep 스크립트 작성</name>
  <files>developer_park_repo/tools/lint-sensitive.sh</files>
  <action>
    `tools/` 디렉토리를 생성하고 bash 스크립트 `lint-sensitive.sh`를 작성한다.

    **검출 패턴 (3그룹):**

    1. **직원 실명 (14명, 마스킹되지 않은 형태):**
       - 최종현, 조은진, 임나영, 정하윤, 한병주, 조성범, 신다혜, 허상민, 이상우, 서인표, 오이벡, 김민, 박세연, 강민구
       - "박문석"은 화이트리스트 (검출 제외)
       - 마스킹된 형태(`최*현`, `조*진` 등)는 정상이므로 검출하지 않음 → 정확히 두 한글 + 한글 + 한글 (3글자 이름)이 연속으로 나오는 경우만 매칭

    2. **이메일 (마스킹되지 않은 형태):**
       - 정규식: `[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.(co\.kr|com|net|org)`
       - 단, `m****@*****.co.kr` 같은 마스킹 패턴은 통과 (별표가 3개 이상이면 OK)
       - 예외: `noreply@anthropic.com`, `noreply@github.com` 등 잘 알려진 시스템 이메일은 화이트리스트

    3. **내부 URL / 시스템 주소:**
       - `j3.jtranet.co.kr`, `decoceo.gabia.io`, `decopave.taskworld.com` 등 ERP/Taskworld 직접 URL
       - 마스킹된 `***.jtranet.***` 같은 형태는 통과

    4. **금융정보:**
       - 한글 은행명 + 계좌번호 패턴: `(국민|신한|우리|하나|기업|농협|새마을|카카오)\s*\d{3,}-\d+`
       - 금액(천만원 이상의 정확한 숫자) 검출은 false positive가 많아 v1에서는 제외 (수동 검수)

    **스크립트 동작:**
    - 인자가 없으면 `s1/ s2/ s3/ index.html` 전체를 검사
    - 인자가 있으면 그 파일들만 검사
    - 위반 발견 시: 파일경로:줄번호:매칭내용 형태로 출력 후 exit 1
    - 위반 없으면 `[lint-sensitive] OK` 출력 후 exit 0

    **셔뱅 + set:**
    ```bash
    #!/usr/bin/env bash
    set -euo pipefail
    ```

    **구현 힌트:**
    ```bash
    EMPLOYEES="최종현|조은진|임나영|정하윤|한병주|조성범|신다혜|허상민|이상우|서인표|오이벡|김민|박세연|강민구"
    INTERNAL_URLS="j3\.jtranet\.co\.kr|decoceo\.gabia\.io|decopave\.taskworld\.com"
    EMAIL_RE='[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.(co\.kr|com|net|org)'
    EMAIL_WHITELIST="noreply@anthropic\.com|noreply@github\.com"

    FAIL=0
    if grep -rEnH --include='*.html' --include='*.md' "$EMPLOYEES" "$@" 2>/dev/null; then FAIL=1; fi
    if grep -rEnH --include='*.html' --include='*.md' "$INTERNAL_URLS" "$@" 2>/dev/null; then FAIL=1; fi
    # 이메일은 화이트리스트 제외 후 검사
    if grep -rEnH --include='*.html' --include='*.md' "$EMAIL_RE" "$@" 2>/dev/null \
         | grep -vE "$EMAIL_WHITELIST" \
         | grep -v '\*\*\*\*'; then FAIL=1; fi

    [ $FAIL -eq 0 ] && echo "[lint-sensitive] OK"
    exit $FAIL
    ```

    스크립트 작성 후 `chmod +x tools/lint-sensitive.sh` 실행 (Windows에서는 git update-index --chmod=+x로 추가 처리).
  </action>
  <verify>
    <automated>
      cd developer_park_repo && bash tools/lint-sensitive.sh s1/ s2/ s3/ index.html; echo "exit=$?"
      # 현재 콘텐츠는 이미 마스킹 처리된 상태이므로 exit=0이어야 정상.
      # 추가로 임시 파일에 "최종현 프로" 한 줄을 넣고 실행 → exit=1 + 매칭 출력 확인 후 임시 파일 삭제.
    </automated>
  </verify>
  <done>
    - `tools/lint-sensitive.sh` 파일 존재, 실행 권한 부여
    - 35편 전체 검사 시 exit 0 (현재 콘텐츠 통과)
    - 의도적으로 직원 실명을 넣은 임시 파일에 대해 exit 1 + 정확한 줄번호 출력
    - 화이트리스트(박문석, noreply@) 통과 확인
  </done>
</task>

<task type="auto" id="P0-2">
  <name>Task P0-2: 회사명 정규화 grep 스크립트</name>
  <files>developer_park_repo/tools/lint-company.sh</files>
  <action>
    bash 스크립트 `lint-company.sh`를 작성한다.

    **검출 패턴:**

    1. **㈜ 인코딩 오류:**
       - `&#x338E;` (㎎ 문자) → 검출
       - `㎎` (실제 ㎎ 문자, 회사명 옆에 등장하면 의심) → 검출
       - 정상: `㈜` 또는 `&#x321C;`

    2. **회사명 변종 (정규화 위반):**
       - `데코페이브 주식회사` (공식 표기 외) → 검출
       - `데코페이브\(주\)` (괄호 표기) → 검출
       - `Decopave Co\., Ltd\.` 영문 변종 일관성 검사 (warning만)
       - 정상: `데코페이브㈜` 또는 `데코페이브 ㈜`

    3. **회사명 인근 깨진 인코딩:**
       - `데코페이브.{0,5}(â€|ï¿½|�)` 패턴 → 검출

    **동작:**
    - 인자 처리: P0-1과 동일
    - exit code: 위반 시 1, 통과 시 0
    - 출력: `[lint-company] OK` 또는 `[lint-company] FAIL: <매칭 내역>`

    **구현 골자:**
    ```bash
    #!/usr/bin/env bash
    set -euo pipefail

    BAD_ENCODING="&#x338E;"
    COMPANY_VARIANTS="데코페이브 주식회사|데코페이브\(주\)"
    BROKEN_NEAR_COMPANY="데코페이브.{0,5}(â€|ï¿½)"

    FAIL=0
    if grep -rEnH --include='*.html' --include='*.md' "$BAD_ENCODING" "$@" 2>/dev/null; then
      echo "[lint-company] ㈜ 인코딩 오류: &#x338E;는 ㎎(밀리그램)입니다. &#x321C; 또는 ㈜를 사용하세요."
      FAIL=1
    fi
    if grep -rEnH --include='*.html' --include='*.md' "$COMPANY_VARIANTS" "$@" 2>/dev/null; then
      echo "[lint-company] 회사명 변종 발견: '데코페이브㈜'로 통일하세요."
      FAIL=1
    fi
    if grep -rEPnH --include='*.html' --include='*.md' "$BROKEN_NEAR_COMPANY" "$@" 2>/dev/null; then
      echo "[lint-company] 회사명 인근 깨진 인코딩"
      FAIL=1
    fi

    [ $FAIL -eq 0 ] && echo "[lint-company] OK"
    exit $FAIL
    ```

    **주의:** Git Bash의 grep은 `-P`(PCRE)를 지원함. `-E`로 충분히 표현 가능하면 `-E` 우선.
  </action>
  <verify>
    <automated>
      cd developer_park_repo && bash tools/lint-company.sh s1/ s2/ s3/ index.html; echo "exit=$?"
      # 통과해야 함. 임시로 "데코페이브 주식회사" 삽입 후 exit=1 확인.
    </automated>
  </verify>
  <done>
    - 35편 검사 통과 (exit 0)
    - 의도적 변종 삽입 시 exit 1 + 명확한 한국어 메시지 출력
    - `&#x338E;` 패턴 검출 시 사용자에게 어떻게 고칠지 안내
  </done>
</task>

<task type="auto" id="P0-3">
  <name>Task P0-3: HTML/CSS 무결성 grep 스크립트</name>
  <files>developer_park_repo/tools/lint-html.sh</files>
  <action>
    bash 스크립트 `lint-html.sh`를 작성한다.

    **검출 패턴:**

    1. **CSS 색상값 언더스코어:**
       - `#[0-9a-fA-F]+_[0-9a-fA-F]*` (예: `#000_000`, `#ff_aa_bb`)
       - 매칭 시 FAIL

    2. **class 속성 중복 선언:**
       - 한 태그 내 `class="..."`가 두 번 나오는 경우
       - 정규식: `<[^>]*\sclass="[^"]*"[^>]*\sclass="`
       - multiline 매칭 필요 → `grep -P` + `-z` 또는 한 줄 단위로 검사 (HTML이 한 태그 = 한 줄이라는 보장이 없으므로 `-Pz` 사용)

    3. **깨진 한글 인코딩 시그니처:**
       - `â€`, `ï¿½`, `\xc3\xa2` 등 UTF-8 → CP949 → UTF-8 round-trip 실패 흔적
       - 패턴: `(â€|ï¿½|�)`

    4. **닫히지 않은 따옴표 휴리스틱 (warning):**
       - 한 줄에 `"` 개수가 홀수면 의심 (단, 멀티라인 문자열은 false positive 다수 → warning만 출력하고 exit 0)

    5. **인라인 스타일에 빈 값:**
       - `style=""` 또는 `style="; "` → warning

    **동작:**
    - exit 1: 1~3번 위반 시
    - exit 0: 4~5번 warning만 있을 때 (warning은 출력하되 차단하지 않음)
    - 출력: `[lint-html] OK` 또는 `[lint-html] FAIL: ...`

    **구현 골자:**
    ```bash
    #!/usr/bin/env bash
    set -euo pipefail

    FAIL=0
    # 1. CSS 색상 언더스코어
    if grep -rEnH --include='*.html' --include='*.css' '#[0-9a-fA-F]+_[0-9a-fA-F]*' "$@" 2>/dev/null; then
      echo "[lint-html] CSS 색상값에 언더스코어 사용 금지"
      FAIL=1
    fi

    # 2. class 중복 (한 태그 내)
    if grep -rPznH --include='*.html' '<[^>]*\sclass="[^"]*"[^>]*\sclass="' "$@" 2>/dev/null; then
      echo "[lint-html] class 속성이 같은 태그에서 중복 선언됨"
      FAIL=1
    fi

    # 3. 깨진 인코딩
    if grep -rEnH --include='*.html' --include='*.md' '(â€|ï¿½|�)' "$@" 2>/dev/null; then
      echo "[lint-html] UTF-8 인코딩 오류 흔적 발견"
      FAIL=1
    fi

    # 4. warning: 빈 style
    grep -rEnH --include='*.html' 'style="\s*;?\s*"' "$@" 2>/dev/null | sed 's/^/[lint-html WARN] /' || true

    [ $FAIL -eq 0 ] && echo "[lint-html] OK"
    exit $FAIL
    ```

    **검증 시 주의:** 이미 알려진 렌더링 버그 14건이 메모리에 기록되어 있다. 이 스크립트는 그 버그들 중 일부를 실제로 검출해야 한다 (그것이 가치 증명). 검출되지 않으면 패턴을 보강한다.
  </action>
  <verify>
    <automated>
      cd developer_park_repo && bash tools/lint-html.sh s1/ s2/ s3/ index.html; echo "exit=$?"
      # 알려진 버그가 있다면 exit=1로 그것을 잡아야 한다.
      # 만약 현재 통과한다면, 의도적으로 ep001.html에 #aaa_bbb를 삽입 → exit=1 → 원복.
    </automated>
  </verify>
  <done>
    - 스크립트 존재, 실행 가능
    - 의도적 위반(언더스코어, class 중복, â€) 모두 검출
    - 35편 실측 결과가 audit 파일(P0-7)에 반영됨
  </done>
</task>

<task type="auto" id="P0-4-installer">
  <name>Task P0-4a: hook 설치 스크립트 + 일괄 lint 진입점</name>
  <files>
    developer_park_repo/tools/install-hooks.sh,
    developer_park_repo/tools/run-all-lints.sh
  </files>
  <action>
    P0-1/2/3이 완료된 후 실행한다.

    **`tools/run-all-lints.sh`** (단순 wrapper):
    ```bash
    #!/usr/bin/env bash
    set -e
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
    cd "$REPO_ROOT"

    bash "$SCRIPT_DIR/lint-sensitive.sh" s1/ s2/ s3/ index.html
    bash "$SCRIPT_DIR/lint-company.sh"   s1/ s2/ s3/ index.html
    bash "$SCRIPT_DIR/lint-html.sh"      s1/ s2/ s3/ index.html

    echo "[run-all-lints] all checks passed"
    ```

    **`tools/install-hooks.sh`**:
    ```bash
    #!/usr/bin/env bash
    set -euo pipefail
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
    HOOK_PATH="$REPO_ROOT/.git/hooks/pre-push"

    cat > "$HOOK_PATH" <<'EOF'
    #!/usr/bin/env bash
    # 자동 생성된 pre-push hook (tools/install-hooks.sh).
    # 절대 직접 수정하지 말 것. 패턴 변경은 tools/lint-*.sh를 수정 후 install-hooks.sh를 재실행.
    set -e
    REPO_ROOT="$(git rev-parse --show-toplevel)"
    cd "$REPO_ROOT"
    bash tools/run-all-lints.sh
    EOF

    chmod +x "$HOOK_PATH"
    echo "[install-hooks] pre-push hook 설치 완료: $HOOK_PATH"
    echo "[install-hooks] 우회가 필요하면: git push --no-verify (사용 자제)"
    ```

    **why heredoc 안에 또 heredoc 없음:** install-hooks.sh가 `cat > pre-push <<EOF` 한 번만 사용하므로 안전.

    설치 후 즉시 검증을 위해 install-hooks.sh가 마지막에 `bash tools/run-all-lints.sh`를 한 번 호출해 보고하도록 추가하는 것을 권장 (선택).
  </action>
  <verify>
    <automated>
      cd developer_park_repo && bash tools/install-hooks.sh && ls -la .git/hooks/pre-push && bash .git/hooks/pre-push; echo "exit=$?"
    </automated>
  </verify>
  <done>
    - `.git/hooks/pre-push` 파일이 존재하고 실행 권한 보유
    - 파일 내용이 `bash tools/run-all-lints.sh`를 호출
    - run-all-lints가 3개 lint를 순차 실행하고 모두 통과
  </done>
</task>

<task type="auto" id="P0-4-test">
  <name>Task P0-4b: pre-push hook end-to-end 시뮬레이션</name>
  <files>(테스트만 — 파일 변경 없음)</files>
  <action>
    실제 push를 차단하는지 시뮬레이션한다 (실제 remote에는 push하지 않음).

    1. 새 브랜치 생성: `git checkout -b test/lint-hook-sim`
    2. 의도적 위반 커밋:
       - `s1/ep001.html` 끝에 `<!-- 최종현 프로 테스트 -->` 추가
       - `git add` + `git commit -m "test: 의도적 위반"`
    3. `git push origin test/lint-hook-sim --dry-run` 또는 `git push origin test/lint-hook-sim` 시도
    4. **기대:** hook이 lint-sensitive에서 실패 → push 거부 → 빨간 메시지 출력
    5. 커밋 되돌리기: `git reset --hard HEAD~1`
    6. 브랜치 삭제: `git checkout main && git branch -D test/lint-hook-sim`

    절대 push가 실제로 이루어지지 않도록 주의. `--dry-run`이 hook을 트리거하지 않을 수 있으므로 실제 push 시도 후 거부 확인이 가장 신뢰할 수 있음.
  </action>
  <verify>
    <automated>
      # 자동화 어렵 — 다음 명령으로 hook 직접 트리거 시뮬레이션:
      cd developer_park_repo && echo "<!-- 최종현 프로 -->" >> /tmp/sim.html && bash tools/lint-sensitive.sh /tmp/sim.html; echo "exit=$?"
      # exit=1이어야 함. 그 후 rm /tmp/sim.html
    </automated>
  </verify>
  <done>
    - hook이 위반 커밋의 push를 실제로 차단함을 확인
    - 작업 트리/원격이 깨끗한 상태로 복원됨 (테스트 잔여물 없음)
  </done>
</task>

<task type="auto" id="P0-5">
  <name>Task P0-5: 메모리 신선도 갱신</name>
  <files>
    C:/Users/moons/.claude/projects/c--Users-moons-Downloads------------/memory/project_developer_park.md,
    C:/Users/moons/.claude/projects/c--Users-moons-Downloads------------/memory/project_devpark_pending_fixes.md
  </files>
  <action>
    현재 시리즈 실제 상태를 메모리에 반영한다.

    **현재 실측 상태 (2026-05-10 기준, ls 결과):**
    - S1: ep001~ep008 + index.html (8 + 1)
    - S2: ep001~ep007 + epilogue + final + index.html (7 + 2 + 1)
    - S3: ep001~ep015 + epilogue2 + epilogue2_2 + interlude + prologue + index.html (15 + 4 + 1)
    - 총 에피소드 수: 8 + 9 + 19 = 36 (index.html 제외하면 35편)

    **`project_developer_park.md` 갱신 항목:**
    - 마지막 갱신일: 2026-05-10
    - 시즌별 에피소드 수 정확히 기록
    - GitHub Pages URL: https://moonsukpark92.github.io/developer_park/
    - 신규 도구 항목 추가: `tools/lint-sensitive.sh`, `lint-company.sh`, `lint-html.sh`, `install-hooks.sh`, `run-all-lints.sh`
    - pre-push hook 설치 사실 명시

    **`project_devpark_pending_fixes.md` 갱신 항목:**
    - "렌더링 버그 14건 + 맞춤법 6건" 항목 중, P0-7 audit에서 자동 검출된 것은 별도 마킹
    - P0-7 결과를 토대로 자동 검출 가능한 것 / 수동 검수 필요한 것 분리

    P0-7과 동시에 작성하기 어려운 경우 → P0-7 완료 후 메모리 갱신을 마무리한다 (P0-5는 P0-7에 의존).

    **중요:** Read 후 Edit. 직접 Write로 덮어쓰지 말 것 (다른 섹션이 손상될 위험).
  </action>
  <verify>
    <automated>
      grep -c "2026-05-10" "C:/Users/moons/.claude/projects/c--Users-moons-Downloads------------/memory/project_developer_park.md"
      # 1 이상이어야 함
      grep -c "lint-sensitive" "C:/Users/moons/.claude/projects/c--Users-moons-Downloads------------/memory/project_developer_park.md"
      # 1 이상
    </automated>
  </verify>
  <done>
    - 두 메모리 파일에 2026-05-10 갱신 흔적
    - S3 에피소드 수가 실제(15편 + 보조 4편)와 일치
    - tools/ 신규 자산 5개가 메모리에 등재됨
    - MEMORY.md 인덱스에서 두 파일이 가리키는 설명이 현재 상태와 일치
  </done>
</task>

<task type="checkpoint:human-action" id="P0-6" gate="blocking">
  <name>Task P0-6: GitHub 계정 안전성 점검 (사용자 직접 수행)</name>
  <files>개발자 박대표 시리즈/.planning/audits/2026-05-10-github-account.md</files>
  <what-built>
    Claude는 audit 템플릿을 미리 작성해 두고, 사용자가 GitHub 웹에서 직접 확인 후 결과를 채워 넣는다.
    GitHub 2FA 활성화/복구코드 발급은 Claude가 대신 수행할 수 없다 (개인 계정, 2FA 시드 노출 금지).
  </what-built>
  <how-to-verify>
    Claude 사전 작업:
    1. `.planning/audits/2026-05-10-github-account.md` 파일을 다음 템플릿으로 생성:
       ```markdown
       # GitHub 계정 안전성 점검 — 2026-05-10

       대상 계정: moonsukpark92 (https://github.com/moonsukpark92)

       ## 점검 항목

       - [ ] 2FA 활성화 확인 (Settings → Password and authentication)
         - 방식: [ ] TOTP 앱  [ ] SMS  [ ] Security key  [ ] Passkey
       - [ ] 복구코드 발급 및 별도 저장
         - 저장 위치: ____________________ (예: 1Password, 종이, USB)
         - 발급일: 2026-05-10
       - [ ] Authorized OAuth Apps 정리 (사용하지 않는 권한 제거)
       - [ ] Personal Access Token 목록 점검
         - 만료일 없는 token이 있는가? [ ] Yes / [ ] No
         - 조치: ____________________
       - [ ] SSH key 목록 점검
         - 사용하지 않는 key 제거 여부: [ ] 완료 / [ ] 해당 없음
       - [ ] 이메일 주소 백업 확인
         - 주 이메일: moonsukpark92@gmail.com (확인됨)
         - 백업 이메일: ____________________
       - [ ] Sign-in 활동 로그 확인 (최근 14일 의심스러운 로그인 없음)

       ## 발견된 위험

       (있다면 기록)

       ## 조치 결과

       (완료된 항목과 일자)
       ```

    사용자 직접 수행:
    1. https://github.com/settings/security 접속
    2. 위 체크리스트의 각 항목을 직접 확인하고 체크 표시
    3. 복구코드를 별도 위치에 저장 (캡처 금지, 텍스트로)
    4. audit 파일에 결과 기록 후 저장

    완료 신호: audit 파일의 모든 체크박스가 `[x]`로 채워졌고 발견된 위험/조치가 기록됨.
  </how-to-verify>
  <resume-signal>"점검 완료" + audit 파일 경로 회신, 또는 발견된 위험사항 보고</resume-signal>
</task>

<task type="auto" id="P0-7">
  <name>Task P0-7: 35편 전수 1차 점검</name>
  <files>개발자 박대표 시리즈/.planning/audits/2026-05-10-full-sweep.md</files>
  <action>
    P0-1/2/3 lint 스크립트를 35편 전체에 실행하고 결과를 단일 audit 파일로 저장한다.

    **실행 절차:**

    1. `cd developer_park_repo`
    2. 3개 lint를 개별 실행하여 각각의 출력을 캡처:
       ```bash
       bash tools/lint-sensitive.sh s1/ s2/ s3/ index.html > /tmp/lint-sensitive.out 2>&1; echo "exit=$?"
       bash tools/lint-company.sh   s1/ s2/ s3/ index.html > /tmp/lint-company.out   2>&1; echo "exit=$?"
       bash tools/lint-html.sh      s1/ s2/ s3/ index.html > /tmp/lint-html.out      2>&1; echo "exit=$?"
       ```

    3. 추가 수동 점검:
       - 35편 각각의 `<title>` 태그 존재 여부
       - `<meta charset="utf-8">` 또는 동등 표기 존재 여부
       - 상하단 네비게이션 바(시리즈 바 + 에피소드 바) 존재 여부 — 정규식: `s1/index|s2/index|s3/index`
       - 각 시즌 index.html이 모든 에피소드를 링크하는지 (S3는 ep001~ep015 + 보조 페이지 4개)

    4. audit 파일을 다음 구조로 작성:
       ```markdown
       # 35편 전수 1차 점검 — 2026-05-10

       ## 요약
       - 총 검사 파일 수: 35 (+ index 4)
       - lint-sensitive: PASS / FAIL (위반 N건)
       - lint-company: PASS / FAIL (위반 N건)
       - lint-html: PASS / FAIL (위반 N건)
       - 수동 점검: 정상 N편 / 이슈 N편

       ## lint-sensitive 결과
       (출력 그대로 붙여넣기)

       ## lint-company 결과
       ...

       ## lint-html 결과
       ...

       ## 수동 점검 결과 (편별)
       | 파일 | <title> | charset | nav 상 | nav 하 | 비고 |
       |------|---------|---------|--------|--------|------|

       ## 카테고리별 이슈
       ### 자동 검출 가능 (lint로 잡힘)
       - ...

       ### 수동 검수 필요 (lint로 잡히지 않음)
       - 맞춤법/띄어쓰기: 메모리에 기록된 6건 + 신규 발견
       - 렌더링 미세 버그: 메모리에 기록된 14건 중 lint로 안 잡힌 것

       ## 우선순위
       1. (즉시) ...
       2. (다음 phase) ...
       3. (백로그) ...
       ```

    5. P0-5 메모리 갱신을 위한 입력 자료로 사용.

    **시간 절약 팁:** 수동 점검 부분은 grep one-liner로 자동화 가능:
    ```bash
    for f in s1/*.html s2/*.html s3/*.html; do
      printf "%s\t" "$f"
      grep -q "<title>" "$f" && printf "title=Y\t" || printf "title=N\t"
      grep -q "charset" "$f" && printf "charset=Y\n" || printf "charset=N\n"
    done > /tmp/manual-check.tsv
    ```
    이 결과를 표 형식으로 audit에 포함.
  </action>
  <verify>
    <automated>
      ls "C:/Users/moons/Downloads/개발자 박대표 시리즈/.planning/audits/2026-05-10-full-sweep.md" && wc -l "C:/Users/moons/Downloads/개발자 박대표 시리즈/.planning/audits/2026-05-10-full-sweep.md"
      # 파일 존재 + 100줄 이상 (35편 표 + lint 결과를 담으려면 최소 100줄)
    </automated>
  </verify>
  <done>
    - audit 파일 존재, 5개 섹션(요약/lint 3종/수동/카테고리/우선순위) 모두 채워짐
    - 35편 전체에 대한 수동 점검 표 완성
    - 발견된 이슈가 자동/수동 카테고리로 분류됨
    - P0-5에서 이 파일을 참조하여 메모리 갱신 가능한 상태
  </done>
</task>

</tasks>

<dependency_graph>
**Wave 1 (병렬 가능):**
- P0-1 (lint-sensitive)
- P0-2 (lint-company)
- P0-3 (lint-html)
- P0-6 (사용자 직접, 비동기)

**Wave 2 (Wave 1 완료 후):**
- P0-4a (install-hooks + run-all-lints) ← P0-1, P0-2, P0-3
- P0-7 (전수 점검) ← P0-1, P0-2, P0-3

**Wave 3 (Wave 2 완료 후):**
- P0-4b (hook 시뮬레이션) ← P0-4a
- P0-5 (메모리 갱신) ← P0-7

**시간 추정:**
- P0-1: 60분 (정규식 설계 + 화이트리스트 + 검증)
- P0-2: 30분 (패턴 단순)
- P0-3: 60분 (multiline class 검출 + 인코딩 시그니처 조사)
- P0-4a: 20분
- P0-4b: 20분 (시뮬레이션)
- P0-5: 30분 (메모리 두 파일 편집)
- P0-6: 사용자 작업 (10~30분)
- P0-7: 60~90분 (35편 수동 표 작성이 가장 큼)
- 합계: 약 4.5~5.5시간 (병렬 효과 고려 시)
</dependency_graph>

<risks_and_mitigations>
| 위험 | 발생 가능성 | 대응 |
|------|-------------|------|
| Git Bash의 grep이 `-P` 미지원 | 낮음 (대부분 지원) | `-E`로 표현 가능한 패턴은 `-E` 우선. PCRE 필요 시 git for windows 버전 명시. |
| 한글 정규식이 UTF-8 환경 변수 부재 시 오작동 | 중간 | 스크립트 상단에 `export LC_ALL=C.UTF-8 || true` 추가. |
| 마스킹된 형태(`최*현`)를 false positive로 검출 | 높음 | 직원 명단을 정확한 한글 3글자로 매칭. `최.현`처럼 `.`을 쓰지 않음. |
| pre-push hook이 large repo에서 느려짐 | 낮음 (35편 ~수MB) | `git ls-files` 대신 디렉토리 직접 grep으로 충분. |
| 이메일 정규식 false positive (예: CSS 선택자 일부) | 중간 | 화이트리스트 + `\*\*\*\*` 통과 규칙. 첫 실행 후 결과 보며 튜닝. |
| 사용자가 `--no-verify`로 우회 | 중간 | install-hooks.sh가 안내 메시지로 자제 권유. 강제 차단은 server-side hook 필요(이번 phase 범위 밖). |
| GitHub 계정 점검 중 2FA 키 분실 | 낮음 | audit 템플릿에 복구코드 저장 위치 기록 필수. |
| 35편 수동 점검 누락 | 중간 | for 루프 + tsv 출력으로 자동화. 사람 눈은 카테고리별 이슈 분류에만 사용. |
| Windows 줄바꿈(CRLF)이 bash 스크립트에 섞여 실행 실패 | 높음 | `.gitattributes`에 `*.sh text eol=lf` 추가 또는 작성 시 LF 강제. |
</risks_and_mitigations>

<verification>
**Phase 종료 시 한 줄 점검:**
```bash
cd developer_park_repo \
  && bash tools/run-all-lints.sh \
  && test -x .git/hooks/pre-push \
  && test -f "../개발자 박대표 시리즈/.planning/audits/2026-05-10-full-sweep.md" \
  && test -f "../개발자 박대표 시리즈/.planning/audits/2026-05-10-github-account.md" \
  && grep -q "2026-05-10" "C:/Users/moons/.claude/projects/c--Users-moons-Downloads------------/memory/project_developer_park.md" \
  && echo "Phase 1 ALL GREEN"
```
</verification>

<success_criteria>
- [ ] `tools/lint-sensitive.sh` exit 0 on 35편 전수 (또는 의도적 위반에 exit 1)
- [ ] `tools/lint-company.sh` exit 0 on 35편 전수
- [ ] `tools/lint-html.sh` 결과가 audit에 반영됨
- [ ] `.git/hooks/pre-push` 설치 + 실행 권한
- [ ] `tools/install-hooks.sh`가 새 환경에서 1회 실행으로 hook 복원
- [ ] 메모리 두 파일에 2026-05-10 갱신 + 신규 도구 5개 등재
- [ ] GitHub 계정 audit 모든 체크박스 체크
- [ ] 35편 전수 audit 5개 섹션 완성
</success_criteria>

<output>
이 phase 완료 후 다음 위치에 기록:
- `.planning/phases/phase-1-quality-automation/SUMMARY.md` (이 PLAN을 따라 실행한 결과 요약)
- `devlogs/2026-05-10.md` (CLAUDE.md 의무 규칙)
- `.planning/audits/2026-05-10-full-sweep.md` (P0-7 산출물)
- `.planning/audits/2026-05-10-github-account.md` (P0-6 산출물)
- 메모리 두 파일 (P0-5)
</output>
