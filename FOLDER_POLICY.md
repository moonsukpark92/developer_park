# 폴더 관리 규정

> 이 규정은 "개발자 박대표 시리즈" 프로젝트의 파일/폴더 관리 표준입니다.
> 새 파일은 반드시 `_inbox/`에 업로드하고, Claude가 자동 처리합니다.

---

## 1. 표준 폴더 구조

```
개발자 박대표 시리즈/                  ← 메인 작업 디렉토리
├── CLAUDE.md                          ← 프로젝트 규칙 (자동 로딩)
├── FOLDER_POLICY.md                   ← 이 파일
├── SETUP_BLOG_FEATURES.md             ← 블로그 기능 설정 가이드
├── index.html                         ← 통합 메인 페이지
├── assets/                            ← 공용 리소스 (JS/CSS/이미지)
│   └── blog-features.js
├── s1/                                ← Season 1 (8 에피소드)
├── s2/                                ← Season 2 (9 에피소드)
├── s3/                                ← Season 3 (16 에피소드)
├── devlogs/                           ← 개발일지 (YYYY-MM-DD.md)
│
├── _inbox/                            ← 새 파일 업로드 staging (사용자 사용)
│
└── _archive/                          ← 백업/이력 (read-only)
    ├── originals_zip/                 ← 최초 zip 파일들
    ├── s1_originals/                  ← S1 원본 백업
    ├── s2_originals/                  ← S2 원본 백업
    ├── s3_originals/                  ← S3 원본 백업
    └── staging_history/               ← 처리 완료 임시 파일들

../developer_park_repo/                ← Git 저장소 (자동 동기화)
└── (메인 폴더와 동일 구조, _archive/_inbox 제외)
```

---

## 2. 새 파일 업로드 규칙

### 사용자 액션
새로운 에피소드/이미지/파일은 **`_inbox/` 폴더에 업로드**.

```
_inbox/
├── ep014.html              ← 새 에피소드
├── s3_ep014.html           ← 어떤 이름이든 OK (Claude가 표준화)
├── new_episode_v3.html     ← 임시명 OK
└── ...
```

### Claude 자동 처리
사용자가 `_inbox/`에 파일을 넣고 채팅으로 알리면 Claude가 자동으로:
1. 파일명 표준화 (ep0NN.html, prologue.html, interlude.html, epilogue*.html)
2. 민감정보 마스킹 (직원 실명, 이메일, 금융정보)
3. 회사명 통일 ((주)데코페이브)
4. 콘텐츠 맥락 점검 (footer 다음 에피소드, 시간 순서)
5. 시리즈 네비 + 하단 네비 + blog-features 통합
6. 적절한 위치 (s1/s2/s3)로 이동
7. 기존 에피소드 네비 + 인덱스 업데이트
8. 원본 동기화 + Git push
9. 라이브 사이트 검증
10. `_inbox/` 원본 → `_archive/staging_history/`로 이동

---

## 3. 파일명 표준

### 활성 파일 (s1/s2/s3 안)
| 종류 | 패턴 | 예시 |
|------|------|------|
| 정규 에피소드 | `ep0NN.html` | `ep001.html`, `ep012.html` |
| 프롤로그 | `prologue.html` | (시즌 1개) |
| 인터루드 | `interlude.html` | (시즌 1개) |
| 에필로그 | `epilogue.html` 또는 `epilogue2.html` | 다수 가능 |
| 파이널 | `final.html` | (시즌 1개) |
| 시즌 인덱스 | `index.html` | (시즌마다 1개) |

### `_inbox/`의 파일은 자유 형식
- `dev_ceo_s3_ep014.html` OK
- `new_ep.html` OK
- `s3_ep014_v2.html` OK
- → Claude가 표준 이름으로 변환 후 적절 위치에 배치

### 절대 금지
- 메인 폴더 루트(`s1/s2/s3` 외)에 HTML 직접 두기
- 숫자 패딩 없는 이름 (`ep1.html` ❌ → `ep001.html` ✅)
- 한글 파일명 (URL 인코딩 문제)
- 공백 포함 파일명

