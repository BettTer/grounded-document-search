# Grounded Document Search

[English](#english) · [简体中文](#简体中文)

## English

Grounded Document Search is a portfolio project for finding evidence across multiple documents. It aims to surface the relevant passages, cite them in an answer, and explain what evidence is missing when the documents only cover part of the question.

The first dataset uses original notes on Yu-Gi-Oh! card interactions and summoning rules, with links to official references. For example, answering whether a Link Summon is possible after a card effect resolves can require both the card's restriction and the general summoning rules. A second dataset of fictional engineering runbooks will test the same workflow in a different domain.

**Status:** The Python CLI can index the the English evidence from the bilingual corpus in PostgreSQL. Keyword search and a repeatable retrieval evaluation are available. The cited-answer demo is next. Planned comparisons cover keyword, vector, and hybrid retrieval, measuring evidence recall, citation support, and latency.

[First evaluation case](docs/first-evaluation-case.md#english) · [Evidence control experiment](docs/evidence-control-experiment.md#english)

### Quick start

Run from the repository root with Python 3.10+ and Docker Compose.

```bash
docker compose up -d --wait db
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python -m grounded_search index --corpus yugioh
```

The sample corpus indexes 7 English evidence sections with their source links.

### Search and evaluate

Search returns ranked passages and source links. Evaluation reports Recall@1/3/5, complete evidence coverage, missing passages, and retrieval latency. Default OR matching accepts any query term. Use `--match and` to compare all-term matching.

```bash
python -m grounded_search search "Can Monster Reborn revive a Link Monster?" --corpus yugioh
python -m grounded_search eval --corpus yugioh --dataset evals/yugioh-smoke.json
python -m grounded_search eval --corpus yugioh --dataset evals/yugioh-smoke.json --match and
```

### Replay the evidence controls

Start Ollama and run `ollama list` to find your installed model tag. Replace `gemma4:e4b` below if you use another model. Frozen replay reads the published inputs and only needs Python and Ollama.

```bash
python3 evals/evidence_control.py prepare --frozen
python3 evals/evidence_control.py run '<directory printed by prepare>' --model gemma4:e4b
```

To retrieve fresh passages for group A, complete the indexing steps and run `prepare` without `--frozen`. Each run saves the prompts, requests, and responses to the Git-ignored `evals/runs/` directory.

## 简体中文

Grounded Document Search 是一个跨文档检索作品。它要把散落在不同文档里的相关段落找齐，在回答里给出可核对的引用，并在文档只能回答一部分时指出还缺什么依据。

第一套语料是原创的游戏王卡片交互和召唤规则笔记，并附官方资料链接。例如，要判断某个卡片效果结算后还能否进行连接召唤，可能需要同时查到该效果的限制和通用召唤规则。第二套使用自编的工程运维手册，验证同一套流程能否换个领域复跑。

**当前状态**：Python 命令行已能将双语语料的英文证据导入 PostgreSQL。关键词检索和可重复运行的检索评测已实现，接下来是带引用的问答示例。后续计划比较关键词、向量和混合检索，记录证据召回率、引用支持情况和延迟。

[首条评测题](docs/first-evaluation-case.md#简体中文) · [证据对照实验](docs/evidence-control-experiment.md#简体中文)

### 快速启动

在仓库根目录使用 Python 3.10+ 和 Docker Compose 执行以下命令。

```bash
docker compose up -d --wait db
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python -m grounded_search index --corpus yugioh
```

样例语料会导入 7 段英文证据，并保留来源链接。

### 检索与评测

检索返回排序后的段落和来源链接。评测报告 Recall@1/3/5、全部证据找齐情况、遗漏段落和检索耗时。默认 OR 匹配允许任一查询词命中，可以用 `--match and` 对比全词匹配。

```bash
python -m grounded_search search "Can Monster Reborn revive a Link Monster?" --corpus yugioh
python -m grounded_search eval --corpus yugioh --dataset evals/yugioh-smoke.json
python -m grounded_search eval --corpus yugioh --dataset evals/yugioh-smoke.json --match and
```

### 复跑证据对照

启动 Ollama，再用 `ollama list` 查看已安装的模型标签。如果使用其他模型，把下方的 `gemma4:e4b` 换成你的标签。复跑公开的固定输入只需要 Python 和 Ollama。

```bash
python3 evals/evidence_control.py prepare --frozen
python3 evals/evidence_control.py run '<prepare 打印的目录>' --model gemma4:e4b
```

如需从数据库重新检索 A 组证据，完成导入后运行 `prepare`，省去 `--frozen` 参数。每轮的提示、请求和响应都保存在 Git 忽略的 `evals/runs/` 目录。
