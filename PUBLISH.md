# 发布与验收

本仓库的 GitHub 目标固定为 `RaphaelAI-OpenLab/awesome-seedream-5-5`，默认分支为 `main`。

## 发布前

1. 运行 `python3 scripts/build.py --check` 检查生成一致性。
2. 运行 `python3 scripts/validate.py` 检查数据、路径、双语 README Prompt 优先展示、本地图片与基础凭据扫描。
3. 修改来源媒体时先运行 `python3 scripts/refresh_previews.py` 刷新预览，再运行 `python3 scripts/check_media.py` 更新解码记录。
4. 检查待提交文件，排除缓存、凭据、临时下载文件与未授权媒体归档。

## 发布后

1. 核对默认分支与本地提交 SHA。
2. 等待 GitHub Actions 的“校验案例库”工作流通过。
3. 检查中英文 README、案例链接和投稿表单。

提交、推送、合并与独立网站部署分别报告。本仓库首版没有独立网站部署步骤。
