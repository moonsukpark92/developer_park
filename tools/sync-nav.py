#!/usr/bin/env python3
"""
sync-nav.py — 시즌 내 모든 에피소드의 하단 네비게이션 자동 동기화

용도:
  새 에피소드 추가 시 같은 시즌의 모든 에피소드 하단 네비에 새 링크 자동 삽입.
  파일명 정렬 기준으로 prev/next 자동 계산.

시즌별 ORDER 규칙:
  S1: ep001 ~ ep008
  S2: ep001 ~ ep007 → epilogue → final
  S3: prologue → ep001 ~ ep005 → interlude → ep006 ~ ep0NN → epilogue2 → epilogue2_2

사용:
  python tools/sync-nav.py s3              # S3 모든 에피소드 하단 네비 재생성
  python tools/sync-nav.py s3 --check      # 동기화 필요 여부만 검사
"""
import os
import re
import sys
import glob

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_season_order(season):
    """시즌별 에피소드 순서 + 라벨 반환"""
    files = sorted(glob.glob(os.path.join(REPO, season, "*.html")))
    files = [os.path.basename(f) for f in files if not f.endswith("index.html")]

    if season == "s1":
        # ep001 ~ ep008
        order = sorted([f.replace(".html", "") for f in files if f.startswith("ep")])
        labels = {ep: ep[2:].lstrip("0") or "0" for ep in order}
        return order, labels

    if season == "s2":
        eps = sorted([f.replace(".html", "") for f in files if f.startswith("ep")])
        order = eps[:]
        if "epilogue.html" in files:
            order.append("epilogue")
        if "final.html" in files:
            order.append("final")
        labels = {ep: ep[2:].lstrip("0") or "0" for ep in eps}
        labels["epilogue"] = "EP"
        labels["final"] = "FIN"
        return order, labels

    if season == "s3":
        eps = sorted([f.replace(".html", "") for f in files if re.match(r"ep\d+$", f.replace(".html", ""))])
        order = []
        if "prologue.html" in files:
            order.append("prologue")
        # ep001~ep005
        order += [e for e in eps if e <= "ep005"]
        if "interlude.html" in files:
            order.append("interlude")
        # 나머지 ep
        order += [e for e in eps if e > "ep005"]
        # epilogue2(_2 포함) 마지막
        for f in sorted(files):
            n = f.replace(".html", "")
            if n.startswith("epilogue") and n not in order:
                order.append(n)

        labels = {}
        for ep in order:
            if ep == "prologue":
                labels[ep] = "PR"
            elif ep == "interlude":
                labels[ep] = "IL"
            elif ep == "epilogue2":
                labels[ep] = "E2"
            elif ep == "epilogue2_2":
                labels[ep] = "E2-2"
            elif ep == "ep013":
                labels[ep] = "12-2"  # ep013은 EP012 2부
            else:
                labels[ep] = ep[2:].lstrip("0") or "0"
        return order, labels

    return [], {}


def make_bottom_nav(current, order, labels):
    idx = order.index(current)
    prev_link = order[idx - 1] + ".html" if idx > 0 else "index.html"
    next_link = order[idx + 1] + ".html" if idx < len(order) - 1 else "index.html"

    items = [
        f'<a href="{prev_link}" style="color:#e8a83a;text-decoration:none;padding:4px 8px;">&larr;</a>',
        '<a href="index.html" style="color:#e8a83a;text-decoration:none;padding:4px 8px;font-weight:700;">&#9776;</a>',
    ]
    for ep in order:
        label = labels[ep]
        if ep == current:
            style = "color:#fff;text-decoration:none;padding:4px 5px;font-weight:700;border-bottom:2px solid #e8a83a;"
        else:
            style = "color:rgba(255,255,255,.4);text-decoration:none;padding:4px 5px;"
        items.append(f'<a href="{ep}.html" style="{style}">{label}</a>')
    items.append(f'<a href="{next_link}" style="color:#e8a83a;text-decoration:none;padding:4px 8px;">&rarr;</a>')

    inner = "\n  ".join(items)
    return (
        '<div style="position:fixed;bottom:0;left:0;right:0;z-index:9999;'
        "background:rgba(4,5,10,.97);backdrop-filter:blur(10px);"
        "border-top:1px solid rgba(232,168,58,.12);padding:10px 16px;"
        "display:flex;align-items:center;justify-content:center;gap:5px;"
        'font-family:monospace;font-size:.6rem;flex-wrap:wrap;">\n'
        f"  {inner}\n</div>"
    )


def main():
    if len(sys.argv) < 2:
        print("사용: python tools/sync-nav.py <s1|s2|s3> [--check]")
        sys.exit(2)

    season = sys.argv[1]
    check_only = "--check" in sys.argv
    order, labels = get_season_order(season)

    if not order:
        print(f"시즌 {season} 처리할 에피소드 없음")
        return

    print(f"{season} 순서: {' → '.join(order)}")

    changed = []
    for ep in order:
        fp = os.path.join(REPO, season, ep + ".html")
        with open(fp, "r", encoding="utf-8") as f:
            content = f.read()

        # 기존 하단 네비 div 제거 (position:fixed;bottom:0;...z-index:9999)
        new_content = re.sub(
            r'<div style="position:fixed;bottom:0[^"]*z-index:9999[^"]*"[^>]*>.*?</div>',
            "",
            content,
            flags=re.DOTALL,
        )

        # 새 하단 네비 삽입 (blog-features 직전 또는 </body> 직전)
        new_nav = make_bottom_nav(ep, order, labels)
        if "<!-- BLOG FEATURES" in new_content:
            new_content = new_content.replace(
                "<!-- BLOG FEATURES", new_nav + "\n\n<!-- BLOG FEATURES"
            )
        else:
            new_content = new_content.replace("</body>", new_nav + "\n</body>")

        if new_content != content:
            changed.append(ep)
            if not check_only:
                with open(fp, "w", encoding="utf-8") as f:
                    f.write(new_content)

    if changed:
        action = "필요" if check_only else "갱신"
        print(f"\n[{action}] {len(changed)}건: {', '.join(changed)}")
        if check_only:
            sys.exit(1)
    else:
        print("\n모든 하단 네비 동기 [OK]")


if __name__ == "__main__":
    main()
