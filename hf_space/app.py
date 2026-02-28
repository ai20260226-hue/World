import json
from pathlib import Path

import gradio as gr


def _latest_artifacts(limit: int = 20):
    base = Path("artifacts")
    if not base.exists():
        return []
    files = sorted(base.rglob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
    return [str(p) for p in files[:limit]]


def _queue_status():
    inbox = len(list(Path("tasks/inbox").glob("*.json")))
    done = len(list(Path("tasks/done").glob("*.json")))
    failed = len(list(Path("tasks/failed").glob("*.json")))
    return {"inbox": inbox, "done": done, "failed": failed}


def _read_memory():
    p = Path("memory/company-A-research.json")
    if not p.exists():
        return {"message": "memory file not found"}
    return json.loads(p.read_text(encoding="utf-8"))


def refresh_dashboard():
    status = _queue_status()
    memory = _read_memory()
    artifacts = _latest_artifacts()
    lines = [
        "# HF Space Dashboard (No Local PC)",
        f"- inbox: {status['inbox']}",
        f"- done: {status['done']}",
        f"- failed: {status['failed']}",
        "",
        "## memory",
        "```json",
        json.dumps(memory, ensure_ascii=False, indent=2),
        "```",
        "",
        "## latest artifacts",
    ]
    lines.extend([f"- {a}" for a in artifacts] or ["- none"])
    return "\n".join(lines)


with gr.Blocks(title="HF Multi-Agent Dashboard") as demo:
    gr.Markdown("## HF上で運用するAIワーカーダッシュボード")
    output = gr.Markdown(refresh_dashboard())
    refresh_btn = gr.Button("Refresh")
    refresh_btn.click(fn=refresh_dashboard, outputs=output)


demo.launch(server_name="0.0.0.0", server_port=7860)
