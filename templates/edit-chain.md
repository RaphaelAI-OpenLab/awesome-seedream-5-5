# 三轮连续编辑 / Three-round edit chain

**本仓库原创练习配方 · 未执行 · 不对应来源样张的原始输入**

## 中文指令

```text
每轮以上一轮输出作为输入，一次只提交一条指令。第一轮：把自行车车架改为墨绿色，其他内容保持。第二轮：只给车篮添加一束雏菊。第三轮：只在车把加一个铜色车铃。保留人物、背景、相机位置与光照。
```

## English prompt

```text
Submit one instruction per round, using the preceding output as the next input. Round 1: recolor the bicycle frame forest green; preserve everything else. Round 2: add only a bunch of daisies to the basket. Round 3: add only a brass bell to the handlebar. Preserve the people, background, camera position and lighting.
```

## 验收项

1. 分别保存每一轮，不能只保留末轮。
2. 比较每轮未编辑区域，记录新增漂移。
3. 确认前两轮的编辑在第三轮仍然存在。

如服务没有对应模型或输出开关，不以提示词文字代替服务能力。生成结果需要人工检查。
