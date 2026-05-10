#!/usr/bin/env python3
"""
sync-index.py — 메인 index와 시즌 index의 에피소드 카운트 자동 갱신

용도:
  새 에피소드 추가/삭제 시 자동으로:
  - 메인 index.html의 "N SEASONS · M EPISODES" 갱신
  - 메인 index.html의 stat-num (총 에피소드) 갱신
  - 각 시즌 index.html의 "N편" 메타 갱신
  - 각 시즌 index.html의 stat-num "총 에피소드" 갱신

사용:
  python tools/sync-index.py        # 갱신 적용
  python tools/sync-index.py --check # 불일치만 체크 (CI용)
"""
import os
import re
import sys
import glob

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def count_episodes(season_dir):
    """index.html 제외한 .html 파일 수"""
    files = glob.glob(os.path.join(REPO, season_dir, "*.html"))
    return len([f for f in files if not f.endswith("index.html")])


def update_main_index(s1, s2, s3, check_only=False):
    """메인 index.html 갱신"""
    fp = os.path.join(REPO, "index.html")
    with open(fp, "r", encoding="utf-8") as f:
        content = f.read()

    total = s1 + s2 + s3
    issues = []

    # "N SEASONS · M EPISODES" 패턴
    m = re.search(r"3 SEASONS · (\d+) EPISODES", content)
    if m and int(m.group(1)) != total:
        issues.append(f"main hero-meta: {m.group(1)} → {total}")
        if not check_only:
            content = re.sub(
                r"3 SEASONS · \d+ EPISODES",
                f"3 SEASONS · {total} EPISODES",
                content,
            )

    # stat-num (Episodes 라벨 위)
    m = re.search(
        r'<div class="stat-num">(\d+)</div>\s*<div class="stat-label">Episodes</div>',
        content,
    )
    if m and int(m.group(1)) != total:
        issues.append(f"main stat-num Episodes: {m.group(1)} → {total}")
        if not check_only:
            content = re.sub(
                r'(<div class="stat-num">)\d+(</div>\s*<div class="stat-label">Episodes</div>)',
                rf"\g<1>{total}\g<2>",
                content,
            )

    if not check_only and issues:
        with open(fp, "w", encoding="utf-8") as f:
            f.write(content)
    return issues


def update_season_index(season, count, check_only=False):
    """시즌 index.html 갱신"""
    fp = os.path.join(REPO, season, "index.html")
    if not os.path.exists(fp):
        return []
    with open(fp, "r", encoding="utf-8") as f:
        content = f.read()

    issues = []

    # "에피소드 <span>N편</span>" 패턴
    m = re.search(
        r'<div class="meta-item">에피소드 <span>(\d+)편</span></div>', content
    )
    if m and int(m.group(1)) != count:
        issues.append(f"{season} meta 에피소드: {m.group(1)}편 → {count}편")
        if not check_only:
            content = re.sub(
                r'(<div class="meta-item">에피소드 <span>)\d+(편</span></div>)',
                rf"\g<1>{count}\g<2>",
                content,
            )

    # stat-num (총 에피소드)
    m = re.search(
        r'<span class="stat-num">(\d+)</span><span class="stat-label">총 에피소드',
        content,
    )
    if m and int(m.group(1)) != count:
        issues.append(f"{season} stat-num 총 에피소드: {m.group(1)} → {count}")
        if not check_only:
            content = re.sub(
                r'(<span class="stat-num">)\d+(</span><span class="stat-label">총 에피소드)',
                rf"\g<1>{count}\g<2>",
                content,
            )

    if not check_only and issues:
        with open(fp, "w", encoding="utf-8") as f:
            f.write(content)
    return issues


def main():
    check_only = "--check" in sys.argv

    counts = {
        "s1": count_episodes("s1"),
        "s2": count_episodes("s2"),
        "s3": count_episodes("s3"),
    }
    print(f"실측: S1={counts['s1']}, S2={counts['s2']}, S3={counts['s3']}, 합계={sum(counts.values())}")

    all_issues = []
    all_issues += update_main_index(counts["s1"], counts["s2"], counts["s3"], check_only)
    for s, cnt in counts.items():
        all_issues += update_season_index(s, cnt, check_only)

    if all_issues:
        action = "발견" if check_only else "정정"
        print(f"\n[{action}] {len(all_issues)}건:")
        for i in all_issues:
            print(f"  - {i}")
        if check_only:
            sys.exit(1)
    else:
        print("\n모든 인덱스 카운트 일치 [OK]")


if __name__ == "__main__":
    main()
