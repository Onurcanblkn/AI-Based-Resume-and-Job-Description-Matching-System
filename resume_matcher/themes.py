THEMES = {
    "Dark": {
        "background": "#101820",
        "surface": "#111827",
        "surface_alt": "#1f2937",
        "panel": "#16212d",
        "text": "#f3f4f6",
        "muted": "#a3adba",
        "border": "rgba(148,163,184,0.22)",
        "input": "#111827",
        "input_text": "#e5e7eb",
        "hero_start": "#0f766e",
        "hero_mid": "#1d4ed8",
        "hero_end": "#334155",
        "shadow": "rgba(0,0,0,0.32)",
        "matched_text": "#86efac",
        "missing_text": "#fca5a5",
        "rec_bg": "rgba(20,184,166,0.10)",
        "rec_border": "rgba(45,212,191,0.32)",
    },
    "Light": {
        "background": "#f8fafc",
        "surface": "#ffffff",
        "surface_alt": "#eef6f6",
        "panel": "#f1f5f9",
        "text": "#111827",
        "muted": "#64748b",
        "border": "rgba(100,116,139,0.24)",
        "input": "#ffffff",
        "input_text": "#111827",
        "hero_start": "#0f766e",
        "hero_mid": "#2563eb",
        "hero_end": "#475569",
        "shadow": "rgba(15,23,42,0.12)",
        "matched_text": "#15803d",
        "missing_text": "#b91c1c",
        "rec_bg": "rgba(15,118,110,0.07)",
        "rec_border": "rgba(15,118,110,0.22)",
    },
}


def get_theme_css(theme_name: str) -> str:
    theme = THEMES[theme_name]
    css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: {theme["background"]}; color: {theme["text"]}; }
.block-container { padding-top: 1.25rem; max-width: 1120px; }
#MainMenu, footer, header, [data-testid="stToolbar"], [data-testid="stDecoration"] {
  display: none;
}

.app-header {
  display: flex; align-items: center; justify-content: space-between; gap: 16px;
  margin-bottom: 18px;
}
.brand-block {
  display: flex; flex-direction: column; gap: 2px;
}
.brand-title {
  color: {theme["text"]}; font-size: 18px; font-weight: 800;
}
.brand-subtitle {
  color: {theme["muted"]}; font-size: 13px; font-weight: 600;
}

.theme-panel {
  background: {theme["surface"]}; border: 1px solid {theme["border"]};
  border-radius: 8px; padding: 12px 14px; margin: -10px 0 18px 0;
  box-shadow: 0 8px 18px {theme["shadow"]};
}
.theme-panel-title {
  color: {theme["muted"]}; font-size: 12px; font-weight: 800;
  margin-bottom: 6px;
  text-transform: uppercase;
}

