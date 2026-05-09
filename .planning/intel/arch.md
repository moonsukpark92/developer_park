# 아키텍처 / 구조 매핑 (arch)

**분석 일자:** 2026-05-10
**분석 대상:** `c:/Users/moons/Downloads/developer_park_repo/`
**프로젝트:** 개발자 박대표 시리즈 (정적 HTML 블로그, GitHub Pages 배포)

---

## 1. 패턴 개요

**전체 패턴:** 정적 멀티페이지 사이트(MPA) — 프레임워크/빌드 도구 없음, 순수 HTML/CSS + 인라인 JS.

**핵심 특성:**
- 페이지마다 자기 완결적(스타일 인라인 `<style>`, 스크립트 인라인 또는 단일 외부 JS)
- 시즌별 디자인 토큰 분리 (S1=빨강, S2=금색, S3=호박색)
- 라우팅 = 디렉토리 경로 (`/s3/ep011.html` 형태)
- 동적 콘텐츠는 `assets/blog-features.js` 한 파일이 모든 페이지에 주입
- 백엔드 없음 — 댓글/구독/통계는 외부 SaaS(GitHub Issues, Buttondown, Giscus, GoatCounter)

---

## 2. 디렉토리 구조

```
developer_park_repo/                ← Git 저장소 루트 (GitHub Pages 배포)
├── CLAUDE.md                       ← 프로젝트 규칙 (자동 로딩)
├── FOLDER_POLICY.md                ← 폴더 관리 규정 v1.0
├── SETUP_BLOG_FEATURES.md          ← 블로그 기능 설정 가이드
├── index.html                      ← 통합 메인 (3시즌 카드 허브)
│
├── assets/
│   └── blog-features.js            ← 모든 페이지 공용 JS (구독/댓글/통계)
│
├── devlogs/
│   └── 2026-04-16.md               ← 일자별 개발일지 (현재 1건)
│
├── s1/                             ← Season 1 (8 에피소드)
│   ├── index.html                  ← S1 인덱스 (206 lines)
│   └── ep001.html ~ ep008.html
│
├── s2/                             ← Season 2 (9개: 7 EP + epilogue + final)
│   ├── index.html                  ← S2 인덱스 (118 lines)
│   ├── ep001.html ~ ep007.html
│   ├── epilogue.html
│   └── final.html                  ← S3로의 브릿지
│
├── s3/                             ← Season 3 (16개: 13 EP + 3 특별편)
│   ├── index.html                  ← S3 인덱스 (342 lines, IntersectionObserver 사용)
│   ├── prologue.html               ← S3 시작 전 에세이
│   ├── ep001.html ~ ep013.html     ← 13편 (단, EP012는 1부=ep012, 2부=ep013)
│   ├── interlude.html              ← EP005~EP006 사이 쉬어가기
│   └── epilogue2.html              ← 시즌 마무리 (epilogue가 아닌 epilogue2 명칭)
│
└── .planning/                      ← GSD 워크플로우 (Git 추적 가능)
    ├── HANDOFF.json                ← 자동 체크포인트 상태 (auto-postool)
    ├── intel/                      ← 코드베이스 분석 (이 파일 포함)
    ├── phases/                     ← 단계별 실행 계획
    └── roadmap/                    ← 장기 로드맵
```

**원본 폴더(작업 디렉토리)와의 관계:**

```
c:/Users/moons/Downloads/개발자 박대표 시리즈/    ← 메인 작업 디렉토리 (사용자가 편집)
├── _inbox/        ← 신규 파일 업로드 staging (Git 동기화 ❌)
├── _archive/      ← 백업/이력, 읽기 전용  (Git 동기화 ❌)
│   ├── originals_zip/
│   ├── s1_originals/, s2_originals/, s3_originals/
│   └── staging_history/
└── (활성 파일은 repo와 동일)

           │ 단방향 자동 동기화 (Claude가 처리)
           ▼
c:/Users/moons/Downloads/developer_park_repo/    ← Git 저장소 (이 분석 대상)
   → GitHub: moonsukpark92/developer_park (main 브랜치)
   → 라이브: https://moonsukpark92.github.io/developer_park/
```

