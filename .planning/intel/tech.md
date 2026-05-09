# 기술 스택 매핑 — 개발자 박대표 시리즈

**분석 일자:** 2026-05-10
**대상 저장소:** `c:/Users/moons/Downloads/developer_park_repo/`
**프로젝트 성격:** 정적 HTML 인터랙티브 에세이 시리즈 (3시즌, 31+ 에피소드)

---

## 1. 핵심 기술 스택

### 언어 / 런타임
- **HTML5**: 모든 콘텐츠가 단일 파일(self-contained) HTML로 작성. 시즌별 페이지마다 인라인 `<style>` 또는 `@import` 방식으로 CSS 내장.
- **CSS3**: 외부 CSS 파일 없음 — 페이지마다 인라인. `:root` 커스텀 프로퍼티(CSS 변수) 패턴으로 시즌별 색 팔레트 정의.
- **JavaScript (Vanilla)**: 프레임워크/번들러 없음. 시즌3 본문 일부와 공통 `assets/blog-features.js`에서만 사용.

### 빌드 도구
- **없음**. 정적 HTML 그대로 GitHub Pages가 서빙. 트랜스파일/번들/포스트프로세싱 단계 0.
- `package.json`, `node_modules`, `.github/workflows/` 모두 부재. 순수 정적 사이트.

---

## 2. 디렉토리 / 파일 구조 (활성)

```
developer_park_repo/
├── index.html                ← 통합 메인 (354 lines, S1+S2+S3 허브)
├── assets/
│   └── blog-features.js      ← 공용 JS (구독/댓글/통계 통합 위젯)
├── s1/  index.html + ep001~ep008.html
├── s2/  index.html + ep001~ep007.html + epilogue.html + final.html
├── s3/  index.html + prologue.html + ep001~ep013.html + interlude.html + epilogue2.html
├── devlogs/                  ← YYYY-MM-DD.md 일자별 개발일지
├── CLAUDE.md / FOLDER_POLICY.md / SETUP_BLOG_FEATURES.md
└── .gitignore
```

- **공용 리소스 (`assets/`)**: 현재 단 1개 파일 — `blog-features.js` (143 lines).
- **CSS / 이미지 자산 없음**: 모든 스타일은 페이지 내부, 모든 비주얼은 CSS 그라디언트/SVG 데이터 URI로 처리.

---

## 3. 시즌별 기술 차이

| 항목 | S1 (밝은 톤) | S2 (다크 + 글리치) | S3 (딥다크 + 새벽빛) |
|------|--------------|--------------------|---------------------|
| 배경색 | `--paper:#f5f0e8` (베이지) | `--bg:#06080c` 다크 | `--void:#04050a` 딥다크 |
| 액센트 | `--accent:#c0392b` (빨강) | `--accent:#ef4444` + `--gold:#eab308` | `--amber:#e8a83a` (호박색) |
| JS 사용 | **없음** (순수 CSS) | **없음** (순수 CSS, 글리치/스캔라인 키프레임) | **있음** (IntersectionObserver) |
| 키프레임 수 | 2개 (`fadeUp`, `scrollPulse`) | 8+ (`pulseGlow`, `termType`, `blink`, `breathe`, `scanline` 등) | fade 계열 + grain 오버레이 |
| 노이즈/그레인 | 없음 | `repeating-linear-gradient` 스캔라인 | **SVG `feTurbulence` 인라인 데이터 URI** (`body::before`) |
| 폰트 | Noto Serif KR + JetBrains Mono + Noto Sans KR | + Cormorant Garamond 추가 | + Syne + DM Mono 추가 |
| 페이지 길이 | ~320 lines | ~817 lines | ~838 lines |
| 분위기 | 신문 에세이 | 터미널/사이버펑크 | 새벽 다큐멘터리 |

### 시즌3 특이사항
- **SVG 노이즈 그레인**: `body::before`에 `data:image/svg+xml,...feTurbulence...` 인라인 SVG로 필름 그레인 구현 (외부 이미지 미사용).
- **IntersectionObserver**: 13개 S3 페이지 전부에서 사용. `threshold:0.1`, `rootMargin:'0px 0px -40px 0px'`로 스크롤 진입 시 `.visible` 클래스 토글, 60ms 스태거 애니메이션.
- 일부 후기 에피소드(`ep011.html`, `ep012.html`, `ep013.html`, `epilogue2.html`)는 폰트 패밀리가 다름 — Nanum Myeongjo, Gowun Batang 등 포함. 시즌 표준에서 벗어난 변형.

---

## 4. 외부 서비스 / 통합

### 4.1 GitHub Pages (호스팅)
- **URL**: https://moonsukpark92.github.io/developer_park/
- **저장소**: `moonsukpark92/developer_park` (branch: `main`)
- **배포 방식**: `git push` → 1-2분 후 자동 반영. Jekyll 사용 안 함 (`.nojekyll` 없지만 `_` 시작 폴더가 활성 폴더에 없음).
- **CI 파이프라인 없음**: `.github/workflows/` 부재. GitHub Pages 기본 자동 빌드만 사용.
- **CNAME / 커스텀 도메인 없음**.

