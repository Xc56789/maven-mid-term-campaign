# Maven mid-term campaign

「Maven 概念侦探社」活动材料：线索档案版、夜间调查版、校园社团版。

## 直接使用

下载根目录的 **[index.html](index.html)**，保存后用浏览器打开。它是一个约 25 MB 的独立文件：图片、三版海报、任务卡、PDF 和两份文案均内置，可直接转发，不需要服务器或同目录附件。

在页面切换视觉版本，再点击下载按钮，即可保存相应版本的材料。微信文件预览器可能限制 HTML 脚本或下载；这种情况下先保存文件，再用系统浏览器打开。页面适配手机与电脑，但尚未做真机浏览器验收。

本页提供活动指引和提问句；真正的学习互动在学生自己的 [Maven](https://ask-maven.com/) 课程中进行。任务审核、开奖和发奖按课程群通知进行。

## 文件地图

| 文件或目录 | 用途 |
| --- | --- |
| `index.html` | 当前独立活动页，内置 11 份可下载材料 |
| `materials/` | 三版 PNG 海报、PNG 任务卡、双页 PDF；群公告与提问句 TXT |
| `content/campaign.json` | 可编辑的任务、提示词、礼品配置、视觉主题、卡片文本和群公告 |
| `src/campaign.css` | 页面样式与手机布局 |
| `src/interactions.js` | 视觉切换、提问句复制与下载逻辑 |
| `src/layout.py` | 海报和任务卡的矢量排版、字体选择 |
| `src/build_html.py` | 把文案、样式、脚本及下载材料嵌入 HTML |
| `src/rebuild.py` | 一条命令重建 PDF、PNG 和独立 HTML |
| `src/check-standalone.cjs` | 内容、交互和内置下载完整性检查 |
| `assets/illustrations/` | 三张生成主视觉原始 PNG |
| `assets/references/` | 用户提供的 6 张品牌／礼品参考图与原活动 PDF |
| `assets/fonts/` | 可分发字体、原始可变字体、静态派生字体及 OFL 许可 |
| `docs/` | 编辑说明、插画提示词、来源、检查记录和文件哈希 |

## 修改并重建

需要 Python 3.11+、Node.js 18+ 和 Poppler 的 `pdftoppm`。

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python src/rebuild.py
node src/check-standalone.cjs
```

如果 Poppler 不在 PATH，可以设置 `PDFTOPPM` 为 `pdftoppm` 的完整路径。重建脚本在缺少渲染器时会停止并提示，避免只改 PDF 却留下旧 PNG。

仅改网页样式或脚本、无需重画海报时：

```bash
python src/rebuild.py --html-only
node src/check-standalone.cjs
```

若改了任务、礼品、海报排版或插画，运行完整重建，并检查全部六张 PNG。`--html-only` 不会更新海报或任务卡上的文字。

### 字体与复现范围

提交的现有 PDF／PNG 使用 Microsoft YaHei 与 Bricolage Grotesque。Windows 安装有微软雅黑时，脚本默认使用本机字体，保留原字体和排版。Microsoft 字体文件没有上传。

其他系统使用仓库内的 OFL 字体：Noto Sans SC 的 400／700 静态派生版与 Bricolage Grotesque。也可设置 `MAVEN_FONT=licensed` 强制使用它们。这个模式可独立构建，但中文字体轮廓与原成品有所区别，应检查换行和间距。PDF 元数据、渲染器版本与平台也可能导致字节差异；不把重新生成 PDF 的 SHA 相同当作验收要求。

现有插画可原样复用。用保存的提示词重新生成插画具有随机性，不保证逐像素复现；这里提供 PNG 原图，没有不存在的 PSD 或分层矢量源文件。

## 礼品配置

沿用原活动示例：Maven Sticker 300 张；Maven 定制帆布袋 120 个；会饮／一瓯茶代金券 50 份；攀岩／健身握力环 30 个；Tangle 30 个；一次性胶片相机、影视飓风复古相机充电宝、abib 防晒各 2 份。

每项任务通过审核获得一次每日抽奖机会，同一任务每人计一次；任意一项通过可领贴纸一张，限量先到先得；六项全完成额外获得一次结案抽奖资格，活动末抽出六位获奖者。原 PDF 的数量与预算是计划值，采购、活动日期和领取安排仍以正式通知为准。参考图中的钥匙扣没有加入奖品承诺。

## 检查范围

检查脚本验证主题切换、任务文案、复制回退、PNG/PDF/TXT 下载内容和所有内置文件 SHA-256。它使用 Node VM 和 DOM 桩，不是浏览器或真机测试。原 PDF 六页已渲染查看；仓库发布前还做了独立目录重建检查，见 `docs/reproduction-check.json`。

仓库仅含活动材料，不含 Maven 应用源码、课程资料、学生数据、账户凭据或服务器配置。建立本仓库没有部署或修改 Maven 生产网站。

字体许可、参考来源与插画生成记录见 [NOTICE.md](NOTICE.md) 和 [docs/provenance.md](docs/provenance.md)。
