from __future__ import annotations

import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTENT_DIR = ROOT / "content"
SRC_DIR = ROOT / "src"
DOCS_DIR = ROOT / "docs"

CAMPAIGN_FILE = CONTENT_DIR / "campaign.json"
OUTPUT_FILE = ROOT / "index.html"
EMBEDDED_FILE = DOCS_DIR / "embedded-materials.json"


def load_campaign() -> dict:
    with CAMPAIGN_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


def esc(value) -> str:
    return html.escape(str(value), quote=True)


def render_styles(campaign: dict) -> str:
    styles = campaign.get("styles", [])

    if not styles:
        return ""

    cards = []

    for style in styles:
        style_id = esc(style.get("id", ""))
        name = esc(style.get("name", ""))
        description = esc(style.get("description", ""))

        cards.append(
            f"""
            <article class="style-card" data-style="{style_id}">
                <div class="style-card-label">CASE STYLE</div>
                <h3>{name}</h3>
                <p>{description}</p>
            </article>
            """
        )

    return f"""
    <section class="section style-section">
        <div class="section-label">01 / CASE FILE</div>
        <h2>线索档案</h2>
        <div class="style-grid">
            {''.join(cards)}
        </div>
    </section>
    """


def render_announcement(campaign: dict) -> str:
    announcement = campaign.get("announcement", {})

    title = esc(announcement.get("title", "Maven Mid-Term Campaign"))
    subtitle = esc(announcement.get("subtitle", ""))
    intro = esc(announcement.get("intro", ""))

    items = announcement.get("items", [])

    item_html = []

    for index, item in enumerate(items, start=1):
        if isinstance(item, dict):
            item_title = esc(item.get("title", ""))
            item_description = esc(item.get("description", ""))
        else:
            item_title = esc(item)
            item_description = ""

        item_html.append(
            f"""
            <article class="announcement-item">
                <div class="announcement-number">
                    {index:02d}
                </div>
                <div>
                    <h3>{item_title}</h3>
                    <p>{item_description}</p>
                </div>
            </article>
            """
        )

    return f"""
    <section class="section">
        <div class="section-label">02 / INVESTIGATION BRIEF</div>

        <div class="section-heading">
            <div>
                <h2>{title}</h2>
                <div class="section-subtitle">{subtitle}</div>
            </div>
        </div>

        <p class="section-intro">{intro}</p>

        <div class="announcement-list">
            {''.join(item_html)}
        </div>
    </section>
    """


def render_rules(campaign: dict) -> str:
    rules = campaign.get("rules", [])

    rule_html = []

    for index, rule in enumerate(rules, start=1):
        rule_html.append(
            f"""
            <div class="rule-item">
                <span class="rule-number">{index:02d}</span>
                <span>{esc(rule)}</span>
            </div>
            """
        )

    return f"""
    <section class="section">
        <div class="section-label">03 / CASE RULES</div>
        <h2>案件规则</h2>

        <div class="rules">
            {''.join(rule_html)}
        </div>
    </section>
    """


def render_tasks(campaign: dict) -> str:
    tasks = campaign.get("tasks", [])

    task_html = []

    for index, task in enumerate(tasks, start=1):
        title = esc(task.get("title", ""))
        description = esc(task.get("description", ""))
        detail = task.get("detail", [])

        detail_html = []

        for line in detail:
            detail_html.append(
                f"<li>{esc(line)}</li>"
            )

        task_html.append(
            f"""
            <article class="task-card">
                <div class="task-top">
                    <div class="task-number">TASK {index:02d}</div>
                    <div class="task-status">CASE CLUE</div>
                </div>

                <h3>{title}</h3>

                <p class="task-description">
                    {description}
                </p>

                <ul class="task-detail">
                    {''.join(detail_html)}
                </ul>
            </article>
            """
        )

    return f"""
    <section class="section">
        <div class="section-label">04 / SIX CLUES</div>
        <h2>六条线索</h2>

        <div class="task-grid">
            {''.join(task_html)}
        </div>
    </section>
    """


