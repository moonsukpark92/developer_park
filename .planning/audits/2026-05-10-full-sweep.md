# 35편 전수 1차 점검 — 2026-05-10

> Phase 1 (Quality Automation) Task P0-7 산출물.
> `tools/lint-sensitive.sh`, `tools/lint-company.sh`, `tools/lint-html.sh`를
> 35편 전체에 1차 실행한 결과 + 메타데이터 수동 점검 표.

## 요약

| 항목                  | 결과                              |
| --------------------- | --------------------------------- |
| 총 검사 파일          | 35편 (S1: 8, S2: 9, S3: 18) + 4 index |
| **lint-sensitive**    | **PASS** (위반 0건)               |
| **lint-company**      | **FAIL (4건)** — 콘텐츠 수정 필요 |
| **lint-html**         | **PASS** (CSS/class 위반 0건)     |
| 메타데이터(title/charset) | 35/35 정상                    |
| 메타데이터(상단 nav)  | S1·S2 정상 / S3 18편은 패턴 불일치(휴리스틱) |
| 메타데이터(하단 nav)  | 휴리스틱 미검출 — 패턴 보강 후 재점검 필요 |

자동 안전망(pre-push hook)이 이미 작동하므로, 위 4건의 회사명 인코딩 위반이
**고쳐지기 전까지 push가 차단된다.** 이는 의도된 동작이며 안전망 가치 증명.

---

## lint-sensitive 결과

```
[lint-sensitive] 검사 시작: s1/ s2/ s3/ index.html
[lint-sensitive] OK
exit=0
```

직원 실명, 마스킹되지 않은 이메일, 내부 시스템 URL(j3.jtranet, decoceo.gabia, decopave.taskworld), 은행+계좌 패턴 — **현재 35편에는 모두 마스킹 처리됨.**

---

## lint-company 결과

```
[lint-company] 검사 시작: s1/ s2/ s3/ index.html

[lint-company] FAIL: ㈜ 자리에 잘못된 HTML 엔티티 사용
  &#x338E;는 '㎎'(밀리그램), &#xAC8C;는 '게'입니다.
  올바른 표기: ㈜ 또는 &#x321C;
s3/ep008.html:336:  <div class="footer-line">Decopave Co., Ltd. · 데코페이브&#xAC8C; · 2026</div>
s3/ep009.html:286:  <div class="footer-line">Decopave Co., Ltd. &middot; 데코페이브&#x338E; &middot; 2026</div>
s3/ep010.html:445:  <div class="footer-line">Decopave Co., Ltd. &middot; 데코페이브&#x338E; &middot; 2026</div>

[lint-company] FAIL: 회사명 변종 발견
  '데코페이브㈜' 또는 '(주)데코페이브'로 통일하세요.
index.html:344:  <div class="footer-text">Decopave Co., Ltd. · 데코페이브 주식회사 · 2025–2026</div>
exit=1
```

### 발견된 4건 (즉시 수정 대상)

| #   | 파일             | 줄  | 잘못                  | 수정안                      |
| --- | ---------------- | --- | --------------------- | --------------------------- |
| 1   | s3/ep008.html    | 336 | `데코페이브&#xAC8C;` (게) | `데코페이브㈜`              |
| 2   | s3/ep009.html    | 286 | `데코페이브&#x338E;` (㎎) | `데코페이브㈜`              |
| 3   | s3/ep010.html    | 445 | `데코페이브&#x338E;` (㎎) | `데코페이브㈜`              |
| 4   | index.html       | 344 | `데코페이브 주식회사` | `데코페이브㈜`              |

→ **콘텐츠 변경**이라 본 phase에서 자동 수정하지 않음(deviation Rule 1 보류).
   별도 콘텐츠 수정 phase에서 해결 후 push 가능 상태로 만든다.

---

## lint-html 결과

```
[lint-html] 검사 시작: s1/ s2/ s3/ index.html
[lint-html] OK
exit=0
```

CSS 색상값 언더스코어, 같은 태그 내 class 중복, UTF-8 인코딩 깨짐 시그니처
(â€/ï¿½/U+FFFD) — **현재 35편 통과.** 빈 style="" 경고도 없음.

> 메모리 인덱스에 기록된 "렌더링 버그 14건"은 lint 패턴 3종에 해당하지 않는
> 다른 카테고리(레이아웃/반응형/폰트 가중치 등)일 가능성. P0-5 메모리 갱신
> 시 별도 분류한다.

---

## 수동 점검 결과 (편별 메타데이터)

자동 추출 (1=Y, 0=N). nav 패턴은 클래스명 휴리스틱이므로 미검출(N)이라도
실제로는 다른 클래스명을 쓰고 있을 가능성 큼. **재점검 필요.**

