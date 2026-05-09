# Quality Intel — 개발자 박대표 시리즈

**분석일자**: 2026-05-10
**대상 저장소**: `c:/Users/moons/Downloads/developer_park_repo/`
**Focus**: quality (품질 보증, 검수, 자동화, 알려진 이슈)

---

## 1. 품질 보증 절차 개요

### 1.1 현재 운영 중인 품질 절차
- **운영 주체**: Claude Code 단일 에이전트 (인간 검수자 없음)
- **트리거**: 새 에피소드 추가, 기존 콘텐츠 수정, `_inbox/` 업로드, 사용자의 "전체 점검" 요청
- **점검 시점**: ① 콘텐츠 수정 직후 → ② Git push 직전 → ③ Git push 직후 라이브 검증
- **자동성 수준**: 사용자 확인 없이 자동 적용 (`feedback_auto_review_fixes.md`, `feedback_auto_workflow.md`)

### 1.2 품질 게이트가 명시된 위치
- `CLAUDE.md` (루트) — 절대 금지 항목 + 자동 워크플로우 (sec.8/9/11)
- `FOLDER_POLICY.md` — `_inbox/` → 자동 처리 10단계 (sec.2)
- 메모리: `feedback_auto_workflow.md` — A/B/C/D 단계별 체크리스트
- 메모리: `project_devpark_pending_fixes.md` — 미해결 이슈 트래킹

### 1.3 부재한 절차
- 자동화된 단위/통합 테스트 부재 (정적 HTML 사이트라 우선순위 낮음)
- CI/CD 파이프라인 없음 (GitHub Pages는 push 시 자동 배포만)
- 린터/포매터 미설정 (HTMLHint, prettier 등 도입 안 됨)
- 인간 검수 단계 없음 — 사용자는 결과만 통보받음

---

## 2. 검수 자동화 시스템

### 2.1 3중 자동화 레이어
| 레이어 | 위치 | 역할 |
|--------|------|------|
| **CLAUDE.md** (루트) | `c:/Users/moons/Downloads/developer_park_repo/CLAUDE.md` | 세션 시작 시 자동 로딩, 절대 금지/자동 워크플로우 정의 |
| **FOLDER_POLICY.md** | `c:/Users/moons/Downloads/developer_park_repo/FOLDER_POLICY.md` | 폴더 관리, `_inbox/`→`_archive/` 흐름, 표준 파일명 |
| **메모리 시스템** | `C:/Users/moons/.claude/projects/c--Users-moons-Downloads------------/memory/` | 11개 파일 (인덱스 + 피드백 6 + 프로젝트 3 + 사용자 1) |

### 2.2 메모리 파일 인벤토리
- `MEMORY.md` — 인덱스
- `feedback_auto_review_fixes.md` — 검수 자동 적용 정책
- `feedback_auto_workflow.md` — A(콘텐츠 정제)/B(시스템 통합)/C(인덱스)/D(배포) 자동화
- `feedback_devlog_mandatory.md` — 개발일지 의무 작성
- `feedback_folder_policy.md` — `_inbox` 자동 처리
- `feedback_style_philosophy.md` — 의도 전달 우선, 문체 존중
- `feedback_time_economy.md` — 묻지 말고 처리, 병렬 실행
- `project_developer_park.md` — 프로젝트 현황 (23일 전 메모 — 갱신 필요)
- `project_devpark_pending_fixes.md` — 미해결 이슈 트래커
- `project_decohub_agent.md` — 별도 프로젝트
- `user_moonsuk.md` — 사용자 프로필

### 2.3 메모리 신선도 이슈
- 다수의 메모리가 23일 전 시점 (시스템 리마인더 표시) → 점검 시 코드 실측 검증 필요
- `project_developer_park.md`: "31개 에피소드"로 기록되어 있으나 실제 35편으로 확장됨
- `project_devpark_pending_fixes.md`: "현재 0건"이지만 메모리는 14건 시점

---

## 3. 자동 점검 항목 (수동 매뉴얼 + 자동 워크플로우 결합)

