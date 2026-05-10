# GitHub 계정 안전성 점검 — 2026-05-10

> Phase 1 (Quality Automation) Task P0-6 산출물.
> Claude는 본 템플릿만 작성하며, 사용자가 https://github.com/settings/security 에 직접
> 접속하여 각 항목을 확인 후 결과를 채워 넣는다.
>
> **2FA 시드 / 복구코드 / Personal Access Token은 어떤 경우에도 이 파일에 평문으로
> 기록하지 않는다.** 저장 위치만 기록한다.

대상 계정: **moonsukpark92** (https://github.com/moonsukpark92)
저장소: developer_park (Public, GitHub Pages 배포 중)
점검자: 박문석 (CEO/작가)
점검일: 2026-05-10

---

## 1. 2FA(2단계 인증) 활성화

- [ ] 2FA가 활성화되어 있다 (Settings → Password and authentication)
- 사용 중인 방식 (해당 항목 체크):
  - [ ] TOTP 앱 (Authy, Google Authenticator, 1Password 등)
  - [ ] SMS (권장하지 않음 — SIM 스왑 위험)
  - [ ] Security key (YubiKey 등 하드웨어 키)
  - [ ] Passkey

- 메모: ____________________

## 2. 복구코드 (Recovery codes)

- [ ] 복구코드 8개 발급 완료
- [ ] 복구코드를 **GitHub 외부**의 안전한 위치에 저장
- 저장 위치(평문 코드는 적지 말 것 — 위치만):
  - [ ] 1Password / Bitwarden 등 비밀번호 매니저
  - [ ] 종이 출력 후 금고/서랍 보관
  - [ ] 암호화된 USB
  - [ ] 기타: ____________________
- 발급일: 2026-05-10
- 차기 재발급 예정일 (1년 후 권장): 2027-05-10

## 3. Authorized OAuth Apps

- [ ] Settings → Applications → Authorized OAuth Apps 확인
- [ ] 사용하지 않는 앱 권한 제거
- 현재 인가된 앱 수: ____ 개
- 제거한 앱: ____________________

## 4. Personal Access Token (PAT)

- [ ] Settings → Developer settings → Personal access tokens 확인
- [ ] 만료일이 없는(영구) token이 존재하는가?
  - [ ] Yes — 즉시 만료일 설정 또는 재발급
  - [ ] No
- 현재 보유 token 수: ____ 개
- 조치 사항: ____________________

## 5. SSH 키

- [ ] Settings → SSH and GPG keys 확인
- [ ] 사용하지 않는 키 제거
- 현재 등록된 SSH 키 수: ____ 개
- 키별 사용 PC 메모:
  - 키 1: ____________________
  - 키 2: ____________________

## 6. 이메일 주소 / 백업

- 주 이메일: moonsukpark92@gmail.com (GitHub 등록 확인됨)
- [ ] 백업 이메일 추가됨
- 백업 이메일: ____________________
- [ ] 두 이메일 모두 2FA 보호된 메일 계정인가?

## 7. Sign-in 활동 로그

- [ ] Settings → Sessions 확인 — 알 수 없는 활성 세션 없음
- [ ] Settings → Security log 확인 — 최근 14일 의심스러운 로그인 없음
- 의심스러운 활동 발견 여부: [ ] Yes / [ ] No
- 상세: ____________________

## 8. 저장소 보안 설정 (developer_park)

- [ ] Settings → Branches: main 브랜치 보호 규칙
  - [ ] Require pull request before merging (선택 사항 — 1인 운영 시 부담)
  - [ ] Require status checks (CI 도입 시)
- [ ] Settings → Secrets and variables: 노출된 secret 없음
- [ ] Settings → Pages: 배포 소스 main / docs 정상

## 9. Gmail 계정 (연동된 핵심 의존)

> GitHub 복구는 결국 Gmail이 살아있어야 가능. 동일 강도로 점검.

- [ ] moonsukpark92@gmail.com 자체에 2FA 활성
- [ ] Gmail 백업 코드 보관 위치: ____________________
- [ ] 의심스러운 Gmail 로그인 활동 없음

---

## 발견된 위험

(점검 중 발견한 문제를 자유 형식으로 기록)

- 

---

## 조치 결과

| 일자       | 항목                          | 결과 |
| ---------- | ----------------------------- | ---- |
| 2026-05-10 | 2FA 활성화 확인               |      |
| 2026-05-10 | 복구코드 발급                 |      |
| 2026-05-10 | OAuth Apps 정리               |      |
| 2026-05-10 | PAT 만료일 설정               |      |
| 2026-05-10 | SSH key 정리                  |      |
| 2026-05-10 | Sign-in 로그 검토             |      |

---

## 다음 점검 예정일

- **분기 점검:** 2026-08-10
- **연 1회 복구코드 재발급:** 2027-05-10

---

## 완료 신호

본 audit 파일의 위 모든 체크박스가 `[x]`로 채워지면 P0-6 완료.
완료 후 `devlogs/audits/2026-Q2-account-security.md`(분기 사이클용 단축 양식)에
요약 1쪽을 작성하여 분기마다 갱신한다.