| 파일                  | title | charset | 상단 nav | 하단 nav |
| --------------------- | ----- | ------- | -------- | -------- |
| s1/ep001.html         | Y     | Y       | Y        | N        |
| s1/ep002.html         | Y     | Y       | Y        | N        |
| s1/ep003.html         | Y     | Y       | Y        | N        |
| s1/ep004.html         | Y     | Y       | Y        | N        |
| s1/ep005.html         | Y     | Y       | Y        | N        |
| s1/ep006.html         | Y     | Y       | Y        | N        |
| s1/ep007.html         | Y     | Y       | Y        | N        |
| s1/ep008.html         | Y     | Y       | Y        | N        |
| s1/index.html         | Y     | Y       | Y        | N        |
| s2/ep001.html         | Y     | Y       | Y        | N        |
| s2/ep002.html         | Y     | Y       | Y        | N        |
| s2/ep003.html         | Y     | Y       | Y        | N        |
| s2/ep004.html         | Y     | Y       | Y        | N        |
| s2/ep005.html         | Y     | Y       | Y        | N        |
| s2/ep006.html         | Y     | Y       | Y        | N        |
| s2/ep007.html         | Y     | Y       | Y        | N        |
| s2/epilogue.html      | Y     | Y       | Y        | N        |
| s2/final.html         | Y     | Y       | Y        | N        |
| s2/index.html         | Y     | Y       | Y        | N        |
| s3/prologue.html      | Y     | Y       | N        | N        |
| s3/ep001.html         | Y     | Y       | N        | N        |
| s3/ep002.html         | Y     | Y       | N        | N        |
| s3/ep003.html         | Y     | Y       | N        | N        |
| s3/ep004.html         | Y     | Y       | N        | N        |
| s3/ep005.html         | Y     | Y       | N        | N        |
| s3/ep006.html         | Y     | Y       | N        | N        |
| s3/ep007.html         | Y     | Y       | N        | N        |
| s3/ep008.html         | Y     | Y       | N        | N        |
| s3/ep009.html         | Y     | Y       | N        | N        |
| s3/ep010.html         | Y     | Y       | N        | N        |
| s3/ep011.html         | Y     | Y       | N        | N        |
| s3/ep012.html         | Y     | Y       | N        | N        |
| s3/ep013.html         | Y     | Y       | N        | N        |
| s3/ep014.html         | Y     | Y       | N        | N        |
| s3/ep015.html         | Y     | Y       | N        | N        |
| s3/epilogue2.html     | Y     | Y       | N        | N        |
| s3/epilogue2_2.html   | Y     | Y       | N        | N        |
| s3/interlude.html     | Y     | Y       | N        | N        |
| s3/index.html         | Y     | Y       | Y        | N        |
| index.html            | Y     | Y       | N        | N        |

### 메타데이터 관찰

- **title / charset:** 35편 모두 정상.
- **상단 nav:** S1·S2는 `series-nav`/`series-bar` 류 클래스를 사용 → 검출됨.
  S3는 다른 클래스명(예: 시즌3 고유 다크 디자인 — 사용자 정의 클래스)을 사용해
  휴리스틱이 N으로 출력. **이는 lint 결함이 아니라 표 휴리스틱 한계.**
- **하단 nav:** 35편 모두 휴리스틱이 N — 실제로는 episode-bar 류와 다른 이름일
  가능성. 추후 lint를 nav 누락 검사로 확장하려면 PROJECT_IDENTITY.md에 클래스
  명세를 고정해야 한다 (별도 task 백로그).

---

## 카테고리별 이슈

### A. 자동 검출 가능 — lint로 잡힘 (4건)

위 lint-company FAIL 4건. pre-push hook이 이를 push 단계에서 차단함.

### B. 수동 검수 필요 — lint로 잡히지 않음

**(B1) 메모리 인덱스 기록의 "렌더링 버그 14건":**
- 본 phase 1차 lint(언더스코어/class 중복/인코딩 깨짐) 3종으로는 검출되지 않음.
- 추정 카테고리: 반응형 미디어 쿼리 누락, 폰트 가중치 불일치, 다크모드 색 대비,
  IntersectionObserver 미작동 케이스 등.
- 별도 phase에서 시각적 점검(브라우저 DevTools) + 분류 후 처리.

**(B2) 메모리 인덱스 기록의 "맞춤법 6건":**
- 현재 lint는 한국어 맞춤법 검사 미포함.
- 별도 도구(예: hanspell, kospell) 또는 수동 검수 phase 필요.

**(B3) 콘텐츠 톤 일관성:**
- 시즌별 화자/문체 차이는 의도된 것 (S1 회고록, S2 다크 에세이, S3 본격 르포).
- 검수 대상 아님.

---

## 우선순위

### 1. (즉시) — pre-push 차단을 풀기 위해 필수

콘텐츠 수정 phase에서 처리:
- s3/ep008.html L336 `&#xAC8C;` → `㈜`
- s3/ep009.html L286 `&#x338E;` → `㈜`
- s3/ep010.html L445 `&#x338E;` → `㈜`
- index.html L344 `데코페이브 주식회사` → `데코페이브㈜`

### 2. (다음 phase)

- 메모리 기록의 렌더링 버그 14건 시각적 분류 + 수정
- 맞춤법 6건 검수
- nav 클래스명 명세 고정 → lint-html에 nav 일관성 검사 추가

### 3. (백로그)

- 자동 맞춤법 검사 도구 평가
- HTML5 validator 통합 (W3C nu validator CLI)
- 이미지 alt 누락 lint
- 외부 링크 dead-link checker

---

## 참고: 안전망 작동 증거

본 audit 작성 시점 기준:
- `tools/run-all-lints.sh` 실행 시 lint-company가 exit 1 → 전체 실패.
- `.git/hooks/pre-push`가 `tools/run-all-lints.sh`를 호출 → 위 4건이 수정되기 전까지 `git push` **차단됨.**
- `tools/install-hooks.sh`로 다른 PC에서도 동일 안전망 1회 설치로 복원 가능.
