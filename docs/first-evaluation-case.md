# First Evaluation Case / 首条评测题

[English](#english) · [简体中文](#简体中文)

## English

### Ecclesia and Link Summon sequencing

**Type:** Multi-document question about effect sequencing. This case uses the official TCG references linked below.

### Question

Assume a monster Special Summoned from the Extra Deck is already on the field and all other requirements are met. I Special Summon Dogmatika Ecclesia, the Virtuous from my hand using her own effect, then resolve her effect that adds a card from the Deck to my hand. Can I still Link Summon to a Main Monster Zone a Link Arrow points to? What if I Link Summon first, then summon Ecclesia and use her search effect?

### Expected evidence

| Evidence | What it must support |
| --- | --- |
| 1. Ecclesia's effects | The effect that Special Summons Ecclesia from the hand and the effect that searches on summon are separate. The search effect restricts Extra Deck summons for the rest of the turn. [Official card database](https://www.db.yugioh-card.com/yugiohdb/card_search.action?cid=15239&ope=2&request_locale=en) |
| 2. Link Summons and zones | A Main Monster Zone a Link Arrow points to can be a destination for a Link Summon. The monster is still summoned from the Extra Deck. [Official rulebook section on Link Summons](https://img.yugioh-card.com/en/downloads/rulebook/SD_RuleBook_EN_10.pdf#page=9) |

### Reference judgment

- **Resolve the search effect, then Link Summon:** The Link Summon is blocked. The arrow makes the zone available, but the Link Summon is still a Special Summon from the Extra Deck and falls under the restriction. Cite evidence 1 and 2.
- **Link Summon, then summon Ecclesia and resolve her search effect:** This order works if all material, zone, timing, and activation requirements are met. The restriction applies to actions later that turn, after the effect resolves. Cite evidence 1 and 2.
- Ecclesia's own Special Summon effect does not impose this restriction. Mark any answer that attributes the restriction to that effect as incorrect. Cite evidence 1.

### How to run this case

1. **Keyword baseline:** Check whether both pieces of evidence appear in the top K results. If only one appears, record whether the missing evidence is the card effect or the summoning rule.
2. **Complete-evidence control:** Give the model both passages. Check that it addresses both sequences separately and that the citations support the corresponding conclusions.
3. **Missing-evidence control:** Give the model only evidence 1. It should explain what imposes the restriction and how long it lasts, then identify the missing rule about Link Summons and zones pointed to by Link Arrows. Mark a conclusion unsupported by the supplied evidence even if the model gets it right from memory.

The question and evidence IDs will go into the evaluation dataset. Use manually selected passages only in the control runs. In the retrieval run, pass only the user's question.

## 简体中文

### 艾克莉西娅与连接召唤顺序

**类型**：多文档、效果顺序。规则口径为所引实体卡官方资料。

### 问题

假设场上已经有从额外卡组特殊召唤的怪兽，其他条件也满足。我用教导的圣女 艾克莉西娅自己的效果从手牌特殊召唤，再让她的检索效果结算。之后，我还能在连接箭头指向的主怪兽区做连接召唤吗？如果改成先完成连接召唤，再召唤艾克莉西娅并使用她的检索效果，是否可行？

### 预期证据

| 证据 | 必须支持的事实 |
| --- | --- |
| 一：艾克莉西娅的效果说明 | 自身从手牌特召和召唤后的检索是两个效果。额外卡组限制来自检索效果，影响本回合余下时间。 [官方卡片数据库](https://www.db.yugioh-card.com/yugiohdb/card_search.action?cid=15239&ope=2&request_locale=en) |
| 二：连接召唤与区域规则 | 指向的主怪兽区可以是连接召唤的落点，这次召唤仍然是从额外卡组进行。 [官方规则书的连接召唤章节](https://img.yugioh-card.com/en/downloads/rulebook/SD_RuleBook_EN_10.pdf#page=9) |

### 参考判断

- **先结算检索，再连接召唤**：不可以。连接箭头提供可用区域，连接召唤本身仍属于检索效果限制的额外卡组特殊召唤。引用证据一和二。
- **先连接召唤，再召唤艾克莉西娅并结算检索**：在材料、区域、时点和效果发动条件均满足时可行。限制只影响结算后本回合余下的动作。引用证据一和二。
- 自身特召未施加上述限制；回答若把限制归到自身特召，记为错误。引用证据一。

### 怎么跑这条题

1. **关键词基线**：看前 K 条是否包含两处证据。只命中一处时，记下缺的是卡片效果还是召唤规则。
2. **完整证据对照**：手动把两段证据一起送给模型。检查两个顺序是否分别回答，以及引用是否支持对应结论。
3. **缺证据对照**：只提供证据一。期望仍可解释限制的来源和持续时间，同时指出尚缺连接召唤与箭头区域的依据。模型即便凭记忆给出正确结论，该结论在本次输入中仍记为证据不足。

预计将题目和证据编号写入评测数据。人工指定证据只用于对照实验，实际检索时仅传用户问题。