def render_rewards(campaign: dict) -> str:
    rewards = campaign.get("poster_rewards", [])

    reward_html = []

    for reward in rewards:
        if isinstance(reward, list):
            parts = [esc(x) for x in reward]
        elif isinstance(reward, dict):
            parts = [
                esc(reward.get("condition", "")),
                esc(reward.get("reward", "")),
                esc(reward.get("description", "")),
            ]
        else:
            parts = [esc(reward)]

        reward_html.append(
            f"""
            <article class="reward-card">
                <div class="reward-main">
                    {''.join(f'<div>{part}</div>' for part in parts)}
                </div>
            </article>
            """
        )

    gifts = campaign.get("gifts", {})

    daily_gifts = gifts.get("daily", [])
    grand_gifts = gifts.get("grand", [])

    daily_html = []

    for gift in daily_gifts:
        if isinstance(gift, dict):
            name = gift.get("name", "")
        else:
            name = gift

        daily_html.append(
            f"""
            <div class="gift-item">
                <span>✦</span>
                <span>{esc(name)}</span>
            </div>
            """
        )

    grand_html = []

    for gift in grand_gifts:
        if isinstance(gift, dict):
            name = gift.get("name", "")
        else:
            name = gift

        grand_html.append(
            f"""
            <div class="gift-item">
                <span>✦</span>
                <span>{esc(name)}</span>
            </div>
            """
        )

    return f"""
    <section class="section">
        <div class="section-label">05 / REWARD RECORD</div>
        <h2>奖励记录</h2>

        <div class="reward-grid">
            {''.join(reward_html)}
        </div>

        <div class="gift-columns">
            <div class="gift-box">
                <div class="gift-label">DAILY RANDOM GIFTS</div>
                <h3>每日随机礼</h3>
                <div class="gift-list">
                    {''.join(daily_html)}
                </div>
            </div>

            <div class="gift-box">
                <div class="gift-label">FINAL CASE PRIZES</div>
                <h3>结案大奖</h3>
                <div class="gift-list">
                    {''.join(grand_html)}
                </div>
            </div>
        </div>
    </section>
    """


def render_my_case() -> str:
    return """
    <section class="my-case-entry">
        <div class="my-case-content">
            <div class="my-case-label">CASE FILE / MY CASE</div>

            <h2>我的案件</h2>

            <p>
                登录你的学校邮箱，提交任务截图，
                查看审核状态，并领取对应的抽奖机会。
            </p>

            <a class="primary-button" href="src/my_case.html">
                进入我的案件 →
            </a>
        </div>

        <div class="my-case-stamp">
            STUDENT<br />
            CASE FILE
        </div>
    </section>
    """


def render_footer() -> str:
    return """
    <footer class="footer">
        <div>MAVEN · MARKETING AI VIRTUAL ENGINE</div>
        <div>CASE CLOSED? NOT YET.</div>
    </footer>
    """


