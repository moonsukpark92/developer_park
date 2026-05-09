/* 개발자 박대표 — 블로그 기능 (구독 + 댓글 + 분석)
 *
 * 기본 모드: GitHub 자체 기능 (가입 불필요, 즉시 작동)
 *   - 구독: GitHub Watch 버튼
 *   - 댓글: GitHub Issues
 *   - 통계: GitHub Insights (관리자만)
 *
 * 업그레이드 모드: 외부 서비스 (가입 후 활성화)
 *   - 구독: Buttondown (이메일 발송)
 *   - 댓글: Giscus (페이지 내 댓글창)
 *   - 통계: GoatCounter (사이트 내 통계)
 */

const CONFIG = {
  // GitHub 저장소 (기본 모드용 — 항상 작동)
  github: {
    owner: 'moonsukpark92',
    repo: 'developer_park',
  },

  // ─── 업그레이드 모드 (선택, 비워두면 GitHub 모드로 작동) ───

  // 1. 이메일 구독 (https://buttondown.com)
  buttondown: 'YOUR_BUTTONDOWN_USERNAME',

  // 2. 댓글 (https://giscus.app)
  giscus: {
    repoId: 'YOUR_GISCUS_REPO_ID',
    categoryId: 'YOUR_GISCUS_CATEGORY_ID',
  },

  // 3. 방문자 통계 (https://www.goatcounter.com)
  goatcounter: 'YOUR_GOATCOUNTER_CODE',
};