### 3.1 콘텐츠 정제 (A 단계)
1. **민감정보 마스킹**
   - 박문석(CEO/작가): 마스킹 금지, 원래 이름 존치
   - 직원 실명: `홍길동 → 홍*동` (중간 글자 *) — 14명 명단 (최*현, 조*진, 임*영, 정*윤, 한*주, 조*범, 신*혜, 허*민, 이*우, 서*표, 오*벡, 김*완, 박*연, 강*구)
   - 이메일: `m****@*****.co.kr` 형태
   - 금융정보: `**억`, `**은행`
   - 내부 URL: `***.***.co.kr`
   - 좌표: `nx=**, ny=***`
2. **회사명 통일**: `데코페이브㈜`, `((주)데코페이브)` 등 변형 → `(주)데코페이브` 단일화
3. **콘텐츠 맥락 점검**: footer "다음 에피소드" 링크 정합성, 시간 순서, 명칭 일관성(DECOHUB, 문실장, JARVIS-CC)
4. **맞춤법/HTML 무결성**: 명백한 오타만, 구어체 존중, HTML 속성 중복 검사

### 3.2 HTML/CSS 무결성 절대 금지 항목 (CLAUDE.md sec.11)
- CSS 색상값 언더스코어 사용 금지: `#색상_40` ❌ → `#색상40` ✅
- HTML 속성 중복 (class 2번 선언) 금지
- ㈜ 인코딩: `㈜` 사용, `&#x338E;`(㎎) 사용 금지
- 박문석 마스킹 금지

### 3.3 시스템 통합 (B 단계)
- 파일명 표준화: `ep0NN.html`, `prologue.html`, `interlude.html`, `epilogue*.html`
- 시리즈 네비(top:0) + 하단 에피소드 네비(bottom:0) 추가 — **div 사용 필수** (nav 태그는 CSS 충돌)
- body padding: `top:40px; bottom:60px`
- S3 `body::before` z-index: `-1` (콘텐츠 가림 방지)
- blog-features 마운트 + `../assets/blog-features.js` 스크립트 추가
- 기존 모든 에피소드 네비에 신규 에피소드 링크 동기화

### 3.4 배포 전 종합 검수 체크리스트 (자동)
- [ ] 마스킹 누락 검사 (실명/이메일/금융)
- [ ] 회사명 일관성
- [ ] HTML 무결성 (중복 속성, 미닫힘 태그)
- [ ] 링크 무결성 (존재하지 않는 파일 참조)
- [ ] 시리즈 네비 + 하단 네비 + blog-features 통합 여부
- [ ] `body::before` z-index 처리
- [ ] 시즌 간 연결 (S1→S2→S3)
- [ ] 시간 순서/맥락 일관성

---

## 4. 배포 후 검증 (라이브 점검)

### 4.1 워크플로우
1. Git push origin main
2. GitHub Pages 배포 대기 (1~2분)
3. `curl`로 200 응답 확인 → WebFetch로 핵심 페이지 4~5개 실접속
4. 정상 렌더링 확인
5. 문제 발견 시 자동 수정 + 재푸시

### 4.2 검증 도구
- **WebFetch**: 라이브 페이지 콘텐츠 실측
- **GitHub Pages 라이브 URL**: https://moonsukpark92.github.io/developer_park/
- **Playwright MCP**: (글로벌 MCP 11개 중 하나, 시각 검증 가능하나 현재 워크플로우에서는 미사용)

### 4.3 검증 부재 영역
- 모바일 반응형 자동 점검 없음
- 크로스 브라우저 테스트 없음
- 접근성(a11y) 점검 없음
- 페이지 로드 성능(LCP, CLS) 점검 없음

---

## 5. 발견된 이슈 패턴 (반복 발생)

