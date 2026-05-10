#!/usr/bin/env python3
"""
add-episode.py — _inbox 신규 에피소드 단일 진입점 자동 처리

용도:
  ../개발자 박대표 시리즈/_inbox/ 의 HTML 파일을 받아:
  1. 콘텐츠 정제: 직원 마스킹, (주)데코페이브 통일, 기타 lint 위반 자동 정리
  2. 시리즈 네비 + body padding + blog-features 마운트 통합
  3. 적절한 시즌(s1/s2/s3) 위치로 표준 파일명으로 배치
  4. sync-nav.py로 형제 에피소드 네비 동기화
  5. sync-index.py로 인덱스 카운트 갱신
  6. 원본 폴더 동기화
  7. 처리 완료 파일을 _archive/staging_history/로 이동

사용:
  python tools/add-episode.py                    # _inbox 자동 스캔
  python tools/add-episode.py path/to/file.html  # 특정 파일만 처리
  python tools/add-episode.py --dry-run          # 검사만
"""
import os
import re
import sys
import shutil
import subprocess
from datetime import datetime

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK_DIR = os.path.normpath(os.path.join(REPO, "..", "개발자 박대표 시리즈"))
INBOX = os.path.join(WORK_DIR, "_inbox")
ARCHIVE = os.path.join(WORK_DIR, "_archive", "staging_history")

# 직원 실명 마스킹 (홍길동 → 홍*동)
EMPLOYEES = [
    ("최종현", "최*현"), ("조은진", "조*진"), ("임나영", "임*영"),
    ("정하윤", "정*윤"), ("한병주", "한*주"), ("조성범", "조*범"),
    ("신다혜", "신*혜"), ("허상민", "허*민"), ("이상우", "이*우"),
    ("서인표", "서*표"), ("오이벡", "오*벡"), ("김지완", "김*완"),
    ("박세연", "박*연"), ("강민구", "강*구"),
]

SERIES_NAV_TEMPLATE = (
    '<div style="position:fixed;top:0;left:0;right:0;z-index:9999;'
    'background:rgba(4,5,10,.95);backdrop-filter:blur(8px);'
    'border-bottom:1px solid rgba(232,168,58,.15);padding:8px 24px;'
    'display:flex;align-items:center;gap:16px;font-family:monospace;'
    'font-size:.7rem;letter-spacing:1px;">\n'
    '  <a href="../index.html" style="color:#e8a83a;text-decoration:none;font-weight:700;">개발자 박대표</a>\n'
    '  <span style="color:rgba(255,255,255,.2);">|</span>\n'
    '  <a href="../s1/index.html" style="color:rgba(255,255,255,.4);text-decoration:none;">S1</a>\n'
    '  <a href="../s2/index.html" style="color:rgba(255,255,255,.4);text-decoration:none;">S2</a>\n'
    '  <a href="../s3/index.html" style="color:#fff;text-decoration:none;font-weight:700;border-bottom:2px solid #e8a83a;padding-bottom:2px;">S3</a>\n'
    '</div>'
)

BLOG_FEATURES = (
    '<!-- BLOG FEATURES (subscribe + comments + analytics) -->\n'
    '<div id="blog-features-mount"></div>\n'
    '<script src="../assets/blog-features.js"></script>'
)


def detect_season_and_filename(content, src_filename):
    """파일 내용/이름으로 시즌과 표준 파일명 추정"""
    name = src_filename.lower()
    title = ""
    m = re.search(r"<title>(.*?)</title>", content, re.IGNORECASE | re.DOTALL)
    if m:
        title = m.group(1)

    # 시즌 추정
    if "s3" in name or "season 3" in title.lower() or "데코허브" in content:
        season = "s3"
    elif "s2" in name or "season 2" in title.lower() or "100일" in content:
        season = "s2"
    elif "s1" in name or "season 1" in title.lower():
        season = "s1"
    else:
        season = "s3"  # 기본

    # 파일명 추정 (ep0NN, prologue, interlude, epilogue)
    m = re.search(r"ep(\d{1,3})", name)
    if m:
        n = int(m.group(1))
        return season, f"ep{n:03d}.html"
    if "prologue" in name:
        return season, "prologue.html"
    if "interlude" in name:
        return season, "interlude.html"
    if "epilogue" in name:
        # 이미 epilogue, epilogue2 있으면 다음 번호
        existing = sorted([
            f for f in os.listdir(os.path.join(REPO, season))
            if f.startswith("epilogue") and f.endswith(".html")
        ])
        if not existing:
            return season, "epilogue.html"
        if existing[-1] == "epilogue.html":
            return season, "epilogue2.html"
        m = re.search(r"epilogue(\d+)", existing[-1])
        n = int(m.group(1)) + 1 if m else 2
        return season, f"epilogue{n}.html"

    # 마지막 ep 번호 + 1
    eps = sorted([
        int(re.search(r"ep(\d+)", f).group(1))
        for f in os.listdir(os.path.join(REPO, season))
        if re.match(r"^ep\d+\.html$", f)
    ])
    next_n = (max(eps) + 1) if eps else 1
    return season, f"ep{next_n:03d}.html"