.hero {
  background: linear-gradient(135deg, {theme["hero_start"]} 0%, {theme["hero_mid"]} 52%, {theme["hero_end"]} 100%);
  padding: 30px 34px; border-radius: 8px; margin-bottom: 24px;
  box-shadow: 0 14px 32px {theme["shadow"]};
}
.hero h1 { color: #fff; font-size: 32px; font-weight: 800; margin: 0; }
.hero p {
  color: rgba(255,255,255,0.9); font-size: 15px; line-height: 1.6;
  margin: 10px 0 0 0; max-width: 760px;
}
.hero .tag {
  display: inline-block; background: rgba(255,255,255,0.18); color: #fff;
  padding: 4px 12px; border-radius: 999px; font-size: 12px; font-weight: 700;
  margin-bottom: 14px;
}

.workflow-row {
  display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 14px;
  margin: -8px 0 12px 0;
}
.workflow-item {
  background: {theme["surface"]}; border: 1px solid {theme["border"]};
  border-radius: 8px; padding: 14px 16px; box-shadow: 0 8px 18px {theme["shadow"]};
}
.workflow-label {
  color: {theme["muted"]}; font-size: 12px; font-weight: 800;
  text-transform: uppercase; margin-bottom: 4px;
}
.workflow-title {
  color: {theme["text"]}; font-size: 15px; font-weight: 800;
}

.score-card {
  border-radius: 8px; padding: 22px; text-align: center; color: #fff;
  box-shadow: 0 10px 24px {theme["shadow"]};
}
.score-card .label { font-size: 13px; font-weight: 600; opacity: .9; text-transform: uppercase; }
.score-card .value { font-size: 40px; font-weight: 800; margin-top: 6px; }
.sc-blue   { background: linear-gradient(135deg,#0ea5e9,#2563eb); }
.sc-purple { background: linear-gradient(135deg,#8b5cf6,#7c3aed); }
.sc-green  { background: linear-gradient(135deg,#10b981,#16a34a); }

.chip {
  display: inline-block; padding: 7px 14px; margin: 5px; border-radius: 8px;
  font-size: 14px; font-weight: 600;
}
.chip-matched { background: rgba(34,197,94,0.14); color: {theme["matched_text"]}; border: 1px solid rgba(34,197,94,0.55); }
.chip-missing { background: rgba(239,68,68,0.11); color: {theme["missing_text"]}; border: 1px solid rgba(239,68,68,0.5); }
.empty-chip { color: {theme["muted"]}; }

.section-title { font-size: 18px; font-weight: 800; margin: 24px 0 10px 0; color: {theme["text"]}; }

.rec-box {
  background: {theme["rec_bg"]}; border: 1px solid {theme["rec_border"]};
  border-radius: 8px; padding: 20px 22px; color: {theme["text"]};
  font-size: 15px; line-height: 1.6;
}

.stButton > button, .stDownloadButton > button {
  background: linear-gradient(135deg,{theme["hero_mid"]},{theme["hero_end"]});
  color: #fff; border: none; border-radius: 8px; padding: 12px 0;
  font-size: 16px; font-weight: 700; width: 100%;
  box-shadow: 0 8px 18px {theme["shadow"]};
}
.stButton > button:hover, .stDownloadButton > button:hover {
  filter: brightness(1.06); color: #fff;
}

div[data-testid="stFileUploader"], div[data-testid="stTextArea"] textarea {
  background: {theme["input"]}; color: {theme["input_text"]};
}
div[data-testid="stFileUploader"] section,
div[data-testid="stFileUploaderDropzone"] {
  background: {theme["surface"]};
  border: 1px solid {theme["border"]};
  border-radius: 8px;
  color: {theme["text"]};
}
div[data-testid="stFileUploader"] section *,
div[data-testid="stFileUploaderDropzone"] * {
  color: {theme["text"]};
}
div[data-testid="stFileUploader"] small,
div[data-testid="stFileUploaderDropzone"] small {
  color: {theme["muted"]};
}
div[data-testid="stFileUploader"] button,
div[data-testid="stFileUploaderDropzone"] button {
  background: {theme["surface_alt"]};
  border: 1px solid {theme["border"]};
  color: {theme["text"]};
  border-radius: 6px;
  font-weight: 700;
}
div[data-testid="stFileUploader"] button *,
div[data-testid="stFileUploaderDropzone"] button * {
  color: {theme["text"]};
}
div[data-testid="stFileUploader"] svg,
div[data-testid="stFileUploaderDropzone"] svg {
  color: {theme["text"]};
  fill: currentColor;
}
div[data-testid="stTextArea"] textarea {
  border: 1px solid {theme["border"]}; border-radius: 8px;
}
div[data-testid="stMarkdownContainer"] p, label, .stRadio label {
  color: {theme["text"]};
}
div[role="radiogroup"] {
  gap: 12px;
}
div[role="radiogroup"] label {
  background: {theme["surface_alt"]}; border: 1px solid {theme["border"]};
  border-radius: 6px; padding: 8px 12px; margin-right: 8px;
}
@media (max-width: 760px) {
  .app-header { flex-direction: column; align-items: stretch; }
  .workflow-row { grid-template-columns: 1fr; }
  .hero h1 { font-size: 26px; }
}
</style>
"""
    for key, value in theme.items():
        css = css.replace('{theme["' + key + '"]}', value)
    return css