### 4.2 Giscus (댓글)
- **방식**: GitHub Discussions 기반 댓글창. `assets/blog-features.js`에서 `https://giscus.app/client.js` 동적 로딩.
- **설정값** (`blog-features.js` CONFIG):
  - `repoId: 'R_kgDOSD0bmQ'`
  - `categoryId: 'DIC_kwDOSD0bmc4C8rg5'`
  - `data-mapping: 'pathname'`, `data-theme: 'dark_dimmed'`, `data-lang: 'ko'`, `data-loading: 'lazy'`
- **폴백**: 미설정 시 GitHub Issues 새 글 작성 링크로 대체.

### 4.3 Buttondown (이메일 구독)
- **방식**: `<form action="https://buttondown.com/api/emails/embed-subscribe/{username}">` 임베드 폼.
- **설정값**: `buttondown: 'moonsuk'`
- **폴백**: 미설정 시 GitHub Watch 링크 안내.

### 4.4 GoatCounter (방문 통계)
- **방식**: `https://gc.zgo.at/count.js` 비동기 스크립트 동적 추가.
- **설정값**: `goatcounter: 'developerpark'` → `https://developerpark.goatcounter.com/count`

### 4.5 Google Fonts
- **로딩 방식**: 두 가지 혼재
  - `<link rel="stylesheet" href="https://fonts.googleapis.com/css2?...">` (S1, S3, index)
  - `@import url('...')` (S2 일부, S3 후기 ep011/ep012/ep013)
- **사용 폰트 전체 목록**:
  - Noto Serif KR (300/400/600/700/900) — 본문 기본
  - Noto Sans KR (300/400/500/700/900) — 보조 산세리프
  - JetBrains Mono (300/400/600/700) — 코드/라벨
  - DM Mono (italic 포함) — S3 라벨 액센트
  - Syne (400/700/800) — S3 + index 헤드라인
  - Cormorant Garamond (italic 포함) — S2 일부
  - Nanum Myeongjo (400/700/800) — S3 ep011 변형
  - Gowun Batang — S3 ep011 변형
- **`<link rel="preconnect" href="https://fonts.googleapis.com">`**: S3 일부에만 적용 (성능 최적화 일관성 부족).

---

## 5. `assets/blog-features.js` 구조

각 페이지 하단의 `<div id="blog-features-mount">`를 찾아 다음을 동적 렌더링:

1. **구독 섹션**: Buttondown CONFIG 설정 시 임베드 폼, 미설정 시 GitHub Watch 버튼.
2. **댓글 섹션**: Giscus repoId/categoryId 모두 설정 시 `giscus.app/client.js` 로드, 아니면 GitHub Issues 새 글 링크.
3. **방문 통계**: GoatCounter username 설정 시 `gc.zgo.at/count.js` 비동기 추가.

설정 게이팅 헬퍼: `isConfigured(val) => val && !val.startsWith('YOUR_')`.

40개 HTML 파일이 이 스크립트를 참조 (`blog-features-mount` 또는 `blog-features.js` 매칭).

---

## 6. 배포 파이프라인

```
[작성 PC] 개발자 박대표 시리즈/  (원본)
        ↓ 수동 동기화 (Claude가 양쪽 폴더에 동시 작성)
[Git PC] developer_park_repo/   (.git)
        ↓ git push origin main
GitHub  moonsukpark92/developer_park
        ↓ GitHub Pages 자동 빌드 (Jekyll off, 정적 그대로)
Live    https://moonsukpark92.github.io/developer_park/
```

- 빌드 단계 없음. 푸시한 파일이 그대로 URL.
- `.gitignore`: `_inbox/`, `_archive/`, `*.zip`, `*.tmp`, `.vscode/`, `.idea/`, `.DS_Store`, `Thumbs.db` 제외.

---

## 7. 환경 / 종속성 요약

- **런타임 종속성**: 브라우저만 (모던 브라우저 — `IntersectionObserver`, CSS `clamp()`, custom properties, SVG inline data URI 모두 사용).
- **빌드 종속성**: 0개.
- **외부 호출 도메인** (런타임):
  - `fonts.googleapis.com`, `fonts.gstatic.com` (폰트)
  - `giscus.app`, `github.com` (댓글, 게이트키핑)
  - `buttondown.com` (구독 폼 액션)
  - `gc.zgo.at`, `{user}.goatcounter.com` (통계)
- **API 키 / 시크릿 없음**: 모든 통합이 공개 가능한 username/repoId/categoryId 만으로 구성.

---

## 8. 일관성 부족 / 주의 영역

- **폰트 로딩 방식 혼재**: `<link>` vs `@import` 두 패턴. `@import`는 렌더링 차단 가능성.
- **시즌별 색 변수 명명 불일치**: S1 `--accent`, S2 `--accent`+`--accent2`, S3 `--amber`/`--gold`/`--dawn` 다층 — 공용 디자인 토큰 부재.
- **S3 후기 에피소드(ep011~ep013, epilogue2) 폰트 변형**: 시즌 표준 Syne+DM Mono 라인에서 벗어남. 의도/누락 구분 필요.
- **`preconnect` 적용 비일관**: 일부 S3 페이지에만 존재.
- **공용 자산 단 1개**: `blog-features.js` 외 공통 CSS/유틸 없음 → 페이지마다 스타일 중복. 향후 공용 헤더/푸터 추출 시 이 점 고려.

---

*이 문서는 `/gsd:plan-phase`에서 신규 에피소드 추가, 디자인 토큰 통합, 외부 서비스 교체 등의 작업 계획 시 참조됩니다.*