(function () {
  const mount = document.getElementById('blog-features-mount');
  if (!mount) return;

  const isConfigured = (val) => val && !val.startsWith('YOUR_');
  const ghUrl = `https://github.com/${CONFIG.github.owner}/${CONFIG.github.repo}`;
  const pageTitle = document.title || 'Episode';

  // 현재 페이지 정보 (이슈 생성 시 자동 입력용)
  const path = window.location.pathname.split('/').filter(Boolean).pop() || 'index';
  const issueTitle = encodeURIComponent(`💬 ${pageTitle}`);
  const issueBody = encodeURIComponent(`> 페이지: ${window.location.href}\n\n여기에 의견을 적어주세요.`);
  const issueLabels = encodeURIComponent('comments');

  // ─── 구독 섹션 HTML ───
  const subscribeHtml = isConfigured(CONFIG.buttondown) ? `
    <div style="text-align:center;margin-bottom:60px;">
      <div style="font-family:'JetBrains Mono','DM Mono',monospace;font-size:.65rem;letter-spacing:3px;color:#e8a83a;margin-bottom:12px;">SUBSCRIBE</div>
      <h3 style="font-family:'Noto Serif KR',serif;font-size:1.4rem;font-weight:700;margin-bottom:8px;color:#f0e8d0;">새 에피소드 구독하기</h3>
      <p style="font-size:.9rem;color:rgba(240,232,208,.55);margin-bottom:24px;line-height:1.7;">새 글이 발행되면 이메일로 알려드립니다.</p>
      <form action="https://buttondown.com/api/emails/embed-subscribe/${CONFIG.buttondown}" method="post" target="popupwindow" onsubmit="window.open('https://buttondown.com/${CONFIG.buttondown}', 'popupwindow')" style="display:flex;gap:8px;max-width:400px;margin:0 auto;flex-wrap:wrap;">
        <input type="email" name="email" placeholder="your@email.com" required style="flex:1;min-width:200px;padding:12px 16px;background:rgba(255,255,255,.05);border:1px solid rgba(232,168,58,.3);color:#f0e8d0;font-family:inherit;font-size:.9rem;border-radius:4px;outline:none;">
        <button type="submit" style="padding:12px 24px;background:#e8a83a;color:#04050a;border:none;font-family:'JetBrains Mono',monospace;font-size:.7rem;letter-spacing:2px;font-weight:700;cursor:pointer;border-radius:4px;">구독</button>
      </form>
    </div>
  ` : `
    <div style="text-align:center;margin-bottom:60px;">
      <div style="font-family:'JetBrains Mono','DM Mono',monospace;font-size:.65rem;letter-spacing:3px;color:#e8a83a;margin-bottom:12px;">SUBSCRIBE</div>
      <h3 style="font-family:'Noto Serif KR',serif;font-size:1.4rem;font-weight:700;margin-bottom:8px;color:#f0e8d0;">새 에피소드 알림 받기</h3>
      <p style="font-size:.9rem;color:rgba(240,232,208,.55);margin-bottom:24px;line-height:1.7;">GitHub에서 이 저장소를 <strong style="color:#e8a83a;">Watch</strong>하시면<br>새 에피소드가 올라올 때마다 알림이 갑니다.</p>
      <a href="${ghUrl}/subscription" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;gap:10px;padding:14px 28px;background:#e8a83a;color:#04050a;text-decoration:none;font-family:'JetBrains Mono',monospace;font-size:.75rem;letter-spacing:2px;font-weight:700;border-radius:4px;transition:transform .2s ease;" onmouseover="this.style.transform='translateY(-2px)'" onmouseout="this.style.transform='translateY(0)'">
        <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor"><path d="M8 16A1.68 1.68 0 0 1 6.43 15H9.57A1.68 1.68 0 0 1 8 16M14 14H2V13L3 11.91V8.5A4.5 4.5 0 0 1 6.5 4.13V3.5A1.5 1.5 0 0 1 8 2A1.5 1.5 0 0 1 9.5 3.5V4.13A4.5 4.5 0 0 1 13 8.5V11.91L14 13V14Z"/></svg>
        WATCH ON GITHUB
      </a>
      <p style="font-size:.7rem;color:rgba(240,232,208,.3);margin-top:16px;font-family:'JetBrains Mono',monospace;">또는 <a href="https://moonsukpark92.github.io/developer_park/" style="color:rgba(232,168,58,.6);text-decoration:underline;">RSS 피드 구독</a></p>
    </div>
  `;

  // ─── 댓글 섹션 HTML ───
  const commentsHtml = (isConfigured(CONFIG.giscus.repoId) && isConfigured(CONFIG.giscus.categoryId)) ? `
    <div style="border-top:1px solid rgba(232,168,58,.1);padding-top:60px;">
      <div style="font-family:'JetBrains Mono','DM Mono',monospace;font-size:.65rem;letter-spacing:3px;color:#e8a83a;margin-bottom:12px;text-align:center;">COMMENTS</div>
      <h3 style="font-family:'Noto Serif KR',serif;font-size:1.4rem;font-weight:700;margin-bottom:24px;text-align:center;color:#f0e8d0;">댓글</h3>
      <div id="giscus-mount"></div>
    </div>
  ` : `
    <div style="border-top:1px solid rgba(232,168,58,.1);padding-top:60px;text-align:center;">
      <div style="font-family:'JetBrains Mono','DM Mono',monospace;font-size:.65rem;letter-spacing:3px;color:#e8a83a;margin-bottom:12px;">COMMENTS</div>
      <h3 style="font-family:'Noto Serif KR',serif;font-size:1.4rem;font-weight:700;margin-bottom:8px;color:#f0e8d0;">의견을 남겨주세요</h3>
      <p style="font-size:.9rem;color:rgba(240,232,208,.55);margin-bottom:24px;line-height:1.7;">GitHub 계정으로 댓글을 남길 수 있습니다.<br>비회원은 가입(무료, 1분) 후 작성 가능합니다.</p>
      <div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap;">
        <a href="${ghUrl}/issues/new?title=${issueTitle}&body=${issueBody}&labels=${issueLabels}" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;gap:10px;padding:12px 24px;background:rgba(232,168,58,.15);color:#e8a83a;text-decoration:none;font-family:'JetBrains Mono',monospace;font-size:.7rem;letter-spacing:2px;font-weight:700;border:1px solid rgba(232,168,58,.4);border-radius:4px;transition:background .2s ease;" onmouseover="this.style.background='rgba(232,168,58,.25)'" onmouseout="this.style.background='rgba(232,168,58,.15)'">
          <svg width="14" height="14" viewBox="0 0 16 16" fill="currentColor"><path d="M14 1H2C1.45 1 1 1.45 1 2V12C1 12.55 1.45 13 2 13H4V16L7 13H14C14.55 13 15 12.55 15 12V2C15 1.45 14.55 1 14 1Z"/></svg>
          댓글 작성하기
        </a>
        <a href="${ghUrl}/issues?q=is%3Aissue+label%3Acomments" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;gap:10px;padding:12px 24px;background:transparent;color:rgba(240,232,208,.7);text-decoration:none;font-family:'JetBrains Mono',monospace;font-size:.7rem;letter-spacing:2px;font-weight:700;border:1px solid rgba(240,232,208,.15);border-radius:4px;transition:border-color .2s ease;" onmouseover="this.style.borderColor='rgba(240,232,208,.4)'" onmouseout="this.style.borderColor='rgba(240,232,208,.15)'">
          모든 댓글 보기 →
        </a>
      </div>
    </div>
  `;

  // ─── 전체 렌더 ───
  mount.innerHTML = `
    <div style="background:#0a0b12;border-top:1px solid rgba(232,168,58,.15);padding:60px 24px;font-family:'Noto Sans KR','Noto Serif KR',sans-serif;color:#f0e8d0;margin-top:60px;">
      <div style="max-width:680px;margin:0 auto;">
        ${subscribeHtml}
        ${commentsHtml}
      </div>
    </div>
  `;

  // ─── Giscus 댓글 로드 (설정된 경우) ───
  if (isConfigured(CONFIG.giscus.repoId) && isConfigured(CONFIG.giscus.categoryId)) {
    const giscusMount = document.getElementById('giscus-mount');
    if (giscusMount) {
      const s = document.createElement('script');
      s.src = 'https://giscus.app/client.js';
      s.async = true;
      s.crossOrigin = 'anonymous';
      const attrs = {
        'data-repo': `${CONFIG.github.owner}/${CONFIG.github.repo}`,
        'data-repo-id': CONFIG.giscus.repoId,
        'data-category': 'General',
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

  // ─── GoatCounter 방문 통계 (설정된 경우) ───
  if (isConfigured(CONFIG.goatcounter)) {
    const gc = document.createElement('script');
    gc.async = true;
    gc.setAttribute('data-goatcounter', `https://${CONFIG.goatcounter}.goatcounter.com/count`);
    gc.src = 'https://gc.zgo.at/count.js';
    document.head.appendChild(gc);
  }
})();
