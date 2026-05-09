/* 개발자 박대표 — 블로그 기능 (구독 + 댓글 + 분석)
 * 한 곳에서 설정 후 모든 페이지에 자동 적용
 *
 * 설정 후 해야 할 일:
 *   1. Buttondown 가입 → username 입력
 *   2. Giscus 설정 (https://giscus.app) → repoId, categoryId 입력
 *   3. GoatCounter 가입 → code 입력
 */

const CONFIG = {
  // 1. 이메일 구독 (https://buttondown.com)
  buttondown: 'YOUR_BUTTONDOWN_USERNAME',  // 예: 'moonsukpark'

  // 2. 댓글 (https://giscus.app)
  giscus: {
    repo: 'moonsukpark92/developer_park',
    repoId: 'YOUR_GISCUS_REPO_ID',          // giscus.app에서 확인
    category: 'General',
    categoryId: 'YOUR_GISCUS_CATEGORY_ID',  // giscus.app에서 확인
  },

  // 3. 방문자 통계 (https://www.goatcounter.com)
  goatcounter: 'YOUR_GOATCOUNTER_CODE',    // 예: 'developerpark'
};

(function () {
  const mount = document.getElementById('blog-features-mount');
  if (!mount) return;

  const isConfigured = (val) => val && !val.startsWith('YOUR_');

  // ─── HTML 렌더 ───
  mount.innerHTML = `
    <div style="background:#0a0b12;border-top:1px solid rgba(232,168,58,.15);padding:60px 24px;font-family:'Noto Sans KR','Noto Serif KR',sans-serif;color:#f0e8d0;margin-top:60px;">
      <div style="max-width:680px;margin:0 auto;">

        <!-- SUBSCRIBE -->
        <div style="text-align:center;margin-bottom:60px;">
          <div style="font-family:'JetBrains Mono','DM Mono',monospace;font-size:.65rem;letter-spacing:3px;color:#e8a83a;margin-bottom:12px;">SUBSCRIBE</div>
          <h3 style="font-family:'Noto Serif KR',serif;font-size:1.4rem;font-weight:700;margin-bottom:8px;color:#f0e8d0;">새 에피소드 구독하기</h3>
          <p style="font-size:.9rem;color:rgba(240,232,208,.55);margin-bottom:24px;line-height:1.7;">새 글이 발행되면 이메일로 알려드립니다.<br>광고 없음. 언제든 해지 가능.</p>
          ${isConfigured(CONFIG.buttondown) ? `
            <form action="https://buttondown.com/api/emails/embed-subscribe/${CONFIG.buttondown}" method="post" target="popupwindow" onsubmit="window.open('https://buttondown.com/${CONFIG.buttondown}', 'popupwindow')" style="display:flex;gap:8px;max-width:400px;margin:0 auto;flex-wrap:wrap;">
              <input type="email" name="email" placeholder="your@email.com" required style="flex:1;min-width:200px;padding:12px 16px;background:rgba(255,255,255,.05);border:1px solid rgba(232,168,58,.3);color:#f0e8d0;font-family:inherit;font-size:.9rem;border-radius:4px;outline:none;">
              <button type="submit" style="padding:12px 24px;background:#e8a83a;color:#04050a;border:none;font-family:'JetBrains Mono',monospace;font-size:.7rem;letter-spacing:2px;font-weight:700;cursor:pointer;border-radius:4px;">구독</button>
            </form>
          ` : `
            <div style="padding:16px 20px;background:rgba(232,168,58,.05);border:1px dashed rgba(232,168,58,.3);border-radius:4px;font-size:.8rem;color:rgba(240,232,208,.5);">
              구독 기능 설정 중입니다 — 곧 오픈합니다.
            </div>
          `}
        </div>

        <!-- COMMENTS -->
        <div style="border-top:1px solid rgba(232,168,58,.1);padding-top:60px;">
          <div style="font-family:'JetBrains Mono','DM Mono',monospace;font-size:.65rem;letter-spacing:3px;color:#e8a83a;margin-bottom:12px;text-align:center;">COMMENTS</div>
          <h3 style="font-family:'Noto Serif KR',serif;font-size:1.4rem;font-weight:700;margin-bottom:24px;text-align:center;color:#f0e8d0;">댓글</h3>
          <div id="giscus-mount"></div>
          ${!isConfigured(CONFIG.giscus.repoId) ? `
            <div style="padding:16px 20px;background:rgba(232,168,58,.05);border:1px dashed rgba(232,168,58,.3);border-radius:4px;font-size:.8rem;color:rgba(240,232,208,.5);text-align:center;">
              댓글 기능 설정 중입니다 — 곧 오픈합니다.
            </div>
          ` : ''}
        </div>

      </div>
    </div>
  `;

  // ─── Giscus 댓글 로드 ───
  if (isConfigured(CONFIG.giscus.repoId) && isConfigured(CONFIG.giscus.categoryId)) {
    const giscusMount = document.getElementById('giscus-mount');
    if (giscusMount) {
      const s = document.createElement('script');
      s.src = 'https://giscus.app/client.js';
      s.async = true;
      s.crossOrigin = 'anonymous';
      const attrs = {
        'data-repo': CONFIG.giscus.repo,
        'data-repo-id': CONFIG.giscus.repoId,
        'data-category': CONFIG.giscus.category,
        'data-category-id': CONFIG.giscus.categoryId,
        'data-mapping': 'pathname',
        'data-strict': '0',
        'data-reactions-enabled': '1',
        'data-emit-metadata': '0',
        'data-input-position': 'bottom',
        'data-theme': 'dark_dimmed',
        'data-lang': 'ko',
        'data-loading': 'lazy',
      };
      Object.entries(attrs).forEach(([k, v]) => s.setAttribute(k, v));
      giscusMount.appendChild(s);
    }
  }

  // ─── GoatCounter 방문 통계 ───
  if (isConfigured(CONFIG.goatcounter)) {
    const gc = document.createElement('script');
    gc.async = true;
    gc.setAttribute('data-goatcounter', `https://${CONFIG.goatcounter}.goatcounter.com/count`);
    gc.src = 'https://gc.zgo.at/count.js';
    document.head.appendChild(gc);
  }
})();
