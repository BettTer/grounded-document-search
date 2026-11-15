# Evidence Control Experiment / 证据对照实验

[English](#english) · [简体中文](#简体中文)

## English

Each block below is a complete model input from the original run. Copy one block at a time. Use independent requests and keep the model and settings fixed. The original run used Ollama with `gemma4:e4b`, temperature 0 and thinking disabled. Group A contains the five passages returned by keyword search in PGlite. Groups B and C differ by one passage.

All three answers said the revival was possible. A and C lacked Ecclesia’s restriction and did not report the gap. B had the restriction but omitted it from the explanation. Evaluate whether each condition is addressed and supported separately from whether the final yes/no is correct.

### A · Actual retrieval

```text
Answer using only the evidence below. Cite the supporting evidence IDs for each conclusion. If evidence is incomplete, state what it supports and what is missing.

Question:
Ecclesia's search has resolved. A Link Monster in the Graveyard was properly Link Summoned earlier and has no separate restriction. I have an available Main Monster Zone. Can Monster Reborn revive it, assuming all other requirements are met?

Evidence:
[link-summon-origin]
A Link Summon Special Summons the Link Monster from the Extra Deck. A Main Monster Zone pointed to by a Link Arrow can be a destination for the summon. Choosing that zone does not change where the monster is summoned from.

[proper-summon-before-revival]
An Extra Deck monster needs to have been properly summoned before it can be revived by a card effect. A Link Monster sent directly from the Extra Deck to the Graveyard without being properly summoned does not meet this requirement. Any separate restrictions on the target card still matter.

[link-material-count]
When a Link Monster is used as Link Material, it can count as one material or as its own Link Rating. The summon must also meet the number and type of monsters required by the monster being summoned.

[link-revival-zone]
An eligible Link Monster Special Summoned from the Graveyard goes to a Main Monster Zone. A Link Arrow does not need to point to that zone.

[monster-reborn-origin]
Monster Reborn targets one monster in either player's Graveyard and Special Summons it. The source of that summon is the Graveyard.
```

### B · Complete evidence

```text
Answer using only the evidence below. Cite the supporting evidence IDs for each conclusion. If evidence is incomplete, state what it supports and what is missing.

Question:
Ecclesia's search has resolved. A Link Monster in the Graveyard was properly Link Summoned earlier and has no separate restriction. I have an available Main Monster Zone. Can Monster Reborn revive it, assuming all other requirements are met?

Evidence:
[ecclesia-extra-deck-lock]
After Ecclesia is Normal or Special Summoned, her separate search effect can add an eligible Dogmatika card from the Deck to the hand. Once that effect resolves, the player who used it cannot Special Summon from the Extra Deck for the rest of the turn. Her effect that summons herself from the hand does not impose that restriction.

[monster-reborn-origin]
Monster Reborn targets one monster in either player's Graveyard and Special Summons it. The source of that summon is the Graveyard.

[proper-summon-before-revival]
An Extra Deck monster needs to have been properly summoned before it can be revived by a card effect. A Link Monster sent directly from the Extra Deck to the Graveyard without being properly summoned does not meet this requirement. Any separate restrictions on the target card still matter.
```

### C · One passage removed

```text
Answer using only the evidence below. Cite the supporting evidence IDs for each conclusion. If evidence is incomplete, state what it supports and what is missing.

Question:
Ecclesia's search has resolved. A Link Monster in the Graveyard was properly Link Summoned earlier and has no separate restriction. I have an available Main Monster Zone. Can Monster Reborn revive it, assuming all other requirements are met?

Evidence:
[monster-reborn-origin]
Monster Reborn targets one monster in either player's Graveyard and Special Summons it. The source of that summon is the Graveyard.

[proper-summon-before-revival]
An Extra Deck monster needs to have been properly summoned before it can be revived by a card effect. A Link Monster sent directly from the Extra Deck to the Graveyard without being properly summoned does not meet this requirement. Any separate restrictions on the target card still matter.
```

## 简体中文

以下是对应的中文输入，便于阅读和另做中文实验。复跑原实验时，请使用上方英文原文，每组单独发送并保持模型设置一致。原实验用 Ollama 的 `gemma4:e4b`，温度为 0，关闭思考。A 是 PGlite 中关键词检索返回的前 5 段。B 和 C 只差一个段落。

三组都回答可以复活。A 和 C 没有艾克莉西娅的限制依据，也没有指出缺口。B 收到了限制依据，但解释里漏了这条条件。判读时分别检查结论方向是否正确，以及每个条件是否得到回答和证据支持。

### A · 实际检索

```text
只使用下方证据回答。给每个结论标注支持它的证据编号。如果证据不完整，请说明现有证据支持什么、还缺什么。

问题：
艾克莉西娅的检索已结算。墓地里的连接怪兽此前正规连接召唤过，本身没有其他限制，我也有可用的主怪兽区。其他条件满足时，可以用死者苏生复活它吗？

证据：
[link-summon-origin]
连接召唤会把连接怪兽从额外卡组特殊召唤到场上。被连接箭头指向的主怪兽区可以作为落点。选择这个区域并不会改变本次召唤的来源。

[proper-summon-before-revival]
额外卡组怪兽要先经过正规召唤，才能由其他卡片的效果复活。没有经过正规召唤就直接从额外卡组送去墓地的连接怪兽，不满足这个条件。目标卡自身的召唤限制也仍需检查。

[link-material-count]
连接怪兽作为连接素材时，可以按一只计算，也可以按自身的连接数值计算。同时仍要满足将要召唤的怪兽所要求的素材数量和类别。

[link-revival-zone]
符合复活条件的连接怪兽从墓地特殊召唤时，放到主怪兽区。该区域无需被连接箭头指向。

[monster-reborn-origin]
「死者苏生」以任一方墓地里的一只怪兽为对象，将其特殊召唤。这次召唤的来源是墓地。
```

### B · 完整证据

```text
只使用下方证据回答。给每个结论标注支持它的证据编号。如果证据不完整，请说明现有证据支持什么、还缺什么。

问题：
艾克莉西娅的检索已结算。墓地里的连接怪兽此前正规连接召唤过，本身没有其他限制，我也有可用的主怪兽区。其他条件满足时，可以用死者苏生复活它吗？

证据：
[ecclesia-extra-deck-lock]
艾克莉西娅通常召唤或特殊召唤成功后，可以发动另一个效果，将符合条件的「教导」卡从卡组加入手牌。该效果结算后，发动者在本回合余下时间不能从额外卡组特殊召唤。她从手牌特殊召唤自身的效果没有这项限制。

[monster-reborn-origin]
「死者苏生」以任一方墓地里的一只怪兽为对象，将其特殊召唤。这次召唤的来源是墓地。

[proper-summon-before-revival]
额外卡组怪兽要先经过正规召唤，才能由其他卡片的效果复活。没有经过正规召唤就直接从额外卡组送去墓地的连接怪兽，不满足这个条件。目标卡自身的召唤限制也仍需检查。
```

### C · 移除一段

```text
只使用下方证据回答。给每个结论标注支持它的证据编号。如果证据不完整，请说明现有证据支持什么、还缺什么。

问题：
艾克莉西娅的检索已结算。墓地里的连接怪兽此前正规连接召唤过，本身没有其他限制，我也有可用的主怪兽区。其他条件满足时，可以用死者苏生复活它吗？

证据：
[monster-reborn-origin]
「死者苏生」以任一方墓地里的一只怪兽为对象，将其特殊召唤。这次召唤的来源是墓地。

[proper-summon-before-revival]
额外卡组怪兽要先经过正规召唤，才能由其他卡片的效果复活。没有经过正规召唤就直接从额外卡组送去墓地的连接怪兽，不满足这个条件。目标卡自身的召唤限制也仍需检查。
```
