# survey-analyzer-lite

零依赖的**开放题聚类与观点摘要**小工具：把一堆用户开放回答按语义近似聚成若干簇，统计高频词，并为每簇挑一条代表性回答。纯标准库（中文 bigram 特征 + 贪心聚类），无需任何 API。

## 功能简介

- 中文按相邻两字（bigram）做特征，无需分词库。
- 统计全局高频观点词。
- 按特征重合度把相似回答聚成簇，按规模排序。
- 每簇自动选一条代表性回答 + 示例。

## 快速开始

```bash
# 从文件（每行一条）
python3 cli.py --file answers.txt

# 内联多条
python3 cli.py --answer "加载太慢" --answer "页面很卡" --answer "客服态度好"
```

## 无 API key 如何运行

本项目**完全不需要 API key**，纯本地规则聚类。

## 目录说明

```
survey-analyzer-lite/
├── survey.py    # bigrams / cluster / summarize
├── cli.py    # 命令行入口
├── tests/
│   └── test_survey.py
├── README.md
├── LICENSE
└── .gitignore
```

## 运行测试

```bash
python3 -m unittest discover -s tests
```

## License

MIT License，Copyright (c) 2026 ljiang9。