def cleanse_content(content):
    """마스킹 + (주)데코페이브 통일 + 기본 lint 정리"""
    # 직원 마스킹
    for old, new in EMPLOYEES:
        content = content.replace(old, new)
    # (주)데코페이브 통일
    content = content.replace("데코페이브㈜", "(주)데코페이브")
    content = content.replace("데코페이브 주식회사", "(주)데코페이브")
    content = content.replace("데코페이브&#x338E;", "(주)데코페이브")
    content = content.replace("데코페이브&#xAC8C;", "(주)데코페이브")
    return content


def integrate_layout(content):
    """body padding + 시리즈 네비 + blog-features 마운트 추가"""
    # 이미 통합됐으면 skip
    has_series_nav = "z-index:9999" in content[:5000] and "../index.html" in content[:5000]
    has_blog = "blog-features-mount" in content

    # body 태그 padding
    if "padding-top:40px" not in content[:content.find("</head>") + 200 if "</head>" in content else 5000]:
        content = re.sub(
            r"<body([^>]*)>",
            r'<body\1 style="padding-top:40px;padding-bottom:60px;">',
            content,
            count=1,
        )

    # 시리즈 네비
    if not has_series_nav:
        content = re.sub(
            r"(<body[^>]*>)",
            r"\1\n" + SERIES_NAV_TEMPLATE,
            content,
            count=1,
        )

    # blog-features
    if not has_blog:
        content = content.replace("</body>", BLOG_FEATURES + "\n</body>")

    return content


def process_file(src_path, dry_run=False):
    src_filename = os.path.basename(src_path)
    print(f"\n=== 처리: {src_filename} ===")

    with open(src_path, "r", encoding="utf-8") as f:
        content = f.read()

    season, dest_filename = detect_season_and_filename(content, src_filename)
    dest_path = os.path.join(REPO, season, dest_filename)

    print(f"  → {season}/{dest_filename}")

    content = cleanse_content(content)
    content = integrate_layout(content)

    if dry_run:
        print("  (dry-run: 파일 작성 안 함)")
        return season, dest_filename

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(content)
    # 원본 폴더 동기화
    work_dest = os.path.join(WORK_DIR, season, dest_filename)
    os.makedirs(os.path.dirname(work_dest), exist_ok=True)
    shutil.copy(dest_path, work_dest)

    # _archive로 원본 이동
    os.makedirs(ARCHIVE, exist_ok=True)
    archive_path = os.path.join(ARCHIVE, src_filename)
    if os.path.exists(archive_path):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_path = archive_path.replace(".html", f"_{ts}.html")
    shutil.move(src_path, archive_path)
    print(f"  원본 → {archive_path}")

    return season, dest_filename


def main():
    dry_run = "--dry-run" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("--")]

    targets = []
    if args:
        targets = [os.path.abspath(a) for a in args]
    else:
        if not os.path.isdir(INBOX):
            print(f"_inbox 없음: {INBOX}")
            return
        targets = [
            os.path.join(INBOX, f)
            for f in os.listdir(INBOX)
            if f.endswith(".html")
        ]

    if not targets:
        print("처리할 .html 파일 없음")
        return

    seasons_touched = set()
    for t in targets:
        s, _ = process_file(t, dry_run)
        seasons_touched.add(s)

    if dry_run:
        return

    # sync-nav 시즌별 + sync-index
    for s in seasons_touched:
        print(f"\n[sync-nav {s}]")
        subprocess.run([sys.executable, "tools/sync-nav.py", s], cwd=REPO)
    print("\n[sync-index]")
    subprocess.run([sys.executable, "tools/sync-index.py"], cwd=REPO)

    print("\n완료. git add/commit/push는 수동 또는 hook으로.")


if __name__ == "__main__":
    main()