### 5.1 고빈도 패턴 — 메모리 + Git 이력 기반
| 패턴 | 빈도 | 근거 (커밋/메모리) |
|------|------|-------------------|
| **CSS 색상 언더스코어** (`#색상_40`) | S1 ep002~008 (7건) | `project_devpark_pending_fixes.md` |
| **`body::before` z-index 가림** | S3 전체 4회 fix | `2b3c55c`, `48d13fa`, `6b79a29`, `381d668` |
| **㈜ 인코딩 오류** (`&#x338E;` ㎎, `&#xAC8C;` 게) | S3 ep008/009/010 (3건) | pending_fixes |
| **회사명 표기 변형** (`데코페이브㈜`, `((주)데코페이브)`) | 39건+이중 괄호 | `ba5b064`, `b21aecc`, `6846f8c` |
| **class 속성 중복** | S3 ep003:841 외 | pending_fixes, CLAUDE.md sec.11 |
| **HTML data-label 파싱 오류** | S3 ep002:753, ep003:789 | pending_fixes |
| **CSS 선택자 공백** (`.  decomp-key`) | S3 ep008:139 | pending_fixes |
| **title 태그 불일치** | S2 ep001/ep002 | pending_fixes |
| **민감정보 마스킹 누락/정책 변동** | 1회 정책 수정 | `4cc9c46` (실명 마스킹 정책 수정) |

### 5.2 패턴 분석
- **렌더링 버그**(CSS/HTML 무결성)가 콘텐츠 오타보다 빈도와 심각도 모두 높음
- **㈜ 글자 변환**은 텍스트 처리 도구의 인코딩 결함에서 반복 — 자동 검사 도입이 가장 ROI 높음
- **회사명 표기**는 4회의 fix 커밋이 있을 정도로 반복 — 단일 정규화 함수 필요
- **z-index/네비게이션 오버레이**는 S3에서만 발생 — S3 전용 템플릿 안정화 필요

---

## 6. 테스트 부재

- **자동화 테스트 없음**: 단위/통합/E2E 모두 부재
- **정적 사이트 특성상 우선순위 낮음**: 백엔드 로직 없음, JS도 IntersectionObserver 정도
- **현재 검증 방식**: 사람(Claude) 안목 + WebFetch 라이브 점검
- **개선 권장**: 7장 참조

---

## 7. 콘텐츠 검토 절차

### 7.1 현재 검토 흐름
1. 사용자가 `_inbox/`에 업로드 또는 채팅으로 요청
2. Claude가 콘텐츠 정제(A) → 시스템 통합(B) → 인덱스(C) → 배포(D) 4단계 수행
3. 발견 사항은 `project_devpark_pending_fixes.md`에 누적
4. 다음 업데이트 시 자동 적용 (사용자 확인 없이)
5. 적용 후 개발일지(`devlogs/YYYY-MM-DD.md`)에 기록 + pending에서 제거

### 7.2 활용 가능한 보조 도구 (현재 미연동)
- **gsd-doc-verifier**: 문서/콘텐츠 정합성 검증 가능 — `.planning/phases/`와 결합해 PR-style 리뷰 가능
- **graphify Skill**: `/graphify` 명령으로 콘텐츠 → 지식 그래프화 (스토리/명칭 일관성 검증에 활용 가능)
- **Memory Server MCP**: 검토 발견 사항을 자동으로 `project_devpark_pending_fixes.md`에 기록하도록 강화 가능

### 7.3 검토 기준 (CLAUDE.md sec.8 명시)
- 맞춤법/띄어쓰기 한국어 표준
- 구어체 문체는 작가 의도로 존중 (`feedback_style_philosophy.md`)
- 민감정보 마스킹 필수
- CSS 언더스코어 금지, HTML 속성 중복 금지, ㈜ 인코딩 정확도

---

## 8. 알려진 미해결 이슈

### 8.1 현재 상태
- `project_devpark_pending_fixes.md` 갱신 시점: 2026-04-16 (23일 전)
- 메모리 인덱스(`MEMORY.md`)에는 "현재 0건, 갱신 시 기록"으로 표기
- 최신 커밋 `0874890 fix: 점검 발견 사항 수정` (2026-04-16 이후 일괄 fix됨 — 추정)
- Git 이력상 ㈜ 표기, body::before, S3 EP011 교체 등 주요 fix는 적용 완료

