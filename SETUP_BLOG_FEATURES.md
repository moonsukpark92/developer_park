# 블로그 기능 설정 가이드

이 사이트의 댓글 / 이메일 구독 / 방문자 통계는 모두 외부 무료 서비스를 사용합니다.
설정 후 `assets/blog-features.js` 파일의 `CONFIG` 객체만 수정하면 모든 페이지에 즉시 반영됩니다.

---

## 1. 이메일 구독 — Buttondown

**용도:** 새 에피소드 발행 시 구독자들에게 자동 메일 발송

### 설정 단계

1. https://buttondown.com 접속 → 무료 가입 (100명까지 무료)
2. 가입 시 username 결정 (예: `moonsukpark`)
3. `assets/blog-features.js` 열기
4. `buttondown` 값을 본인 username으로 변경:
   ```js
   buttondown: 'moonsukpark',
   ```
5. 새 글 발행 시 Buttondown 대시보드에서 "New email" 작성 후 발송

### 새 에피소드 발행 시 이메일 보내는 법

1. Buttondown 대시보드 → "New email"
2. 제목: `[개발자 박대표] S3 EP012 — 새 에피소드 제목`
3. 본문에 에피소드 링크: `https://moonsukpark92.github.io/developer_park/s3/ep012.html`
4. "Send" 클릭 → 모든 구독자에게 자동 발송

---

## 2. 댓글 — Giscus (GitHub Discussions 기반)

**용도:** 방문자가 각 에피소드에 댓글 남기기. GitHub 계정으로 로그인.

### 설정 단계

#### 단계 A: GitHub 저장소에 Discussions 활성화

1. https://github.com/moonsukpark92/developer_park/settings 접속
2. 좌측 메뉴 "General" → 아래로 스크롤 → "Features" 섹션
3. **Discussions** 체크박스 활성화 → "Set up discussions" 클릭

#### 단계 B: Giscus 앱 설치

1. https://github.com/apps/giscus 접속
2. "Install" → 본인 계정 선택
3. "Only select repositories" 선택 → `developer_park` 선택 → "Install"

#### 단계 C: Giscus 설정값 받기

1. https://giscus.app 접속
2. **Repository** 입력: `moonsukpark92/developer_park`
3. **Page ↔ Discussions Mapping**: `pathname` 선택
4. **Discussion Category**: `General` 선택 (또는 새로 생성한 카테고리)
5. **Features**: "Enable reactions for the main post" 체크
6. **Theme**: `dark_dimmed`
7. 페이지 하단의 `<script>` 태그에서 다음 두 값 복사:
   - `data-repo-id="..."`  → 이 값을 `repoId`에
   - `data-category-id="..."`  → 이 값을 `categoryId`에

#### 단계 D: 설정 적용

`assets/blog-features.js` 의 giscus 부분 수정:
```js
giscus: {
  repo: 'moonsukpark92/developer_park',
  repoId: 'R_kgDOxxxxxxx',          // ← 단계 C에서 복사한 값
  category: 'General',
  categoryId: 'DIC_kwDOxxxxxxx',    // ← 단계 C에서 복사한 값
},
```

---

## 3. 방문자 통계 — GoatCounter

**용도:** 어느 에피소드가 인기있는지, 방문자 수 등 통계

### 설정 단계

1. https://www.goatcounter.com 접속 → 무료 가입
2. 가입 시 사이트 코드 결정 (예: `developerpark`)
3. `assets/blog-features.js` 의 goatcounter 값 변경:
   ```js
   goatcounter: 'developerpark',
   ```
4. https://developerpark.goatcounter.com 에서 통계 확인

---

## 적용 방법

설정 완료 후:

```bash
cd developer_park_repo
git add assets/blog-features.js
git commit -m "feat: 블로그 기능 설정 완료"
git push
```

GitHub Pages는 1-2분 후 자동 반영됩니다.

---

## 현재 상태

| 기능 | 서비스 | 설정 상태 |
|------|--------|----------|
| 이메일 구독 | Buttondown | ⚠️ 가입 필요 |
| 댓글 | Giscus | ⚠️ Discussions 활성화 + 설정 필요 |
| 통계 | GoatCounter | ⚠️ 가입 필요 |

설정 안 된 기능은 페이지에 "곧 오픈" 메시지가 표시됩니다.
