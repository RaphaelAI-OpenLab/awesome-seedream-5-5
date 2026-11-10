# 半透明材质测试 / Partial-transparency test

**本仓库原创练习配方 · 未执行 · 不对应来源样张的原始输入**

## 中文指令

```text
生成一个浅琥珀色玻璃茶壶，细壶嘴、圆把手，壶身能够透出背景。独立物体，无桌面、无文字、无环境。若服务支持，请保留壶身的部分透明度，导出带 Alpha 通道的 PNG。不要用乳白填充模拟透明。
```

## English prompt

```text
Create an isolated pale amber glass teapot with a narrow spout and round handle. The background must show through its body. No tabletop, lettering or environment. If supported, preserve partial transparency in the body and export an alpha-channel PNG. Do not simulate transparency with a milky fill.
```

## 验收项

1. 检查 Alpha 是否存在介于完全透明与完全不透明之间的值。
2. 叠在彩色方格上，检查背景是否能透过壶身。
3. 检查壶把与壶嘴内部的空洞是否清晰。

如服务没有对应模型或输出开关，不以提示词文字代替服务能力。生成结果需要人工检查。
