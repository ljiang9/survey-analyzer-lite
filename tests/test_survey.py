import unittest

from survey import bigrams, cluster, summarize


ANSWERS = [
    "加载太慢了，经常转圈",
    "页面很卡，加载慢",
    "打开速度慢，白屏很久",
    "客服态度很好，问题解决快",
    "客服回复及时，服务不错",
    "价格有点贵，希望打折",
]


class TestBigram(unittest.TestCase):
    def test_basic(self):
        bg = bigrams("加载慢")
        self.assertIn("加载", bg)
        self.assertIn("载慢", bg)


class TestCluster(unittest.TestCase):
    def test_groups_similar(self):
        clusters = cluster(ANSWERS)
        # 前 3 条都是“慢/卡”相关，应聚到一起
        sizes = sorted(len(c["items"]) for c in clusters)
        self.assertGreaterEqual(max(sizes), 3)

    def test_has_representative(self):
        s = summarize(ANSWERS)
        for c in s["clusters"]:
            self.assertTrue(c["representative"])
            self.assertGreater(c["count"], 0)


class TestSummarize(unittest.TestCase):
    def test_total(self):
        s = summarize(ANSWERS)
        self.assertEqual(s["total"], 6)

    def test_top_keywords(self):
        s = summarize(ANSWERS)
        kws = [k for k, _ in s["top_keywords"]]
        self.assertTrue(any("加载" in k or "慢" in k for k in kws))

    def test_empty(self):
        s = summarize(["", "  "])
        self.assertEqual(s["total"], 0)


if __name__ == "__main__":
    unittest.main()
