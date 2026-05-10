---
created: 2026-05-10
authority: 박대표 직접 지시
status: LOCKED — 변경 시 박대표 명시 동의 필요
---

# 세션 영역 분리 규정

> developer_park 프로젝트는 **여러 Claude Code 세션이 병렬 운영**된다.
> 본 문서는 각 세션의 책임 영역을 명문화하여 영역 침범·중복 작업·산출물 충돌을 방지한다.
> 모든 세션은 작업 시작 전 본 문서를 확인할 의무가 있다.

## 0. 명칭 동의어

본 문서는 두 표현 체계를 모두 인정한다 — 같은 세션을 가리킨다.

| 박대표 표현 | 메모리 표준 명칭 | GSD 워크스페이스 |
| --- | --- | --- |
| **메인 관리 세션** | **블로그 트랙** | `.planning/` |
| **콘텐츠 세션** | **유튜브 트랙** | `.planning-youtube/` |

이하 본문에서는 박대표 표현(메인 관리 / 콘텐츠)을 1차 표기로 사용하되, 어느 표현으로 호명되어도 동일하게 적용된다.

## 1. 세션 구분

### A. 메인 관리 세션 (Meta / Infra) ≡ 블로그 트랙
**역할**: 프로젝트 전체 메타·인프라·다중 세션 조율 + 블로그(s1/s2/s3) 운영

**책임 영역**:
- `CLAUDE.md` (이 파일 포함 모든 CLAUDE.md)
- `MEMORY.md` 및 `memory/` 전체
- `SCOPE_BOUNDARY.md` (이 문서)
- `devlogs/` 작성 및 `developer_park_repo/devlogs/` 동기화
- `.gitignore` 안전망 관리 (양 리포 모두)
- `tools/` 자동 검증 스크립트
- `.planning/` GSD 워크플로우 (있는 경우)
- 시즌 1~3 기존 콘텐츠 (`s1/`, `s2/`, `s3/`, `index.html`) 운영·검수
- 시스템 도구 설치 (winget, pip, npm 전역 등) — 단 콘텐츠 세션에 사전 통지
- HANDOFF / 세션 간 인계 메커니즘
- Git 전략 (커밋·브랜치·푸시 정책)
- 보안·권한·민감정보 마스킹 정책 운영

**금지 영역**:
- `marketing/` 13개 문서 작성·수정 (단 인용·참조는 OK)
- `voice_rec/` 음성 파일 처리·전사·합성
- 트레일러·롱폼·쇼츠 스크립트·영상 작업
- ElevenLabs / Midjourney / Descript / YouTube 채널 운영

### B. 콘텐츠 세션 (YouTube Launch)
**역할**: 유튜브 채널 런칭 및 콘텐츠 제작 운영

**책임 영역**:
- `marketing/` 13개 문서 (00_INDEX ~ 99_sources) 작성·갱신·진화
- `voice_rec/` 음성 자산 전 처리 (Stage P1~P5 전체)
- ElevenLabs PVC 학습·검증·운영
- Midjourney/DALL-E 아바타 시드·반복
- Descript / Remotion 영상 합성·조립
- YouTube 채널 개설·운영·발행
- 트레일러·롱폼·쇼츠 스크립트 작성
- 발행 전 헌법 5계명 체크리스트 운영
- LinkedIn / Stibee / SNS 운영
- 자동화 Phase A~D 구현·검증

**금지 영역**:
- 시즌 1~3 기존 에피소드 본문 수정 (필요 시 메인에 요청)
- `.gitignore` 직접 수정 (필요 시 메인에 요청)
- `CLAUDE.md` / `MEMORY.md` 직접 수정
- 시스템 도구 전역 설치 (필요 시 메인에 요청)

## 2. 경계 모호 영역 — 룰

| 영역 | 책임 | 협력 방식 |
|------|------|----------|
| `.gitignore` 보강 | 메인 (안전망 디폴트) | 콘텐츠 세션이 항목 제안 → 메인이 적용 |
| `devlogs/` 작성 | 양쪽 모두 작성 가능 | 작성자 명시(헤더에 "세션: 메인" 또는 "세션: 콘텐츠"). 같은 날 충돌 시 `_meta.md` / `_content.md` 분기 |
| `MEMORY.md` 갱신 | 메인 단독 | 콘텐츠 세션이 사실 변경 통지 → 메인이 반영 |
| 시스템 도구 설치 (winget/pip/npm 전역) | 메인 단독 | 콘텐츠 세션 요청 시 메인이 설치 후 NOTE 남김 |
| `voice_rec/` 폴더 자체 (안전망·디렉토리 정책) | 메인 (정책) + 콘텐츠 (내용) | 메인은 `.gitignore`만, 내부 파일 처리는 콘텐츠 |
| HANDOFF.json | 양쪽 각각 자기 영역만 | 메인 = `.planning/HANDOFF.json` / 콘텐츠 = `marketing/HANDOFF.json` |

## 3. 영역 침범 시 절차

영역을 침범한 산출물이 발견되면:
1. **즉시 작업 중단**
2. 산출물에 `_NOTE.md` 첨부 (출처·사양·인계 내용)
3. 해당 영역 세션이 결정할 후속 항목 명시
4. 환경 전역 변경(설치 등) 발생 시 본 문서 또는 NOTE에 기록
5. 가능하면 산출물 보존 (재사용 가치) — 폐기는 영역 세션 결정

## 4. 본 문서 작성 계기

2026-05-10 — 메인 관리 세션이 직전 콘텐츠 세션의 HANDOFF (`marketing/HANDOFF.json`)에서 `/gsd:resume-work` 후 옵션 B (PVC 학습) 진입을 자동 선택하여:
- voice_rec/stage1_wav/ 12개 WAV 생성 (788MB)
- openai-whisper 전역 설치
완료한 시점에서 박대표가 영역 분리를 지시함.

해당 산출물은 `voice_rec/stage1_wav/_NOTE.md`로 인계되어 콘텐츠 세션이 결정 가능 상태.

## 5. 다중 세션 발견·동기화

각 세션은 시작 시:
- 본 문서 자동 로딩 (CLAUDE.md에서 reference)
- 자기 영역의 HANDOFF.json 확인 (있으면 resume)
- 다른 영역의 HANDOFF.json은 **읽기만** 하여 컨텍스트 파악, 작업 진입 금지
- 영역 외 작업 요청 받으면 → 박대표에게 적절한 세션 전환 권유
