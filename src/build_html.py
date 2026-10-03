from pathlib import Path
import json
import base64
import hashlib
import html
import layout as campaign


REPO = Path(__file__).resolve().parent.parent
ROOT = REPO / "materials"
ROOT.mkdir(exist_ok=True)

DATA = json.loads(
    (REPO / "content" / "campaign.json").read_text(encoding="utf-8")
)

for attribute, key in [
    ("TITLE", "title"),
    ("TASKS", "tasks"),
    ("STYLES", "styles"),
    ("REWARDS", "poster_rewards"),
    ("CARDTEXT", "card_text"),
]:
    setattr(campaign, attribute, DATA[key])

GIFTS = DATA["gifts"]
ANNOUNCEMENT = DATA["announcement"]

CSS = (REPO / "src" / "campaign.css").read_text(encoding="utf-8")
JS = (REPO / "src" / "interactions.js").read_text(encoding="utf-8")


def file_asset(path, mime, filename=None):
    raw = path.read_bytes()

    return {
        "mime": mime,
        "filename": filename or path.name,
        "base64": base64.b64encode(raw).decode(),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "bytes": len(raw),
    }


def build_html():
    assets = {}

    # 目前页面只显示「线索档案版」
    # 但仓库中的其他版本素材仍然保留
    for style in campaign.STYLES:
        for kind, ext, mime in [
            ("poster", "png", "image/png"),
            ("task-card", "png", "image/png"),
            ("campaign", "pdf", "application/pdf"),
        ]:
            assets[f"{style['id']}-{kind}"] = file_asset(
                ROOT / f"{style['id']}-{kind}.{ext}",
                mime,
                "Maven-概念侦探社-"
                + style["name"]
                + "-"
                + {
                    "poster": "海报",
                    "task-card": "任务卡",
                    "campaign": "海报与任务卡",
                }[kind]
                + f".{ext}",
            )

    # 群公告
    (ROOT / "群公告-定稿.txt").write_text(
        ANNOUNCEMENT,
        encoding="utf-8-sig",
    )

    # 提问句
    promptdoc = (
        "Maven 概念侦探社｜提问句\n\n"
        + "\n\n".join(
            f"{task['n']:02} {task['title']}\n"
            + "\n\n".join(
                task[key]
                for key in ["prompt", "extra"]
                if task.get(key)
            )
            for task in campaign.TASKS
            if task.get("prompt")
        )
    )

    (ROOT / "提问句-定稿.txt").write_text(
        promptdoc,
        encoding="utf-8-sig",
    )

    assets["notice"] = file_asset(
        ROOT / "群公告-定稿.txt",
        "text/plain;charset=utf-8",
    )

    assets["prompts"] = file_asset(
        ROOT / "提问句-定稿.txt",
        "text/plain;charset=utf-8",
    )

    prompts = {}
    steps = []

    for task in campaign.TASKS:
        extra = ""

        for key in ["prompt", "extra"]:
            if task.get(key):
                prompt_id = f"p{task['n']}-{key}"
                prompts[prompt_id] = task[key]

                extra += (
                    '<div class="promptbox">'
                    f'<p id="{prompt_id}" data-prompt="{prompt_id}">'
                    f"{html.escape(task[key])}"
                    "</p>"
                    f'<button class="copy" type="button" '
                    f'data-copy="{prompt_id}">复制这句</button>'
                    "</div>"
                )

        steps.append(
            f"""
            <details class="step" {"open" if task["n"] == 1 else ""}>
                <summary>
                    <span class="number">{task["n"]:02}</span>
                    <span>
                        <span class="steptitle">{task["title"]}</span>
                        <span class="short">{task["short"]}</span>
                    </span>
                </summary>
                <div class="stepbody">
                    <span class="channel">{task["channel"]}</span>
                    <p>{task["body"]}</p>
                    <p class="help">{task["help"]}</p>
                    {extra}
                    <p class="done">完成：{task["done"]}</p>
                </div>
            </details>
            """
        )

    # 当前页面只使用 archive
    archive = next(
        style
        for style in campaign.STYLES
        if style["id"] == "archive"
    )

    variants = {
        "archive": {
            "name": archive["name"],
            "colors": {
                "bg": archive["bg"],
                "ink": archive["ink"],
                "muted": archive["muted"],
                "accent": archive["accent"],
                "line": archive["line"],
                "panel": archive["panel"],
                "secondary": archive["secondary"],
                "buttonink": "#ffffff",
            },
        }
    }

    initial = ";".join(
        f"--{key}:{value}"
        for key, value in variants["archive"]["colors"].items()
    )

    # 礼物
    gifts = ""

    for group in ["每日随机礼", "结案大奖"]:
        rows = "".join(
            f'<li><span>{gift["name"]}</span></li>'
            for gift in GIFTS
            if gift["group"] == group
        )

        if group == "每日随机礼":
            description = "每通过一项，增加一次每日抽奖机会。"
        else:
            description = "六项全部完成，额外参加大奖抽奖。"

        gifts += f"""
        <article class="giftgroup">
            <h3>{group}</h3>
            <p>{description}</p>
            <ul>{rows}</ul>
        </article>
        """

    def dump(value):
        return json.dumps(
            value,
            ensure_ascii=False,
            separators=(",", ":"),
        ).replace("<", "\\u003c")

    page = f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="light dark">