def build_html(campaign: dict) -> str:
    styles_html = render_styles(campaign)
    announcement_html = render_announcement(campaign)
    rules_html = render_rules(campaign)
    tasks_html = render_tasks(campaign)
    rewards_html = render_rewards(campaign)
    my_case_html = render_my_case()
    footer_html = render_footer()

    title = esc(
        campaign.get(
            "title",
            "Maven Mid-Term Campaign"
        )
    )

    subtitle = esc(
        campaign.get(
            "subtitle",
            "Marketing AI Virtual Engine"
        )
    )

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8" />
    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    />

    <title>{title}</title>

    <style>
        :root {{
            --paper: #f0f2ed;
            --ink: #24342f;
            --green: #264e3e;
            --green-light: #dfe7df;
            --line: #8d9a91;
            --muted: #68736d;
            --white: #ffffff;
        }}

        * {{
            box-sizing: border-box;
        }}

        html {{
            scroll-behavior: smooth;
        }}

        body {{
            margin: 0;
            color: var(--ink);
            background:
                linear-gradient(
                    rgba(38, 78, 62, 0.035) 1px,
                    transparent 1px
                ),
                linear-gradient(
                    90deg,
                    rgba(38, 78, 62, 0.035) 1px,
                    transparent 1px
                ),
                var(--paper);
            background-size: 24px 24px;

            font-family:
                -apple-system,
                BlinkMacSystemFont,
                "Segoe UI",
                "PingFang SC",
                "Microsoft YaHei",
                sans-serif;
        }}

        a {{
            color: inherit;
        }}

        .page {{
            width: min(1120px, calc(100% - 32px));
            margin: 0 auto;
        }}

        .hero {{
            min-height: 78vh;
            display: flex;
            align-items: center;
            position: relative;
            padding: 80px 0;
        }}

        .hero-inner {{
            width: 100%;
            position: relative;
            border: 1px solid var(--line);
            background: rgba(255,255,255,0.82);
            padding: clamp(30px, 7vw, 80px);
        }}

        .hero-inner::before {{
            content: "";
            position: absolute;
            left: 0;
            top: 0;
            width: 100%;
            height: 7px;
            background: var(--green);
        }}

        .hero-label {{
            color: var(--muted);
            font-family: Georgia, serif;
            letter-spacing: 0.18em;
            font-size: 13px;
            margin-bottom: 16px;
        }}

        .hero h1 {{
            margin: 0;
            max-width: 900px;
            color: var(--green);
            font-family: Georgia, "Times New Roman", serif;
            font-size: clamp(52px, 10vw, 120px);
            line-height: 0.9;
            letter-spacing: -0.04em;
        }}

        .hero-subtitle {{
            margin-top: 24px;
            color: var(--muted);
            font-size: 15px;
            letter-spacing: 0.08em;
        }}

        .hero-description {{
            max-width: 680px;
            margin-top: 28px;
            color: var(--ink);
            font-size: 16px;
            line-height: 1.9;
        }}

        .hero-stamp {{
            position: absolute;
            right: 34px;
            top: 34px;
            border: 2px solid var(--green);
            color: var(--green);
            padding: 10px 14px;
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 0.12em;
            transform: rotate(-5deg);
        }}

        .hero-button-row {{
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            margin-top: 30px;
        }}

        .primary-button {{
            display: inline-block;
            padding: 13px 20px;
            background: var(--green);
            border: 1px solid var(--green);
            color: white;
            text-decoration: none;
            font-weight: 700;
            font-size: 14px;
        }}

        .primary-button:hover {{
            opacity: 0.9;
        }}

        .section {{
            padding: 80px 0;
            border-top: 1px dashed var(--line);
        }}

        .section-label {{
            color: var(--muted);
            font-size: 12px;
            font-weight: 800;
            letter-spacing: 0.16em;
            margin-bottom: 12px;
        }}

        .section h2 {{
            margin: 0 0 24px;
            color: var(--green);
            font-family: Georgia, "Times New Roman", serif;
            font-size: clamp(34px, 6vw, 58px);
            line-height: 1;
        }}

        .section-subtitle {{
            color: var(--muted);
            font-size: 14px;
        }}

        .section-intro {{
            max-width: 760px;
            color: var(--muted);
            line-height: 1.9;
        }}

        .style-grid {{
            display: grid;
            grid-template-columns: 1fr;
            gap: 16px;
        }}

        .style-card {{
            padding: 24px;
            border: 1px solid var(--line);
            background: rgba(255,255,255,0.7);
        }}

        .style-card-label {{
            color: var(--muted);
            font-size: 10px;
            letter-spacing: 0.16em;
            margin-bottom: 10px;
        }}

        .style-card h3 {{
            margin: 0 0 8px;
            color: var(--green);
            font-family: Georgia, serif;
            font-size: 28px;
        }}

        .style-card p {{
            margin: 0;
            color: var(--muted);
            line-height: 1.7;
        }}

        .announcement-list {{
            border-top: 1px solid var(--line);
        }}

        .announcement-item {{
            display: grid;
            grid-template-columns: 80px 1fr;
            gap: 20px;
            padding: 22px 0;
            border-bottom: 1px solid var(--line);
        }}

        .announcement-number {{
            color: var(--green);
            font-family: Georgia, serif;
            font-size: 25px;
            font-weight: 700;
        }}

        .announcement-item h3 {{
            margin: 0 0 7px;
            font-size: 18px;
        }}

        .announcement-item p {{
            margin: 0;
            color: var(--muted);
            line-height: 1.7;
        }}

        .rules {{
            border: 1px solid var(--line);
            background: rgba(255,255,255,0.72);
        }}

        .rule-item {{
            display: flex;
            gap: 18px;
            padding: 20px;
            border-bottom: 1px dashed var(--line);
            line-height: 1.7;
        }}

        .rule-item:last-child {{
            border-bottom: 0;
        }}

        .rule-number {{
            color: var(--green);
            font-family: Georgia, serif;
            font-weight: 700;
            flex-shrink: 0;
        }}

        .task-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 16px;
        }}

        .task-card {{
            border: 1px solid var(--line);
            background: rgba(255,255,255,0.78);
            padding: 25px;
            min-height: 260px;
        }}

        .task-top {{
            display: flex;
            justify-content: space-between;
            gap: 15px;
            margin-bottom: 22px;
        }}

        .task-number {{
            color: var(--green);
            font-family: Georgia, serif;
            font-weight: 700;
        }}

        .task-status {{
            color: var(--muted);
            font-size: 10px;
            letter-spacing: 0.12em;
        }}

        .task-card h3 {{
            margin: 0 0 12px;
            font-size: 21px;
        }}

        .task-description {{
            color: var(--muted);
            line-height: 1.7;
        }}

        .task-detail {{
            margin: 18px 0 0;
            padding-left: 20px;
            color: var(--ink);
            line-height: 1.8;
            font-size: 13px;
        }}

        .reward-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 16px;
            margin-bottom: 30px;
        }}

        .reward-card {{
            border: 1px solid var(--green);
            background: var(--green-light);
            padding: 22px;
        }}

        .reward-main {{
            display: grid;
            gap: 5px;
            line-height: 1.6;
        }}

        .reward-main div:first-child {{
            font-weight: 700;
        }}

        .gift-columns {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 16px;
        }}

        .gift-box {{
            border: 1px solid var(--line);
            background: rgba(255,255,255,0.72);
            padding: 24px;
        }}

        .gift-label {{
            color: var(--muted);
            font-size: 10px;
            letter-spacing: 0.14em;
            margin-bottom: 8px;
        }}

        .gift-box h3 {{
            margin: 0 0 18px;
            color: var(--green);
            font-family: Georgia, serif;
            font-size: 28px;
        }}

        .gift-list {{
            display: grid;
            gap: 10px;
        }}

        .gift-item {{
            display: flex;
            gap: 10px;
            line-height: 1.6;
        }}

        .gift-item span:first-child {{
            color: var(--green);
        }}

        .my-case-entry {{
            position: relative;
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 30px;
            margin: 30px 0 80px;
            padding: 36px;
            border: 2px solid var(--green);
            background: var(--green);
            color: white;
            overflow: hidden;
        }}

        .my-case-content {{
            max-width: 700px;
        }}

        .my-case-label {{
            font-size: 11px;
            letter-spacing: 0.18em;
            opacity: 0.75;
            margin-bottom: 10px;
        }}

        .my-case-entry h2 {{
            margin: 0 0 12px;
            font-family: Georgia, serif;
            font-size: 42px;
        }}

        .my-case-entry p {{
            margin: 0 0 22px;
            line-height: 1.8;
            opacity: 0.86;
        }}

        .my-case-entry .primary-button {{
            background: var(--paper);
            color: var(--green);
            border-color: var(--paper);
        }}

        .my-case-stamp {{
            flex-shrink: 0;
            border: 2px solid rgba(255,255,255,0.7);
            padding: 13px 16px;
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 0.14em;
            text-align: center;
            transform: rotate(5deg);
        }}

        .footer {{
            padding: 28px 0 45px;
            border-top: 1px dashed var(--line);
            display: flex;
            justify-content: space-between;
            gap: 20px;
            color: var(--muted);
            font-size: 10px;
            letter-spacing: 0.12em;
        }}

        @media (max-width: 720px) {{
            .page {{
                width: min(100% - 20px, 1120px);
            }}

            .hero {{
                min-height: auto;
                padding: 35px 0 50px;
            }}

            .hero-inner {{
                padding: 30px 22px;
            }}

            .hero-stamp {{
                position: static;
                display: inline-block;
                margin-bottom: 25px;
            }}

            .task-grid,
            .reward-grid,
            .gift-columns {{
                grid-template-columns: 1fr;
            }}

            .announcement-item {{
                grid-template-columns: 50px 1fr;
            }}

            .my-case-entry {{
                flex-direction: column;
                align-items: flex-start;
                margin-bottom: 50px;
                padding: 25px;
            }}

            .footer {{
                flex-direction: column;
            }}
        }}
    </style>
