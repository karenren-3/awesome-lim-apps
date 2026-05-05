import argparse
import json
import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Dict


SYSTEM_PROMPT = (
    "你是资深中文健康科普短视频编导。输出内容必须科学、合规、易懂，"
    "面向中老年与减脂人群，不夸大疗效，不提供医疗诊断。"
)


@dataclass
class TrendItem:
    platform: str
    title: str
    summary: str
    url: str = ""



def load_trends(input_file: Path) -> List[TrendItem]:
    data = json.loads(input_file.read_text(encoding="utf-8"))
    items: List[TrendItem] = []
    for row in data:
        items.append(
            TrendItem(
                platform=row.get("platform", "unknown"),
                title=row["title"],
                summary=row.get("summary", ""),
                url=row.get("url", ""),
            )
        )
    return items



def build_prompt(topic: str, trends: List[TrendItem], count: int) -> str:
    trend_block = "\n".join(
        [f"- [{t.platform}] {t.title} | {t.summary} | {t.url}" for t in trends[:50]]
    )
    return f"""
请基于以下热点线索，生成{count}条短视频方案（中文）。
赛道：{topic}

要求：
1) 只借鉴选题方向，不抄袭原句；
2) 每条包含：标题、3秒钩子、60秒口播脚本、画面分镜(3镜头)、互动问题、封面文案；
3) 必须区分平台风格：视频号/小红书；
4) 给出科学依据关键词（如“蛋白质摄入”“抗阻训练”），避免医疗承诺；
5) 输出JSON数组。

热点线索：
{trend_block}
""".strip()



def call_openai(prompt: str, model: str) -> str:
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise RuntimeError("请先安装 openai: pip install openai") from exc

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("请设置环境变量 OPENAI_API_KEY")

    client = OpenAI(api_key=api_key)
    resp = client.responses.create(
        model=model,
        input=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0.8,
    )
    return resp.output_text



def save_output(raw_text: str, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    file = out_dir / f"content_plan_{ts}.json"
    file.write_text(raw_text, encoding="utf-8")
    return file



def main() -> None:
    parser = argparse.ArgumentParser(description="健康科普短视频选题与脚本生成器（合规版）")
    parser.add_argument("--input", required=True, help="热点输入JSON文件")
    parser.add_argument("--topic", default="运动营养与科学减脂")
    parser.add_argument("--count", type=int, default=10)
    parser.add_argument("--model", default="gpt-4.1-mini")
    parser.add_argument("--out", default="outputs")
    args = parser.parse_args()

    trends = load_trends(Path(args.input))
    prompt = build_prompt(args.topic, trends, args.count)
    raw = call_openai(prompt, args.model)
    out_file = save_output(raw, Path(args.out))
    print(f"已生成: {out_file}")


if __name__ == "__main__":
    main()
