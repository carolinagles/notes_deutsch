from __future__ import annotations

import json
import re
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components


BASE_DIR = Path(__file__).parent
SOURCE_FILE = BASE_DIR / "assets" / "Deutsch lernen.html"

st.set_page_config(
    page_title="Deutsch lernen",
    page_icon="ä",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def prepare_html(source: str) -> str:
    """Load the original self-contained app and remove the requested verb intro."""
    match = re.search(
        r'(<script\s+type="application/json"\s+id="src">)(.*?)(</script>)',
        source,
        flags=re.DOTALL,
    )
    if not match:
        return source

    sections = json.loads(match.group(2))
    verb_page = sections.get("verben")
    if verb_page:
        sections["verben"] = re.sub(
            r'<p class="lead">.*?</p>\s*',
            "",
            verb_page,
            count=1,
            flags=re.DOTALL,
        )

    embedded_json = json.dumps(sections, ensure_ascii=False)
    embedded_json = (
        embedded_json.replace("&", r"\u0026")
        .replace("<", r"\u003c")
        .replace(">", r"\u003e")
    )
    return source[: match.start(2)] + embedded_json + source[match.end(2) :]


if not SOURCE_FILE.exists():
    st.error("No se encontró el archivo `assets/Deutsch lernen.html`.")
    st.stop()

page_html = prepare_html(SOURCE_FILE.read_text(encoding="utf-8"))

st.markdown(
    """
    <style>
      [data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu, footer {
        display: none !important;
      }
      [data-testid="stAppViewContainer"], [data-testid="stMain"] {
        background: #FBFAFD !important;
      }
      [data-testid="stMainBlockContainer"], .block-container {
        max-width: none !important;
        padding: 0 !important;
        margin: 0 !important;
      }
      [data-testid="stVerticalBlock"] { gap: 0 !important; }
      iframe { border: 0 !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Keep the supplied HTML and its JavaScript in one sandboxed frame so the
# original layout, navigation, lesson content, and interactions are preserved.
components.html(page_html, height=1100, scrolling=True)
