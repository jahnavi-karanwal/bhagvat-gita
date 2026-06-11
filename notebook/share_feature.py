from __future__ import annotations

import json
import time
import uuid
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, Optional

try:
    import ipywidgets as widgets  # type: ignore
    from IPython.display import Javascript, Markdown, display  # type: ignore
except ModuleNotFoundError:  # pragma: no cover
    widgets = None  # type: ignore[assignment]
    Javascript = None  # type: ignore[assignment]
    Markdown = None  # type: ignore[assignment]
    display = None  # type: ignore[assignment]


_REPO_ROOT = Path(__file__).resolve().parents[1]
_DATA_DIR = _REPO_ROOT / "data"
_SHARES_DIR = _DATA_DIR / "shares"
_ANALYTICS_DIR = _DATA_DIR / "analytics"
_EVENTS_PATH = _ANALYTICS_DIR / "events.jsonl"


def _now_ms() -> int:
    return int(time.time() * 1000)


def _ensure_dirs() -> None:
    _SHARES_DIR.mkdir(parents=True, exist_ok=True)
    _ANALYTICS_DIR.mkdir(parents=True, exist_ok=True)


def log_event(event: str, props: Optional[Dict[str, Any]] = None) -> None:
    _ensure_dirs()
    payload = {"ts_ms": _now_ms(), "event": event, "props": props or {}}
    with _EVENTS_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")


@dataclass(frozen=True)
class ShareCard:
    token: str
    question: str
    answer: str
    created_ts_ms: int
    meta: Dict[str, Any]


def _new_token() -> str:
    return uuid.uuid4().hex[:10]


def _share_path(token: str) -> Path:
    return _SHARES_DIR / f"{token}.json"


def save_share(question: str, answer: str, meta: Optional[Dict[str, Any]] = None) -> ShareCard:
    _ensure_dirs()
    token = _new_token()
    card = ShareCard(
        token=token,
        question=(question or "").strip(),
        answer=(answer or "").strip(),
        created_ts_ms=_now_ms(),
        meta=meta or {},
    )
    _share_path(token).write_text(
        json.dumps(asdict(card), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return card


def load_share(token: str) -> ShareCard:
    payload = json.loads(_share_path(token).read_text(encoding="utf-8"))
    return ShareCard(
        token=payload["token"],
        question=payload.get("question", ""),
        answer=payload.get("answer", ""),
        created_ts_ms=int(payload.get("created_ts_ms") or 0),
        meta=dict(payload.get("meta") or {}),
    )


def render_share_markdown(card: ShareCard) -> str:
    q = card.question.strip()
    a = card.answer.strip()
    lines = ["### Bhagavad Gita Wisdom (RAG)", ""]
    if q:
        lines += [f"**Q:** {q}", ""]
    if a:
        lines += [f"**A:** {a}", ""]
    lines += [f"_Share token:_ `{card.token}`"]
    return "\n".join(lines)


def _copy_to_clipboard_js(text: str) -> Javascript:
    if Javascript is None:  # pragma: no cover
        raise RuntimeError("Clipboard copy requires IPython/Jupyter.")
    escaped = json.dumps(text, ensure_ascii=False)
    return Javascript(
        "\n".join(
            [
                "(async function(){",
                f"  const text = {escaped};",
                "  try {",
                "    await navigator.clipboard.writeText(text);",
                "  } catch (e) {",
                "    const ta = document.createElement('textarea');",
                "    ta.value = text; document.body.appendChild(ta);",
                "    ta.select(); document.execCommand('copy');",
                "    document.body.removeChild(ta);",
                "  }",
                "})();",
            ]
        )
    )


def share_widget(*, question: str, answer: str, meta: Optional[Dict[str, Any]] = None):
    """
    UI entrypoint for the viral loop:
      - Save: persists a share token under data/shares/
      - Copy: copies a shareable Markdown card to clipboard
    """
    if widgets is None or display is None or Markdown is None:  # pragma: no cover
        raise RuntimeError("share_widget requires ipywidgets + IPython (run inside Jupyter).")
    status = widgets.HTML(value="")
    out = widgets.Output()
    btn_save = widgets.Button(description="Save share token", button_style="primary")
    btn_copy = widgets.Button(description="Copy share card")

    state: Dict[str, Any] = {"card": None}

    def _render(card: ShareCard) -> None:
        md = render_share_markdown(card)
        with out:
            out.clear_output()
            display(Markdown(md))

    def _on_save(_btn: widgets.Button) -> None:
        card = save_share(question=question, answer=answer, meta=meta)
        state["card"] = card
        status.value = f"<b>Saved.</b> Share token: <code>{card.token}</code>"
        _render(card)

    def _on_copy(_btn: widgets.Button) -> None:
        card = state.get("card") or save_share(question=question, answer=answer, meta=meta)
        state["card"] = card
        md = render_share_markdown(card)
        display(_copy_to_clipboard_js(md))
        log_event("share_card_copied", {"token": card.token})
        status.value = f"<b>Copied.</b> Share token: <code>{card.token}</code>"
        _render(card)

    btn_save.on_click(_on_save)
    btn_copy.on_click(_on_copy)
    return widgets.VBox([widgets.HBox([btn_save, btn_copy]), status, out])


def open_share(token: str) -> str:
    """Success state: view a saved share card by token (returns Markdown)."""
    card = load_share(token)
    log_event("share_token_opened", {"token": token})
    md = render_share_markdown(card)
    if display is not None and Markdown is not None:  # pragma: no cover
        display(Markdown(md))
    return md
