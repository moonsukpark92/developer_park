# 분기 보안 점검 — 2026 Q2

> 분기마다 한 페이지로 갱신. 상세 점검은 `.planning/audits/YYYY-MM-DD-github-account.md`에 두고
> 본 파일은 **요약 + 추세**만 담는다.

대상 자산:
- GitHub: moonsukpark92 (developer_park 외 비공개 저장소 포함)
- Gmail: moonsukpark92@gmail.com
- 회사 메일: office@decopave.co.kr (이폼싸인 등록)
- ERP: j3.jtranet.co.kr (계정 MH1200)
- 텔레그램, Taskworld, 이폼싸인

점검자: 박문석
점검 분기: 2026 Q2 (4월 ~ 6월)
최종 갱신일: ____ -__-__

---

## 빠른 자가진단 (체크하면서 채우기)

### GitHub
- [ ] 2FA 정상 작동 (지난 로그인에 코드 입력함)
- [ ] 복구코드 위치 기억남
- [ ] 미사용 OAuth/Token/SSH 키 0건
- 마지막 상세 점검: `.planning/audits/____-__-__-github-account.md`

### Gmail
- [ ] 2FA 활성
- [ ] 복구 전화번호/이메일 최신
- [ ] 의심 로그인 0건 (최근 90일)

### 회사 메일 (office@decopave.co.kr)
- [ ] 비밀번호 90일 이내 변경
- [ ] 이 메일을 받는 사람이 박문석 1인인지 확인 (공유 위험)

### ERP (j3.jtranet.co.kr)
- [ ] 비밀번호 무차별 대입 보호 (서비스 자체 정책 의존)
- [ ] 자동 로그아웃 시간 설정
- [ ] 외부 노출 계정 ID/PW 평문 저장 위치 점검 (CLAUDE.md에 평문 기록 → 차기 phase에서 환경 변수화 필요)

### 텔레그램
- [ ] Cloud Password (2FA) 활성
- [ ] 활성 세션 검토 (Settings → Devices)

### 이폼싸인
- [ ] API Key 노출 위치 점검 (CLAUDE.md에 평문 기록 → 차기 phase 대응)

---

## 추세 (분기별 비교)

| 지표                       | 2026 Q1 | 2026 Q2 | 변화 |
| -------------------------- | ------- | ------- | ---- |
| GitHub OAuth Apps          | -       |         |      |
| GitHub PAT (영구 만료)     | -       |         |      |
| 등록된 SSH 키              | -       |         |      |
| Gmail 의심 로그인 90일     | -       |         |      |
| 평문 저장된 비밀(검출 건)  | -       |         |      |

---

## 이번 분기 발견 + 조치

(자유 형식)

- 

---

## 다음 분기 (2026 Q3) TODO

- [ ] CLAUDE.md에 평문으로 기록된 자격증명 → 환경변수/시크릿 매니저로 이전
- [ ] ERP 자동 스크립트의 비밀번호 처리 방식 점검
- [ ] 이폼싸인 API Key 노출 위치 정리
- [ ] 분기 점검을 캘린더에 자동 등록 (Google Calendar primary)

---

## 참조

- 상세 점검 양식: `.planning/audits/2026-05-10-github-account.md`
- 안전망 자동화 도구: `tools/lint-sensitive.sh` (회사 자격증명/이메일/내부 URL 누출 차단)
- pre-push hook: `.git/hooks/pre-push`
