# 编辑与验收

1. 修改 `content/campaign.json`。`tasks` 是六步任务与提示词；`card_text` 是任务卡短文；`styles` 是三版配色和海报标题；`poster_rewards` 是海报奖励摘要；`gifts` 是网页奖品清单；`announcement` 是群公告。网页任务全文和纸卡短文分别编辑，避免短卡溢出。
2. 修改 `src/campaign.css` 调整网页布局；修改 `src/interactions.js` 调整页面交互。它们会在构建时嵌入 `index.html`，不要只改成品 HTML。
3. 修改 `src/layout.py` 调整海报／任务卡的字号、位置、留白和背景。坐标使用 540 ×720 pt 的画布，PNG 渲染为 1080 ×1440。
4. 需要改图时，替换 `assets/illustrations/` 中对应原图。建议保留文件名和 3:4 比例。参考图与生成提示词见本目录；当前没有分层 PSD、AI 或可编辑 SVG。
5. 完整运行 `python src/rebuild.py`，再运行 `node src/check-standalone.cjs`。

礼品名称和数量修改后，也检查群公告、海报奖励摘要和 `src/build_html.py` 的固定规则文字。抽奖规则涉及任务资格与开奖方式，不是单纯改奖品数量。未给定的日期、问卷链接、领取地点没有编造入口。

验收时打开最新的三张海报与三张任务卡，确认无重叠、缺字或换行溢出；检查网页窄屏与桌面布局；切换三版并逐个下载 PNG/PDF/TXT；确认后续提问句沿用第三步的两个概念，且没有概念占位符；检查浏览器复制被拒绝时仍能手动复制。

活动任务按课程群通知审核；涉及账号和引用来源的实际流程在 Maven 网站完成。不要把静态页面改成自动收集密码、微信配对码或学生对话的入口。

## 字体派生文件再生成

仓库内包含源可变字体及两份静态字体，正常重建无需 fonttools。若要更换字重，可安装 `fonttools==4.66.1`，使用 `fontTools.varLib.instancer` 对 `assets/fonts/NotoSansSC-variable.ttf` 的 `wght` 轴固定为 400／700。静态派生版需遵循 OFL 并避免使用保留字体名 `Source`。记录新的字体来源与 SHA。
