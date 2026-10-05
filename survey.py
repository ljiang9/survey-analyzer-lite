"""survey-analyzer-lite：对开放题做轻量聚类与观点摘要。

纯标准库实现：
- 中文按 bigram（相邻两字）做特征；
- 统计高频词；
- 按关键词重合做简单聚类（贪心：把句子并入已有簇，否则新簇）；
- 每个簇取最短/最典型的一条作为代表性回答；
- 输出高频观点 + 每簇规模与代表回答。
"""

from __future__ import annotations

import re
from collections import Counter

STOP = set("的 了 是 我 也 都 就 而 及 与 这 那 在 有 和 就 不 人 都 一 个 上 们 到 说 要 去 你 会 着 没有 看 好 自己 这 他".split())


def bigrams(text: str) -> list[str]:
    """把中文文本切成 bigram 特征。"""
    text = re.sub(r"[^\u4e00-\u9fa5A-Za-z0-9]", "", text)
    if len(text) < 2:
        return [text] if text else []
    return [text[i:i + 2] for i in range(len(text) - 1)]


def keywords(text: str, top: int = 5) -> list[str]:
    bg = [b for b in bigrams(text) if not any(s in b for s in STOP)]
    return bg[:top]


def features(text: str) -> set:
    """聚类特征：bigram + 去停用词后的单字。"""
    feats = set(bigrams(text))
    cleaned = re.sub(r"[^\u4e00-\u9fa5A-Za-z0-9]", "", text)
    for ch in cleaned:
        if ch not in STOP:
            feats.add(ch)
    return feats


def cluster(answers: list[str], min_overlap: int = 1) -> list[dict]:
    """把开放题答案聚成若干簇。"""
    clusters: list[dict] = []
    for ans in answers:
        if not ans.strip():
            continue
        feats = features(ans)
        placed = False
        for c in clusters:
            if len(feats & c["feats"]) >= min_overlap:
                c["items"].append(ans)
                c["feats"] |= feats
                placed = True
                break
        if not placed:
            clusters.append({"feats": feats, "items": [ans]})
    # 按规模排序
    clusters.sort(key=lambda c: len(c["items"]), reverse=True)
    return clusters


def summarize(answers: list[str]) -> dict:
    """生成高频观点摘要。"""
    # 全局高频词
    counter: Counter = Counter()
    for a in answers:
        for b in bigrams(a):
            if b not in STOP and len(b) >= 2:
                counter[b] += 1
    top_keywords = counter.most_common(8)

    clusters = cluster(answers)
    result_clusters = []
    for c in clusters:
        items = c["items"]
        # 代表回答：长度中等、信息较全的一条
        rep = sorted(items, key=lambda s: (abs(len(s) - 12), len(s)))[0]
        result_clusters.append({
            "count": len(items),
            "representative": rep,
            "examples": items[:3],
        })

    return {
        "total": len([a for a in answers if a.strip()]),
        "top_keywords": top_keywords,
        "clusters": result_clusters,
    }