---

## 4. 폴더 별 정책

### `assets/`
- **목적**: 모든 페이지 공용 리소스
- **추가 시**: Claude가 적절한 경로 (`assets/xxx`)로 정리
- **주의**: 페이지에서는 `assets/...` (메인) 또는 `../assets/...` (시즌)로 참조

### `devlogs/`
- **목적**: 일자별 개발 기록
- **파일명**: `YYYY-MM-DD.md` (같은 날 여러 세션이면 `_02`, `_03`)
- **자동 작성**: 매 세션 종료 시 Claude가 자동 작성

### `_inbox/`
- **목적**: 새 파일 업로드 임시 위치
- **주의**: 처리 완료 후 자동으로 `_archive/staging_history/`로 이동됨
- **수동 정리 불필요**

### `_archive/`
- **목적**: 백업/이력 보관
- **원칙**: **읽기 전용** — 직접 수정/삭제 금지
- **하위 분류**:
  - `originals_zip/`: 최초 받은 zip 파일들 (보존)
  - `s1_originals/`, `s2_originals/`, `s3_originals/`: 시즌별 원본 HTML 백업
  - `staging_history/`: 처리 완료된 임시 파일들 (감사 이력용)

---

## 5. Git 저장소 정책

### `developer_park_repo/`
- **위치**: `c:/Users/moons/Downloads/developer_park_repo/`
- **원격**: `https://github.com/moonsukpark92/developer_park.git`
- **브랜치**: `main`
- **자동 동기화 대상**: 메인 폴더의 활성 파일만
  - ✅ `index.html`, `s1/`, `s2/`, `s3/`, `assets/`, `devlogs/`, `CLAUDE.md`, `SETUP_BLOG_FEATURES.md`, `FOLDER_POLICY.md`
  - ❌ `_inbox/`, `_archive/`, 단일 임시 HTML

### `.gitignore` 추가 권장
```
_inbox/
_archive/
*.zip
*.tmp
.DS_Store
```

---

## 6. 정기 정리 주기

### 월 1회 (Claude 자동)
- `_archive/staging_history/`에서 6개월 이상 된 파일 → `_archive/staging_history/{YYYY}/`로 연도별 정리
- 중복 파일 검사 (해시 기반)
- 사용 안 되는 assets 정리

### 분기 1회 (사용자 확인)
- `_archive/` 전체 검토
- 정말 불필요한 파일 영구 삭제 결정

---

## 7. 응급 시 복구

### 활성 파일 손상 시
```bash
# Git에서 복구
cd developer_park_repo && git checkout main -- s3/ep012.html
cp s3/ep012.html "../개발자 박대표 시리즈/s3/"
```

### 원본 잃어버렸을 때
- `_archive/sX_originals/`에서 복원
- 또는 `_archive/originals_zip/`의 zip 압축 해제

---

## 8. Claude 처리 요청 표준 문구

사용자가 다음과 같이 요청하면 Claude가 자동 처리:

| 요청 예시 | Claude 동작 |
|-----------|------------|
| "_inbox에 새 에피소드 올렸어" | inbox 스캔 → 자동 처리 |
| "EP014 추가해줘" | inbox에서 EP014 후보 찾아 처리 |
| "전체 점검" | 활성 파일 전수 검사 + 문제 자동 수정 |
| "정리해줘" | _inbox 처리 + staging_history 갱신 |
| "배포" | Git push + 라이브 검증 |

---

## 9. 안티 패턴 (하지 말 것)

❌ Downloads 루트에 시리즈 파일 두기 → `_inbox/`로
❌ s1/s2/s3 폴더 직접 수정 → Claude에게 요청
❌ `_archive/` 직접 수정 → 읽기 전용
❌ 임시 파일 메인 폴더 루트에 두기 → `_inbox/`로
❌ 같은 날짜에 다른 이름 devlog 만들기 → `_02`, `_03` 사용

---

**버전**: 1.0 (2026-04-16)
**관리자**: Claude Code (자동 적용)