> **중요:** `developer_park_repo/`에는 `_inbox/`, `_archive/`가 **존재하지 않음**. `.gitignore` 또는 동기화 정책으로 제외됨. 실제 ls 결과: `CLAUDE.md FOLDER_POLICY.md SETUP_BLOG_FEATURES.md assets devlogs index.html s1 s2 s3` (그리고 `.planning/`).

---

## 3. 35편 에피소드 분포 (실측)

`Glob`으로 직접 카운트한 결과:

| 시즌 | 정규 EP | 특별편 | 합계 | 비고 |
|------|---------|--------|------|------|
| S1   | 8 (ep001~ep008) | 0 | **8** | 인덱스 1 |
| S2   | 7 (ep001~ep007) | epilogue, final | **9** | 인덱스 1 |
| S3   | 13 (ep001~ep013) | prologue, interlude, epilogue2 | **16** | 인덱스 1 |
| **총** | **28** | **5** | **33편 + 3 인덱스 + 통합 index = 37 HTML** | — |

> 통합 메인 `index.html`은 `3 SEASONS · 35 EPISODES`라 표기. S3 인덱스는 `에피소드 10편 / 인터루드 1편 / 프롤로그 1편` 메타와 별도로 `stats-bar`에 `총 에피소드 16` 표기. **표기와 실제 파일 수가 불일치**(메인=35, 실제 정규+특별=33). EP012가 1부(ep012.html) + 2부(ep013.html)로 분할되어 카운팅 방식에 따라 달라짐.

**S3 특별편 위치(논리적 흐름):**
```
prologue → ep001 → ep002 → ep003 → ep004 → ep005
        → interlude
        → ep006 → ep007 → ep008 → ep009 → ep010 → ep011
        → ep012 (1부) → ep013 (EP012 2부)
        → epilogue2
```

---

## 4. 네비게이션 시스템 — 3계층

```
┌───────────────────────────────────────────────────┐
│  Tier 1: 통합 메인 (index.html)                   │
│  ─ 시즌 카드 3개 (a.season-card.s1/s2/s3)         │
│  ─ ep-chip 미리보기 (각 시즌 에피소드 약식 표시)  │
└───────────┬───────────────────────────────────────┘
            │ href="s1/index.html" 등
            ▼
┌───────────────────────────────────────────────────┐
│  Tier 2: 시즌 인덱스 (s{1,2,3}/index.html)        │
│  ─ ep-card 그리드 (각 에피소드 1장씩)             │
│  ─ S3는 IntersectionObserver로 순차 페이드인      │
│  ─ 특별편(prologue/interlude/epilogue2)도 카드화  │
└───────────┬───────────────────────────────────────┘
            │ href="ep001.html" / "prologue.html" 등
            ▼
┌───────────────────────────────────────────────────┐
│  Tier 3: 에피소드 페이지 (ep0NN.html, 특별편)     │
│  ─ 상단 series-nav (시즌 간 이동, position:fixed) │
│  ─ 본문                                           │
│  ─ 하단 episode-nav (에피소드 간 이동, fixed)     │
│  ─ blog-features 마운트 (구독+댓글)               │
└───────────────────────────────────────────────────┘
```

### 4.1. 상단 시리즈 네비 (모든 에피소드 + 시즌 인덱스 공통)

`<div class="series-nav" style="position:fixed;top:0;left:0;right:0;z-index:9999;...">`

```
┌─────────────────────────────────────────────────┐
│ 개발자 박대표 │ S1  S2  S3                       │ ← top:0 fixed
└─────────────────────────────────────────────────┘
```