<meta
    name="description"
    content="Maven 概念侦探社：查考试安排、比较概念、做小测、画关系图。"
>

<title>Maven 概念侦探社</title>

<style>
:root {{
    {initial}
}}

{CSS}
</style>
</head>

<body>

<header>
    <a class="brand" href="#top">Maven 概念侦探社</a>

    <nav aria-label="页面导航">
        <a href="#clues">任务</a>
        <a href="#gifts">礼物</a>
        <a href="#my-case">我的案件</a>
        <a href="#downloads">下载</a>
    </nav>
</header>


<main id="top">

<section class="hero">

    <div>

        <p class="audience">
            香港中文大学（深圳） · 营销课程期中复习
        </p>

        <h1>概念侦探社</h1>

        <a class="primary" href="#clues">
            接下这桩小案
        </a>

        <p class="note">
            用自己的学校账号参加，已有账号直接登录。
        </p>

    </div>


    <details class="poster" id="poster" open>

        <summary>
            查看活动海报
        </summary>

        <img
            id="poster-image"
            alt="Maven 概念侦探社活动海报"
            width="1080"
            height="1440"
        >

    </details>

</section>


<section
    class="rewardstrip"
    aria-label="参与奖励"
>

    <div>
        <small>每一项通过审核</small>
        <strong>每日抽奖机会 +1</strong>
    </div>

    <div>
        <small>六项全部完成</small>
        <strong>额外参加大奖抽奖</strong>
    </div>

</section>


<section id="clues">

    <div class="tasks">
        {"".join(steps)}
    </div>

</section>


<section class="case-entry" id="my-case">

    <div class="case-entry-content">

        <p class="audience">
            CASE FILE / MY CASE
        </p>

        <h2>我的案件</h2>

        <p>
            完成任务后，提交学习结果截图。
            审核通过后，即可获得每日抽奖机会。
        </p>

        <p class="note">
            使用学校邮箱登录，查看任务审核状态与抽奖资格。
        </p>

    </div>

    <a class="primary" href="src/my_case.html">
        进入我的案件
    </a>

</section>


<section class="gifts" id="gifts">

    <h2>查线索，也有小礼物</h2>

    <div class="giftgroups">
        {gifts}
    </div>


    <ul class="rules">

        <li>
            每完成一项并通过审核，获得一次每日抽奖机会；
            同一任务每人只计一次。
        </li>

        <li>
            每天随机开奖，不用自己选礼物。
            六项全部完成，额外参加大奖抽奖。
        </li>

        <li>
            保存学习结果截图，按课程群通知提交与核验。
            请勿提交密码、二维码或微信配对码。
        </li>

    </ul>

</section>


<section class="downloads" id="downloads">

    <h2>把这份小案卷带走</h2>

    <p class="note">
        当前：<strong id="download-edition">线索档案版</strong>。
    </p>


    <div class="downloadbuttons">

        <button
            class="secondary"
            data-download="poster"
            type="button"
        >
            下载海报 PNG
        </button>


        <button
            class="secondary"
            data-download="task-card"
            type="button"
        >
            下载任务卡 PNG
        </button>


        <button
            class="secondary"
            data-download="campaign"
            type="button"
        >
            下载海报与任务卡 PDF
        </button>


        <button
            class="secondary"
            data-download="poster"
            data-preview="true"
            type="button"
        >
            查看／保存海报
        </button>


        <button
            class="secondary"
            data-download="notice"
            type="button"
        >
            下载群公告文案
        </button>


        <button
            class="secondary"
            data-download="prompts"
            type="button"
        >
            下载提问句
        </button>

    </div>


    <p
        id="download-status"
        class="downloadstatus"
        role="status"
        aria-live="polite"
    ></p>


    <p class="note">
        所有材料都在这一个文件里，无需其他附件。
        微信内若不能打开或下载，请先保存文件，再用浏览器打开。
    </p>

</section>


<section class="closing">

    <a
        class="primary"
        href="https://ask-maven.com/"
        target="_blank"
        rel="noopener"
    >
        去 Maven 开始
    </a>

</section>

</main>


<footer>
    Missing course files? Please contact your TA.<br>
    活动时间、任务提交、开奖与领取安排见课程群通知。
</footer>


<noscript>
    <p style="padding:20px">
        请使用支持 JavaScript 的浏览器打开，
        以显示海报、复制提问句和下载内置材料。
        任务与活动规则可直接阅读。
    </p>
</noscript>


<script type="application/json" id="material-data">
    {dump(assets)}
</script>


<script type="application/json" id="variant-data">
    {dump(variants)}
</script>


<script type="application/json" id="prompt-data">
    {dump(prompts)}
</script>


<script>
{JS}
</script>

</body>
</html>
"""

    output = REPO / "index.html"

    output.write_text(
        page,
        encoding="utf-8",
    )

    manifest = {
        key: {
            item_key: item_value
            for item_key, item_value in value.items()
            if item_key != "base64"
        }
        for key, value in assets.items()
    }

    docs = REPO / "docs"
    docs.mkdir(exist_ok=True)

    (docs / "embedded-materials.json").write_text(
        json.dumps(
            manifest,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(
        "Standalone HTML bytes:",
        output.stat().st_size,
    )

    print(
        "Embedded downloads:",
        len(assets),
    )


if __name__ == "__main__":
    build_html()
