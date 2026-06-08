import plotly.graph_objects as go

from resume_matcher.themes import THEMES


def score_card(label: str, value: float, css_class: str) -> str:
    return (f'<div class="score-card {css_class}">'
            f'<div class="label">{label}</div>'
            f'<div class="value">{value:.0f}%</div></div>')


def chips(skills, css_class: str) -> str:
    if not skills:
        return '<span class="empty-chip">None</span>'
    return "".join(f'<span class="chip {css_class}">{s}</span>'
                   for s in sorted(skills))


def build_gauge(score: float, theme_name: str) -> go.Figure:
    theme = THEMES[theme_name]
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number={"suffix": "%", "font": {"color": theme["text"], "size": 34}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": "#94a3b8"},
            "bar": {"color": "#8b5cf6"},
            "bgcolor": "rgba(0,0,0,0)",
            "borderwidth": 0,
            "steps": [
                {"range": [0, 40], "color": "rgba(239,68,68,0.25)"},
                {"range": [40, 70], "color": "rgba(234,179,8,0.25)"},
                {"range": [70, 100], "color": "rgba(34,197,94,0.25)"},
            ],
        },
    ))
    fig.update_layout(height=300, paper_bgcolor="rgba(0,0,0,0)",
                      font={"color": theme["text"]},
                      margin=dict(l=30, r=30, t=30, b=10))
    return fig


def build_bar(matched, missing, theme_name: str) -> go.Figure:
    theme = THEMES[theme_name]
    fig = go.Figure(go.Bar(
        x=["Matched", "Missing"],
        y=[len(matched), len(missing)],
        marker_color=["#22c55e", "#ef4444"],
        text=[len(matched), len(missing)],
        textposition="outside",
        textfont={"color": theme["text"], "size": 16},
    ))
    fig.update_layout(height=300, paper_bgcolor="rgba(0,0,0,0)",
                      plot_bgcolor="rgba(0,0,0,0)",
                      font={"color": theme["text"]},
                      yaxis={"gridcolor": "rgba(148,163,184,0.2)",
                             "title": "Number of skills"},
                      margin=dict(l=20, r=20, t=30, b=20))
    return fig