### 8.2 추적 보강 필요
- pending_fixes 메모리는 23일 전 스냅샷 — **신규 점검 후 갱신 필요**
- 현재 0건이라는 표기가 실제 0건인지, 단지 추적이 멈춘 것인지 검증 필요
- 정기 전수 점검(분기 1회 권장)이 정책상 명문화되지 않음

### 8.3 갱신 트래킹 권장 형식
```markdown
### YYYY-MM-DD 점검
- 검사 범위: s1/, s2/, s3/ 전체
- 검사 항목: [위 3.2 절대 금지 + 3.4 종합 체크]
- 결과: 높음 N건 / 중간 M건 / 낮음 K건
- 자동 적용 여부: [완료 / 일부 / 미적용]
```

---

## 9. 개선 권장사항

### 9.1 즉시 적용 가능 (낮은 비용)
1. **간단한 정적 점검 스크립트 도입**
   - `tools/lint.py` 또는 `tools/lint.sh`: HTML 파일을 grep/regex로 점검
   - 점검 항목: `#[0-9a-f]+_`, `class="[^"]*"\s+class=`, `&#x338E;`, `&#xAC8C;`, `데코페이브㈜`, `((주)데코페이브)` 패턴
   - GitHub Actions에 등록하면 push 시 자동 검증
2. **메모리 정기 갱신 루틴**
   - 매 세션 종료 시 `project_devpark_pending_fixes.md`의 timestamp 명시적 갱신
   - "현재 0건" 표기 시점도 기록 (`Last verified: YYYY-MM-DD`)
3. **회사명 정규화 함수**
   - 콘텐츠 처리 시 모든 회사명 변형을 `(주)데코페이브`로 자동 치환하는 공통 단계 명문화

### 9.2 중기 도입 (중간 비용)
4. **HTMLHint + Stylelint 도입**
   - 닫히지 않은 태그, 중복 속성, 잘못된 색상값 자동 감지
   - `npm install --save-dev htmlhint stylelint` + 설정 파일
5. **링크 검사 자동화**
   - `lychee` 또는 `markdown-link-check` 등으로 내부/외부 링크 무결성 검증
6. **시각 회귀 테스트** (Playwright)
   - 핵심 페이지(메인, S1/S2/S3 인덱스, 각 시즌 첫 에피소드) 스크린샷 비교
   - z-index/오버레이 회귀 자동 감지

### 9.3 장기 도입 (높은 가치)
7. **Lighthouse CI**
   - 성능/접근성/SEO 자동 점수화
   - 정적 사이트라도 LCP/CLS는 사용자 경험에 직접 영향
8. **GitHub Actions PR 워크플로우**
   - `_inbox/` PR 형태로 운영 → 자동 검수 → 통과 시 main 머지
   - 현재는 main에 직접 push라 롤백 시 불편
9. **gsd-doc-verifier 정식 통합**
   - 콘텐츠(에피소드 .html)에 대한 doc-verifier 실행 표준화
   - `.planning/phases/`와 결합해 점검 결과를 phase 산출물로 관리

### 9.4 운영 정책 보강
10. **분기 1회 전수 점검** 명문화 (현재 `FOLDER_POLICY.md` sec.6에는 _archive 정리만 분기 단위)
11. **점검 기록의 표준 양식**을 `devlogs/`에 별도 카테고리로 보관 (`devlogs/audits/YYYY-Q1.md`)

---

## 10. 요약

- 품질 보증은 **Claude 단일 에이전트 자동화**에 전적으로 의존하며, 인간 검수/CI/테스트 부재
- **3중 명세**(CLAUDE.md + FOLDER_POLICY.md + 메모리 시스템)로 정책은 견고하게 정의되어 있음
- 반복 이슈 패턴은 **HTML/CSS 무결성**(언더스코어, z-index, 인코딩, 속성 중복) > 콘텐츠 오타
- 현재 가장 큰 약점은 **점검의 정기성과 기록 갱신** — 메모리가 23일 전 시점에 멈춰 있음
- 가장 ROI 높은 개선은 **단순 grep 기반 lint 스크립트 + GitHub Actions 자동 실행**

---

*Quality intel: 2026-05-10*