</head>

<body>

    <main class="page">

        <section class="hero">
            <div class="hero-inner">

                <div class="hero-stamp">
                    CASE FILE<br />
                    MID-TERM
                </div>

                <div class="hero-label">
                    MAVEN / MARKETING AI VIRTUAL ENGINE
                </div>

                <h1>{title}</h1>

                <div class="hero-subtitle">
                    {subtitle}
                </div>

                <p class="hero-description">
                    一场围绕 Maven 的校园中期任务行动。
                    从课程线索开始，逐步完成六项任务，
                    留下你的证据，等待案件审核。
                </p>

                <div class="hero-button-row">
                    <a
                        class="primary-button"
                        href="src/my_case.html"
                    >
                        进入我的案件 →
                    </a>
                </div>

            </div>
        </section>

        {styles_html}

        {announcement_html}

        {rules_html}

        {tasks_html}

        {rewards_html}

        {my_case_html}

        {footer_html}

    </main>

</body>
</html>
"""


def build_embedded_materials(campaign: dict) -> dict:
    return {
        "styles": campaign.get("styles", []),
        "tasks": campaign.get("tasks", []),
        "rules": campaign.get("rules", []),
        "poster_rewards": campaign.get("poster_rewards", []),
        "gifts": campaign.get("gifts", {}),
    }


def main() -> None:
    campaign = load_campaign()

    OUTPUT_FILE.write_text(
        build_html(campaign),
        encoding="utf-8"
    )

    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    EMBEDDED_FILE.write_text(
        json.dumps(
            build_embedded_materials(campaign),
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )

    print(f"Built: {OUTPUT_FILE}")
    print(f"Built: {EMBEDDED_FILE}")


if __name__ == "__main__":
    main()
