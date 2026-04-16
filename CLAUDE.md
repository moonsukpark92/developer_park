# 개발자 박대표 시리즈 — 프로젝트 규칙

> 이 파일은 새 세션 시작 시 자동 로딩됩니다.
> 아래 규칙을 모든 세션에서 반드시 준수하세요.

## 1. 프로젝트 개요

- **프로젝트명**: 개발자 박대표 (developer_park)
- **성격**: CEO의 AI 도입 실전 기록 — HTML 기반 인터랙티브 에세이 시리즈
- **GitHub**: https://github.com/moonsukpark92/developer_park.git
- **GitHub Pages**: https://moonsukpark92.github.io/developer_park/
- **시리즈**: 3개 시즌, 총 31개 에피소드

## 2. 디렉토리 구조

```
개발자 박대표 시리즈/          ← 작업 디렉토리 (원본)
├── CLAUDE.md                  ← 이 파일
├── devlogs/                   ← 개발일지 저장소
│   └── YYYY-MM-DD.md          ← 일자별 개발일지
├── index.html                 ← 통합 메인 페이지
├── s1/                        ← Season 1 (8 에피소드)
│   ├── index.html
│   └── ep001~ep008.html
├── s2/                        ← Season 2 (7 에피소드 + epilogue + final)
│   ├── index.html
│   └── ep001~ep007.html, epilogue.html, final.html
├── s3/                        ← Season 3 (10 에피소드 + prologue + interlude)
│   ├── index.html
│   └── prologue.html, ep001~ep010.html, interlude.html
├── developer_park_S1/         ← 원본 백업 (S1)
├── developer_park_S2/         ← 원본 백업 (S2)
└── developer_park_S3/         ← 원본 백업 (S3)

developer_park_repo/           ← Git 저장소 (../developer_park_repo/)
├── .git/
├── index.html
├── s1/ s2/ s3/                ← 위와 동일 구조
└── devlogs/
```

## 3. 기술 스택

- 순수 HTML/CSS (프레임워크 없음)
- S1: 밝은 톤 (베이지 #f5f0e8 + 빨강 #c0392b), JS 없음
- S2: 다크 모드 (#050508 + 금색 #eab308), JS 없음
- S3: 딥다크 (#04050a + 호박색 #e8a83a), IntersectionObserver JS
- 폰트: Noto Serif KR, JetBrains Mono / DM Mono, Syne, Noto Sans KR
- 네비게이션: 상단 시리즈 바 (고정) + 하단 에피소드 바 (고정)

## 4. 민감정보 규칙

- **실명**: 반드시 마스킹 (박*석, 최*현, 조*진 등 중간 글자 *)
- **이메일**: m****@*****.co.kr 형태
- **금융정보**: 금액, 은행명 등 ** 처리
- **내부 URL**: ERP 등 시스템 주소 *** 처리
- 새 에피소드 추가 시에도 이 규칙 적용 필수

## 5. 개발일지 의무 작성 규칙 (최우선)

### 반드시 지켜야 할 규칙
**모든 세션 종료 시 (대화가 끝나기 전) 개발일지를 의무적으로 작성합니다.**

### 개발일지 저장 위치
- 원본: `개발자 박대표 시리즈/devlogs/YYYY-MM-DD.md`
- Git: `developer_park_repo/devlogs/YYYY-MM-DD.md`
- 같은 날 여러 세션이면: `YYYY-MM-DD_02.md`, `YYYY-MM-DD_03.md`

### 개발일지 필수 포함 항목

```markdown
# 개발일지 — YYYY-MM-DD

## 세션 요약
- 시작 시각 (추정): HH:MM
- 주요 작업: [한 줄 요약]

## 수행한 작업 목록
1. [작업1]: 상세 내용
2. [작업2]: 상세 내용
...

## 변경된 파일
- `파일경로` — 변경 내용 요약

## 발견된 이슈 / 미해결 사항
- [ ] 이슈1
- [ ] 이슈2

## 다음 세션에서 해야 할 작업
- [ ] TODO1
- [ ] TODO2

## Git 커밋 이력
- `커밋해시` — 커밋 메시지

## 참고 사항 / 의사결정 기록
- 결정 사항과 그 이유
```

### 개발일지 작성 타이밍
- 사용자가 "끝", "종료", "마무리" 등을 말할 때
- 대화가 자연스럽게 마무리될 때
- 큰 작업 단위가 완료될 때
- **작성하지 않으면 안 됩니다. 잊지 마세요.**

## 6. 세션 시작 시 체크리스트

새 세션이 시작되면 반드시 다음을 수행:

1. **이 CLAUDE.md 읽기** (자동)
2. **메모리 파일 확인**: `C:\Users\moons\.claude\projects\c--Users-moons-Downloads------------\memory\MEMORY.md`
3. **최근 개발일지 확인**: `devlogs/` 폴더에서 가장 최근 파일 읽기
4. **미해결 이슈 확인**: 최근 개발일지의 "미해결 사항" 및 "다음 세션 TODO" 확인
5. **Git 상태 확인**: `developer_park_repo/`에서 `git log --oneline -5`

## 7. Git 워크플로우

- 저장소: `c:/Users/moons/Downloads/developer_park_repo/`
- Remote: `origin` → `https://github.com/moonsukpark92/developer_park.git`
- Branch: `main`
- 작업 후 반드시 원본 폴더(`개발자 박대표 시리즈/s1,s2,s3/`)에도 동기화
- 커밋 메시지: 한국어 또는 영문, Co-Authored-By 포함

## 8. 검토 기준 (에피소드 수정 시)

- 맞춤법/띄어쓰기 한국어 표준 준수
- 구어체 문체는 작가 의도로 존중
- 민감정보 마스킹 필수
- CSS 색상값에 언더스코어(_) 사용 금지
- HTML 속성 중복 방지 (class 2번 선언 등)
- ㈜ 표기: 반드시 ㈜ (&#x321C;) 사용, &#x338E;(㎎) 사용 금지
