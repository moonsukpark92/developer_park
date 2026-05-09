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

- **박문석** (CEO/작가): 마스킹 안 함 — 원래 이름 그대로 존치
- **직원 실명**: 홍길동 → 홍*동 (중간 글자 * 처리. 최*현, 조*진, 임*영, 정*윤, 한*주, 조*범, 신*혜, 허*민, 이*우, 서*표, 오*벡)
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

## 8. 자동 처리 워크플로우 (사용자 확인 없이 진행)

새 에피소드 추가, 수정, 배포 시 다음을 묻지 않고 자동 처리:

### A. 콘텐츠 정제
- 민감정보 마스킹 (박문석 존치, 직원만 홍*동 형태)
- (주)데코페이브 통일 (데코페이브㈜ 금지)
- 맥락 점검: footer "다음 에피소드" 링크, 시간 순서, 명칭 일관성
- 맞춤법 (명백한 오타만, 구어체 존중) + HTML 무결성

### B. 시스템 통합
- 파일명 표준화 (ep0NN, prologue, interlude, epilogue*)
- 시리즈 네비 + 하단 에피소드 네비 (**div 사용** — nav 태그는 CSS 충돌)
- body padding (top:40px, bottom:60px)
- body::before z-index:-1 (S3 콘텐츠 가림 방지)
- blog-features 마운트 추가
- 기존 에피소드 모두의 네비에 새 에피소드 링크 추가
- 시즌/메인 인덱스 카드 + 통계 갱신

### C. 배포
- 원본 폴더 동기화 → Git commit (한국어) → Push
- 1~2분 대기 후 WebFetch로 실접속 검증
- 문제 발견 시 자동 수정 + 재푸시

### D. 세션 종료 시
- `devlogs/YYYY-MM-DD.md` 자동 작성
- 메모리 갱신 (outdated 항목)

## 9. 검수 자동 적용

이전 검토에서 발견된 사항은 **다음 작업 시 자동 반영**.
사용자에게 "진행할까요?" 묻지 않음.

## 10. 시간 경제성

- 묻지 말고 처리 (정책 있는 건)
- 병렬 실행 (독립 작업은 한 메시지에 동시)
- 일괄 처리 (sed/Python 스크립트)
- 간결한 보고 (표/리스트, 결과 위주)
- "개떡같이 말해도 찰떡같이 알아먹는다"

## 11. 절대 금지

- CSS 색상값에 언더스코어(_) 사용 금지
- HTML 속성 중복 (class 2번 선언 등) 금지
- ㈜ 인코딩: ㈜ 사용, &#x338E;(㎎) 사용 금지
- 박문석 마스킹 금지 (CEO/작가는 그대로)
