"""survey-analyzer-lite 命令行入口。

用法示例：
    python3 cli.py --file answers.txt
    python3 cli.py --answer "加载太慢" --answer "页面很卡" --answer "客服态度好"
"""

from __future__ import annotations

import argparse
import sys

from survey import summarize


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="survey-analyzer-lite",
        description="开放题聚类与高频观点摘要",
    )
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--file", help="从文本文件读取，每行一条回答")
    src.add_argument("--answer", action="append", default=[],
                     help="内联一条回答，可重复")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.file:
        with open(args.file, encoding="utf-8") as f:
            answers = [ln.strip() for ln in f.read().splitlines() if ln.strip()]
    else:
        answers = args.answer

    s = summarize(answers)
    print(f"有效回答：{s['total']} 条")
    print("\n高频词：")
    for kw, cnt in s["top_keywords"]:
        print(f"  {kw}  x{cnt}")
    print("\n观点分组：")
    for i, c in enumerate(s["clusters"], 1):
        print(f"  簇{i}（{c['count']} 条）代表：{c['representative']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