- 좌측: `../index.html` → 통합 메인 회귀 (시즌 색상으로 강조: S1=#c0392b, S2=#eab308, S3=#e8a83a)
- 우측: 형제 시즌 인덱스 3개 (`../s1/index.html`, `../s2/index.html`, `../s3/index.html`)
- 현재 시즌은 `border-bottom:2px solid` + `color:#fff`로 강조
- 모든 페이지에 인라인 스타일로 동일 패턴 반복 (외부 CSS 없음 → 중복이지만 자기완결성 우선)

### 4.2. 하단 에피소드 네비 (모든 에피소드 페이지)

`<div style="position:fixed;bottom:0;...">`

```
┌─────────────────────────────────────────────────┐
│ ← │ ☰ │ PR 01 02 03 04 05 IL 06 07 08 09 10 11 12 13 E2 │ → │ ← bottom:0 fixed
└─────────────────────────────────────────────────┘
```

- 맨 좌: `&larr;` (이전 페이지, prev)
- 좌2: `&#9776;` (☰ = 시즌 인덱스 회귀, `index.html`)
- 가운데: 모든 에피소드의 약식 라벨 (`PR`=prologue, `IL`=interlude, `01`~`13`, `E2`=epilogue2, S2는 `EP`/`FIN`)
- 맨 우: `&rarr;` (다음 페이지, next)
- 현재 페이지는 `color:#fff` + `border-bottom:2px solid` 강조

**S3 ep001의 prev/next 처리:**
- prev = `prologue.html` (시즌의 첫 정규편이므로 prologue로 회귀)
- next = `ep002.html`

**S3 epilogue2의 prev/next 처리:**
- prev = `ep013.html`
- next = `index.html` (시즌 인덱스로 닫기)

**S2 final의 시즌 간 이동:**
- prev = `epilogue.html`
- next = `../s3/index.html` ← **시즌 경계를 넘는 유일한 next 링크**
- 본문에도 `<a href="../s3/index.html" ...>SEASON 3 시작하기 →</a>` CTA 버튼 존재

### 4.3. 페이지 간 링크 흐름 (전체 그래프)

```
                  index.html (통합 메인)
                    │
        ┌───────────┼───────────────┐
        ▼           ▼               ▼
   s1/index    s2/index        s3/index
        │           │               │
   ep001~008   ep001~007       prologue
   (선형)       epilogue        ep001~005
                final ──────►   interlude
                (next=s3/index) ep006~011
                                ep012(1부) ep013(2부)
                                epilogue2
                                (next=index.html)
```

- 시즌 내부는 **상단 series-nav**(전역)와 **하단 episode-nav**(시즌 로컬) 두 축으로만 이동
- 시즌 간 직접 점프는 (a) series-nav S1/S2/S3 클릭 (b) `s2/final.html` → `s3/index` next 두 경로뿐
- **S3 → S1, S2 → S1 같은 역방향 next** 링크는 없음 (선형 진행 가정)

---

## 5. 통합 메인 → 에피소드까지의 풀 페이지 흐름

```
사용자 진입
   │
   ├─[A] GitHub Pages 루트(/) → index.html
   │     ↓ (a.season-card 클릭)
   │   s{1,2,3}/index.html
   │     ↓ (a.ep-card 또는 ep-chip 클릭)
   │   s{N}/ep0NN.html
   │     ↓ (하단 → 화살표)
   │   s{N}/ep0(NN+1).html
   │     ↓ ... 시즌 끝까지 ...
   │   다음 시즌 또는 통합 메인 회귀
   │
   ├─[B] 직접 URL (예: /s3/ep011.html) — 검색/공유 링크
   │     → series-nav로 어디서든 시즌 전환 가능
   │
   └─[C] GitHub Issues/Buttondown 외부 링크 → 본문 페이지
```

각 페이지 하단 `blog-features` 영역에서 **이메일 구독(Buttondown)** 또는 **댓글 작성(Giscus → GitHub Discussions)**으로 분기.

---

## 6. `assets/blog-features.js` — 동적 콘텐츠 주입 패턴

**역할:** 모든 페이지가 공유하는 단일 진입점 스크립트(143줄). `<div id="blog-features-mount"></div>`를 가진 페이지에 자동으로 구독/댓글/통계 UI를 주입.

**주입 메커니즘:**

```
페이지 로드
  │
  ▼
<script src="assets/blog-features.js"> (메인) 또는
<script src="../assets/blog-features.js"> (s1/s2/s3 안)
  │
  ▼
IIFE 실행
  ├─ document.getElementById('blog-features-mount') 확인
  ├─ document.title → pageTitle (이슈 제목 자동 입력용)
  ├─ window.location.* → 페이지 식별자
  │
  ├─ CONFIG 분기:
  │    isConfigured(buttondown)  → 이메일 폼 / 아니면 GitHub Watch 버튼
  │    isConfigured(giscus.*)    → Giscus 댓글창 / 아니면 GitHub Issues 링크
  │    isConfigured(goatcounter) → <script async data-goatcounter=...> head 주입
  │
  └─ mount.innerHTML = `${subscribeHtml}${commentsHtml}` 한 번에 주입
```

**현재 활성 설정 (CONFIG):**
- `github`: `moonsukpark92/developer_park`
- `buttondown`: `moonsuk` (이메일 구독 활성)
- `giscus.repoId`: `R_kgDOSD0bmQ`, `categoryId`: `DIC_kwDOSD0bmc4C8rg5` (활성)
- `goatcounter`: `developerpark` (활성)

**핵심 디자인 결정:**
- 페이지마다 같은 UI를 인라인으로 박지 않고, **단일 JS가 런타임에 `innerHTML` 한 방으로 주입**
- 외부 CSS 의존 없이 인라인 스타일로 자기완결 (JS 비활성 환경에서는 단순히 영역이 빈 채로 표시됨)
- Giscus 미설정 시 **GitHub Issues new URL을 미리 인코딩**해 폴백 (`?title=💬...&body=...&labels=comments`)
- `data-mapping: 'pathname'` → 같은 URL = 같은 댓글 스레드 (페이지마다 자동 분리)

**주입 결과 DOM 구조 (런타임):**
```html
<div id="blog-features-mount">
  <div style="background:#0a0b12;border-top:1px solid ...">
    <div style="max-width:680px;margin:0 auto;">
      [구독 섹션 — Buttondown form 또는 GitHub Watch 버튼]
      [댓글 섹션 — Giscus iframe 또는 GitHub Issues 링크]
    </div>
  </div>
</div>
<!-- head에 GoatCounter <script> 추가됨 -->
```

---

## 7. Git 저장소 ↔ 원본 폴더 ↔ `_archive` / `_inbox` 관계

```
┌────────────────────────────────────────────────────────────────┐
│  사용자가 새 에피소드 zip/HTML을 업로드                         │
│           │                                                    │
│           ▼                                                    │
│  메인 작업 디렉토리/_inbox/   ← 자유 형식 파일명 OK             │
│           │                                                    │
│           │ Claude 자동 처리:                                  │
│           │  1. 파일명 표준화 (ep0NN.html)                     │
│           │  2. 민감정보 마스킹 (직원 실명 → 최*현 등)         │
│           │  3. 회사명 통일 ((주)데코페이브)                   │
│           │  4. series-nav + 하단 nav + blog-features 통합     │
│           │  5. 적절한 시즌 폴더로 이동                        │
│           │  6. 기존 에피소드 nav/index 갱신                   │
│           ▼                                                    │
│  메인 작업 디렉토리/s{1,2,3}/  ← 활성 파일 (작가 기준 원본)     │
│           │                                                    │
│           │ 양방향이 아닌 단방향 sync:                         │
│           │  메인 → repo (자동)                                │
│           ▼                                                    │
│  developer_park_repo/s{1,2,3}/   ← Git 추적 대상                │
│           │                                                    │
│           │ git push origin main                               │
│           ▼                                                    │
│  GitHub (moonsukpark92/developer_park) → GitHub Pages 배포     │
│                                                                │
│  처리 완료된 _inbox 파일은:                                    │
│           메인/_inbox/* → 메인/_archive/staging_history/       │
│  (감사 이력 보존, 6개월 후 연도별 폴더로 자동 정리 정책)        │
│                                                                │
│  최초 zip 백업: 메인/_archive/originals_zip/                   │
│  시즌별 백업:   메인/_archive/s{1,2,3}_originals/              │
│  (모두 read-only, 직접 수정 금지)                              │
└────────────────────────────────────────────────────────────────┘
```

**Git 동기화 대상 (FOLDER_POLICY.md §5 기준):**

| 항목 | 동기화 |
|------|--------|
| `index.html`, `s1/`, `s2/`, `s3/`, `assets/`, `devlogs/` | ✅ 동기화 |
| `CLAUDE.md`, `SETUP_BLOG_FEATURES.md`, `FOLDER_POLICY.md` | ✅ 동기화 |
| `.planning/` (HANDOFF, intel, phases, roadmap) | ✅ (현재 commit 안 됐을 가능성, 신규) |
| `_inbox/`, `_archive/`, `*.zip`, `*.tmp` | ❌ `.gitignore` |

**복구 경로:**
- 활성 파일 손상 → `git checkout main -- s3/ep012.html` → `cp` to 메인 폴더
- 원본 잃어버림 → `_archive/sX_originals/` 또는 `_archive/originals_zip/`

---

## 8. 엔트리 포인트 / 진입 책임

| Entry Point | 위치 | 책임 |
|-------------|------|------|
| 통합 메인 | `index.html` | 3시즌 카드 허브, 사이트 첫 인상, hero/stats/about/footer + blog-features |
| 시즌 허브 | `s{1,2,3}/index.html` | 해당 시즌의 모든 에피소드 카탈로그, 통계 바, 특별편 분리 표시 |
| 정규 에피소드 | `s{N}/ep0NN.html` | 본문(에세이), 시즌 nav, 에피소드 nav, blog-features |
| 특별편 | `s{N}/{prologue,interlude,epilogue,epilogue2,final}.html` | 시즌 흐름 내 위치에 따라 prev/next가 인접 에피소드를 가리킴 |

---

## 9. 횡단 관심사 (Cross-Cutting)

| 관심사 | 처리 방식 | 위치 |
|--------|-----------|------|
| 외부 폰트 | Google Fonts CDN (Syne, Noto Serif KR, JetBrains Mono, DM Mono, Noto Sans KR) | 각 페이지 `<head>` |
| 시즌별 컬러 토큰 | CSS 변수 `--s1/--s2/--s3` (통합 메인) / `--amber/--gold/...` (시즌 페이지) | 인라인 `<style>` |
| 구독/댓글/통계 | `assets/blog-features.js` (단일 외부 JS) | 모든 페이지 끝 |
| SEO/메타 | `<title>`, `<meta name="description">` 페이지마다 직접 작성 | 각 페이지 `<head>` |
| 애니메이션 | S3 시즌/에피소드 페이지에서 IntersectionObserver로 ep-card 순차 페이드인 | 인라인 `<script>` |
| 민감정보 마스킹 | 직원명 한 글자 마스킹(최*현), 이메일 `m****@*****.co.kr`, 금융/내부 URL `**`/`***` | 콘텐츠 작성 시점에 정적 마스킹 |
| ㈜ 표기 | `&#x321C;` 사용 (㎎=`&#x338E;` 금지) | 본문 HTML |

---

## 10. 관찰된 일관성/특이점

**일관성:**
- 모든 에피소드 페이지가 동일한 series-nav + episode-nav 패턴(인라인 스타일)을 따름
- 모든 페이지 끝이 `<div id="blog-features-mount"></div><script src=".../blog-features.js"></script>`로 통일
- 경로 참조: 메인은 `assets/...`, 시즌 페이지는 `../assets/...` 일관

**특이점/주의:**
- `s3/ep013.html`은 파일명상 EP013이지만 콘텐츠는 **EP012 2부**. 향후 EP014 추가 시 파일명 vs 콘텐츠 번호 불일치가 누적될 위험.
- 통합 메인의 "35 EPISODES" 표기와 실제 활성 HTML 개수가 카운팅 정의에 따라 달라짐 → 메타 표기 갱신 정책 미정의.
- `devlogs/`에 1건만(`2026-04-16.md`) 존재하나 CLAUDE.md는 "모든 세션 종료 시 의무 작성" 규정 → 반영 격차 존재.
- `.planning/` 디렉토리는 GSD 워크플로우 산출물이며, FOLDER_POLICY.md(v1.0)에는 명시되지 않음 → 정책 v1.1에서 명문화 필요.
- 인라인 `<style>` + 인라인 nav HTML 중복 → 새 에피소드 추가 시 **블록 단위 복붙 + 현재 페이지 강조 위치만 변경**하는 패턴.

---

*아키텍처 분석 완료: 2026-05-10*
