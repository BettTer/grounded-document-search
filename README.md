# Grounded Document Search

[English](#english) · [简体中文](#简体中文)

## English

Grounded Document Search is a portfolio project for finding evidence across multiple documents. It aims to surface the relevant passages, cite them in an answer, and explain what evidence is missing when the documents only cover part of the question.

The first dataset uses original notes on Yu-Gi-Oh! card interactions and summoning rules, with links to official references. For example, answering whether a Link Summon is possible after a card effect resolves can require both the card's restriction and the general summoning rules. A second dataset of fictional engineering runbooks will test the same workflow in a different domain.

**Status:** Early development. The first milestone is a Python CLI with PostgreSQL full-text search, a repeatable evaluation command, and a small cited-answer demo. Planned comparisons cover keyword, vector, and hybrid retrieval, measuring evidence recall, citation support, and latency.

[First evaluation case](docs/first-evaluation-case.md#english)

## 简体中文

Grounded Document Search 是一个跨文档检索作品。它要把散落在不同文档里的相关段落找齐，在回答里给出可核对的引用，并在文档只能回答一部分时指出还缺什么依据。

第一套语料是原创的游戏王卡片交互和召唤规则笔记，并附官方资料链接。例如，要判断某个卡片效果结算后还能否进行连接召唤，可能需要同时查到该效果的限制和通用召唤规则。第二套使用自编的工程运维手册，验证同一套流程能否换个领域复跑。

**当前状态**：早期开发。第一个里程碑包含 Python 命令行、PostgreSQL 全文检索、可重复运行的评测命令和带引用的问答示例。后续计划比较关键词、向量和混合检索，记录证据召回率、引用支持情况和延迟。

[首条评测题](docs/first-evaluation-case.md#简体中文)
