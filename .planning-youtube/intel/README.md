# 유튜브 트랙 — Intel (지식 베이스)

**단일 진실 원본:** `c:/Users/moons/Downloads/개발자 박대표 시리즈/marketing/`

> intel은 별도 작성하지 않고 **marketing/ 11개 문서를 그대로 인용**한다.
> 새로 발견한 사실은 marketing/에 직접 추가하고 여기 인덱스에만 반영.

---

## 1. 헌법·전략 레이어

| 영역 | 원본 | 핵심 |
|------|------|------|
| **헌법** | [`marketing/00_philosophy.md`](../../../개발자%20박대표%20시리즈/marketing/00_philosophy.md) | 5계명 + §6 정체성 보존 (얼굴 비노출, 음성 합성 OK) |
| **자산 진단** | `marketing/01_asset_audit.md` | 37편 콘텐츠 분류 + 시즌 강·약점 |
| **시장 조사** | `marketing/02_market_research.md` | GitHub awesome 리포 + 2026 YouTube 플레이북 + 한국 벤치마크 |
| **포지셔닝** | `marketing/03_positioning.md` | USP, 이중 타겟, 4 Pillar 메시지, 슬로건 |
| **채널 전략** | `marketing/04_channel_strategy.md` | 5가지 영상 포맷, 발행 빈도, 멀티플랫폼, 도구 스택 |
| **로드맵** | `marketing/05_launch_roadmap.md` | 0~180일 Phase 1·2·3 + KPI + D7 체크리스트 |

## 2. 운영·자동화 레이어

| 영역 | 원본 | 핵심 |
|------|------|------|
| **자동화 청사진** | `marketing/06_automation_blueprint.md` | n8n 파이프라인, Phase A~D 빌드 순서, 월 16만원 풀스택 |
| **음성 자산 진단** | `marketing/07_voice_assets.md` | 13개 m4a 156분, ElevenLabs PVC 5단계 전처리 |
| **녹음 셋업** | `marketing/08_recording_setup.md` | OBS Studio 32.1.2 5개 씬 |
| **음성 클린업** | `marketing/09_audio_cleanup.md` | ffmpeg afftdn+loudnorm 1줄 (36분→26초) |
| **영상 편집기** | `marketing/10_video_editor.md` | Descript 채택, DaVinci 거부, Remotion+Descript 역할 분담 |
| **소스 마스터** | `marketing/99_sources.md` | 모든 인용 트레이서빌리티 |

## 3. 제작 자산 레이어

| 영역 | 원본 | 상태 |
|------|------|------|
| **음성 녹음** | `voice_rec/` | 13개 m4a, 156분 (모두 AAC 128k 48kHz mono — PVC 정중앙 분량) |
| **녹음 stage1** | `voice_rec/stage1_wav/` | 변환 진행 중 (예상) |
| **클린 데모** | `voice_rec/stage3_clean_demo/` | ffmpeg 검증된 26초 처리 출력 |

## 4. 도구 인프라 (설치 완료)

| 도구 | 버전 | 용도 |
|------|------|------|
| Figma | 126.3.12 | 썸네일·아바타 시각 디자인 |
| FFmpeg | 8.1.1 | 음성 클린업 1줄 파이프라인 |
| OBS Studio | 32.1.2 | 화면 녹화 (5개 씬 셋업 예정) |
| Audacity | 3.7.7 | 음성 편집 백업 |

## 5. 도구 인프라 (가입·결제 미완)

| 도구 | 월 비용 | 용도 |
|------|---------|------|
| ElevenLabs Creator | $22 | 박문석 음성 PVC 클로닝 |
| Descript Creator | $24 | 영상 편집 (Underlord 활용) |
| Canva Pro | $13 | 썸네일·배너 |
| Stibee | Free→$ | 뉴스레터 |
| n8n self-host | $0 | 자동 분배 파이프라인 |
| Midjourney/DALL-E | $10~ | 박대표·문실장 일러스트 아바타 |

**합계 예상:** 월 $89~ (≒ 12만원)

## 6. Intel 갱신 규칙

1. 새 사실 발견 → marketing/ 에 직접 추가 (이 README는 인덱스만)
2. 새 카테고리 발견 → marketing/에 신규 번호 문서 (예: 11_xxx.md)
3. 외부 도구·서비스 변경 → 04 또는 06 갱신
4. 헌법 변경 → 00 + PROJECT_IDENTITY.md 동시 갱신 + 모든 phase PLAN.md 영향 평가
