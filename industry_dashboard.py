"""
Industry Intelligence Dashboard — Contractor Foreman
TV Dashboard Mode — Auto-rotating, animated, always-on
Port: 8052 | URL: https://cf-industry.ngrok.app
Author: Jose Arzaga — RevOps & Data Analyst
"""

import dash
from dash import dcc, html, Input, Output, clientside_callback
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import date

# ─── APP ───────────────────────────────────────────────────────────────────────
app = dash.Dash(__name__, title="CF Industry Intelligence")
app.config.suppress_callback_exceptions = True

app.index_string = """
<!DOCTYPE html>
<html>
<head>{%metas%}<title>{%title%}</title>{%favicon%}{%css%}
<style>
@keyframes ticker { 0% { transform: translateX(0); } 100% { transform: translateX(-50%); } }
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
.slide-in { animation: fadeIn 0.5s ease forwards; }
body { margin: 0; overflow: hidden; }
</style>
</head>
<body>{%app_entry%}<footer>{%config%}{%scripts%}{%renderer%}</footer></body>
</html>
"""


# ─── THEME ─────────────────────────────────────────────────────────────────────
BG      = "#0a0d14"
CARD    = "#111520"
TEAL    = "#1A6B72"
TEAL_LT = "#22909A"
AMBER   = "#F5A623"
GREEN   = "#2ECC71"
RED     = "#E74C3C"
MUTED   = "#6B7A99"
WHITE   = "#F0F4FF"
FONT    = "Inter, -apple-system, sans-serif"

PLOT_BG = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family=FONT, color=WHITE, size=13),
    margin=dict(l=24, r=24, t=48, b=24),
)

# ─── DATA ──────────────────────────────────────────────────────────────────────
cf_closed_won       = 88
cf_trial_act        = 135
cf_demo_completed   = 346
cf_trial_to_close   = round((cf_closed_won / cf_trial_act) * 100, 1)
cf_demo_to_close    = round((cf_closed_won / cf_demo_completed) * 100, 1)
icp_total           = 378000  # 5-49 emp construction firms

market_growth = pd.DataFrame({
    "Year":     [2020, 2021, 2022, 2023, 2024, 2025, 2026],
    "Market_B": [1.8,  2.2,  2.7,  3.3,  4.0,  4.9,  5.8],
})

conversion = pd.DataFrame({
    "Segment":       ["SMB SaaS Median", "Construction SaaS", "Contractor Foreman", "Top Quartile"],
    "Trial_to_Paid": [15, 12, cf_trial_to_close, 25],
    "Demo_to_Close": [22, 18, cf_demo_to_close,  35],
})

establishments = pd.DataFrame({
    "Size":  ["1–4 emp", "5–9 emp", "10–19 emp", "20–49 emp", "50–99 emp", "100+ emp"],
    "Count": [412000,    198000,    112000,       68000,       22000,       8000],
})

geo = pd.DataFrame({
    "State": ["CA","TX","FL","NY","PA","OH","IL","GA","NC","AZ"],
    "Count": [82000,71000,58000,45000,31000,29000,28000,27000,26000,22000],
})

funnel = pd.DataFrame({
    "Month":     ["Jan","Feb","Mar","Apr","May","Jun"],
    "Leads":     [1820, 1940, 2100, 2250, 2380, 2490],
    "Trials":    [95,   102,  115,  121,  128,  135],
    "ClosedWon": [58,   62,   70,   74,   81,   88],
})

churn = pd.DataFrame({
    "Vertical":     ["SMB SaaS avg","Construction SaaS","Field Service SaaS","Project Mgmt SaaS"],
    "Churn":        [8.5, 10.2, 9.1, 7.4],
})

# ─── FIGURES ───────────────────────────────────────────────────────────────────
def fig_market():
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=market_growth["Year"], y=market_growth["Market_B"],
        mode="lines+markers",
        line=dict(color=TEAL_LT, width=4),
        marker=dict(size=10, color=TEAL_LT, line=dict(color=WHITE, width=2)),
        fill="tozeroy", fillcolor="rgba(26,107,114,0.15)",
        name="Market Size",
    ))
    fig.add_vline(x=2026, line_dash="dash", line_color=AMBER,
                  annotation_text="  2026", annotation_font_color=AMBER, annotation_font_size=14)
    fig.update_layout(
        title=dict(text="Construction SaaS Market Size — $5.8B in 2026", font=dict(size=18, color=WHITE)),
        xaxis=dict(gridcolor="rgba(255,255,255,0.06)", showline=False),
        yaxis=dict(gridcolor="rgba(255,255,255,0.06)", tickprefix="$", ticksuffix="B"),
        showlegend=False, **PLOT_BG,
    )
    return fig

def fig_conversion():
    colors_trial = [MUTED, MUTED, AMBER, GREEN]
    colors_demo  = [MUTED, MUTED, GREEN, TEAL_LT]
    fig = go.Figure()
    for i, row in conversion.iterrows():
        fig.add_trace(go.Bar(
            name=row["Segment"],
            x=["Trial → Paid %", "Demo → Close %"],
            y=[row["Trial_to_Paid"], row["Demo_to_Close"]],
            marker_color=[colors_trial[i], colors_demo[i]],
            text=[f"{row['Trial_to_Paid']}%", f"{row['Demo_to_Close']}%"],
            textposition="outside", textfont=dict(size=14, color=WHITE),
        ))
    fig.update_layout(
        title=dict(text="CF Conversion vs Industry Benchmarks", font=dict(size=18, color=WHITE)),
        barmode="group",
        xaxis=dict(gridcolor="rgba(255,255,255,0.06)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.06)", ticksuffix="%", range=[0, 45]),
        legend=dict(bgcolor="rgba(0,0,0,0.3)", bordercolor=TEAL, borderwidth=1, font=dict(size=12)),
        **PLOT_BG,
    )
    return fig

def fig_establishments():
    icp_sizes = ["5–9 emp", "10–19 emp", "20–49 emp"]
    fig = go.Figure(go.Bar(
        x=establishments["Size"],
        y=establishments["Count"],
        marker_color=[TEAL_LT if s in icp_sizes else MUTED for s in establishments["Size"]],
        text=[f"{c:,}" for c in establishments["Count"]],
        textposition="outside", textfont=dict(size=13, color=WHITE),
    ))
    fig.add_annotation(x=1, y=230000, text="← CF ICP", showarrow=False,
                       font=dict(color=TEAL_LT, size=14), xref="x", yref="y")
    fig.update_layout(
        title=dict(text="US Construction Firms by Size — 378K in ICP (teal)", font=dict(size=18, color=WHITE)),
        xaxis=dict(gridcolor="rgba(255,255,255,0.06)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.06)"),
        showlegend=False, **PLOT_BG,
    )
    return fig

def fig_geo():
    df = geo.sort_values("Count")
    fig = go.Figure(go.Bar(
        x=df["Count"], y=df["State"], orientation="h",
        marker=dict(
            color=df["Count"],
            colorscale=[[0, CARD], [0.5, TEAL], [1, TEAL_LT]],
        ),
        text=[f"{c:,}" for c in df["Count"]],
        textposition="outside", textfont=dict(size=13, color=WHITE),
    ))
    fig.update_layout(
        title=dict(text="Top 10 States — Construction Establishments", font=dict(size=18, color=WHITE)),
        xaxis=dict(gridcolor="rgba(255,255,255,0.06)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.06)"),
        **PLOT_BG,
    )
    return fig

def fig_funnel():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=funnel["Month"], y=funnel["Leads"],
        name="Leads", line=dict(color=MUTED, width=3), mode="lines+markers",
        marker=dict(size=8)))
    fig.add_trace(go.Scatter(x=funnel["Month"], y=funnel["Trials"],
        name="Trial Activations", line=dict(color=TEAL_LT, width=3), mode="lines+markers",
        marker=dict(size=8)))
    fig.add_trace(go.Scatter(x=funnel["Month"], y=funnel["ClosedWon"],
        name="Closed Won", line=dict(color=GREEN, width=3), mode="lines+markers",
        marker=dict(size=8)))
    fig.update_layout(
        title=dict(text="CF Funnel Growth — Jan → Jun 2026", font=dict(size=18, color=WHITE)),
        xaxis=dict(gridcolor="rgba(255,255,255,0.06)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.06)"),
        legend=dict(bgcolor="rgba(0,0,0,0.3)", bordercolor=TEAL, borderwidth=1),
        **PLOT_BG,
    )
    return fig

def fig_churn():
    fig = go.Figure(go.Bar(
        x=churn["Churn"], y=churn["Vertical"], orientation="h",
        marker_color=[AMBER if v == "Construction SaaS" else TEAL_LT for v in churn["Vertical"]],
        text=[f"{c}%" for c in churn["Churn"]],
        textposition="outside", textfont=dict(size=14, color=WHITE),
    ))
    fig.update_layout(
        title=dict(text="Annual Churn by Vertical — Construction SaaS at 10.2%", font=dict(size=18, color=WHITE)),
        xaxis=dict(gridcolor="rgba(255,255,255,0.06)", ticksuffix="%"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.06)"),
        **PLOT_BG,
    )
    return fig

SLIDES = [
    {"id": "market",        "label": "Market Size",     "figure": fig_market()},
    {"id": "funnel",        "label": "CF Funnel",       "figure": fig_funnel()},
    {"id": "conversion",    "label": "Conversion",      "figure": fig_conversion()},
    {"id": "establishments","label": "TAM / ICP",       "figure": fig_establishments()},
    {"id": "geo",           "label": "Geography",       "figure": fig_geo()},
    {"id": "churn",         "label": "Churn Bench.",    "figure": fig_churn()},
]

TICKER_ITEMS = [
    f"⬆ Construction SaaS CAGR: ~20%",
    f"🏗 US Construction Firms: 820K+",
    f"🎯 CF ICP (5–49 emp): {icp_total:,} firms",
    f"✅ CF Trial→Close: {cf_trial_to_close}%  |  Industry Median: 12%",
    f"✅ CF Demo→Close: {cf_demo_to_close}%  |  Industry Median: 18%",
    f"📊 Construction SaaS Market: $5.8B in 2026",
    f"⚠ Construction SaaS Churn: 10.2% annual",
    f"🔥 CF June Closed Won: {cf_closed_won} deals",
    f"🔥 CF June Trial Activations: {cf_trial_act}",
    f"📍 Top Markets: CA · TX · FL · NY · PA",
]

# ─── LAYOUT ────────────────────────────────────────────────────────────────────
app.layout = html.Div(style={
    "backgroundColor": BG, "height": "100vh", "width": "100vw",
    "overflow": "hidden", "fontFamily": FONT, "display": "flex",
    "flexDirection": "column", "boxSizing": "border-box",
}, children=[

    # Auto-advance interval — 8 seconds
    dcc.Interval(id="slide-timer", interval=8000, n_intervals=0),
    dcc.Store(id="current-slide", data=0),

    # ── Header ──
    html.Div(style={
        "display": "flex", "alignItems": "center", "justifyContent": "space-between",
        "padding": "14px 28px 10px", "borderBottom": f"1px solid {TEAL}",
        "flexShrink": "0",
    }, children=[
        html.Div([
            html.Span("CONTRACTOR FOREMAN", style={
                "color": TEAL_LT, "fontSize": "11px", "fontWeight": "700",
                "letterSpacing": "0.18em", "display": "block",
            }),
            html.Span("Industry Intelligence", style={
                "color": WHITE, "fontSize": "22px", "fontWeight": "700",
            }),
        ]),
        html.Div(id="slide-label", style={
            "color": AMBER, "fontSize": "13px", "fontWeight": "600",
            "letterSpacing": "0.1em", "textTransform": "uppercase",
        }),
        html.Div([
            html.Span(date.today().strftime("%b %d, %Y"), style={
                "color": MUTED, "fontSize": "13px",
            }),
        ]),
    ]),

    # ── KPI Bar ──
    html.Div(style={
        "display": "flex", "gap": "0", "flexShrink": "0",
        "borderBottom": f"1px solid rgba(26,107,114,0.25)",
    }, children=[
        html.Div([
            html.Div("TAM", style={"color": MUTED, "fontSize": "10px", "letterSpacing": "0.1em"}),
            html.Div("820K+", style={"color": WHITE, "fontSize": "20px", "fontWeight": "700"}),
            html.Div("US Construction Firms", style={"color": MUTED, "fontSize": "10px"}),
        ], style={"flex":"1","padding":"10px 20px","borderRight":f"1px solid rgba(26,107,114,0.2)"}),
        html.Div([
            html.Div("ICP SWEET SPOT", style={"color": MUTED, "fontSize": "10px", "letterSpacing": "0.1em"}),
            html.Div(f"{icp_total:,}", style={"color": TEAL_LT, "fontSize": "20px", "fontWeight": "700"}),
            html.Div("Firms (5–49 employees)", style={"color": MUTED, "fontSize": "10px"}),
        ], style={"flex":"1","padding":"10px 20px","borderRight":f"1px solid rgba(26,107,114,0.2)"}),
        html.Div([
            html.Div("MARKET CAGR", style={"color": MUTED, "fontSize": "10px", "letterSpacing": "0.1em"}),
            html.Div("~20%", style={"color": GREEN, "fontSize": "20px", "fontWeight": "700"}),
            html.Div("Construction SaaS 2020–26", style={"color": MUTED, "fontSize": "10px"}),
        ], style={"flex":"1","padding":"10px 20px","borderRight":f"1px solid rgba(26,107,114,0.2)"}),
        html.Div([
            html.Div("CF TRIAL→CLOSE", style={"color": MUTED, "fontSize": "10px", "letterSpacing": "0.1em"}),
            html.Div(f"{cf_trial_to_close}%", style={"color": AMBER, "fontSize": "20px", "fontWeight": "700"}),
            html.Div("vs 12% industry median", style={"color": MUTED, "fontSize": "10px"}),
        ], style={"flex":"1","padding":"10px 20px","borderRight":f"1px solid rgba(26,107,114,0.2)"}),
        html.Div([
            html.Div("CF DEMO→CLOSE", style={"color": MUTED, "fontSize": "10px", "letterSpacing": "0.1em"}),
            html.Div(f"{cf_demo_to_close}%", style={"color": GREEN, "fontSize": "20px", "fontWeight": "700"}),
            html.Div("vs 18% industry median", style={"color": MUTED, "fontSize": "10px"}),
        ], style={"flex":"1","padding":"10px 20px","borderRight":f"1px solid rgba(26,107,114,0.2)"}),
        html.Div([
            html.Div("JUNE CLOSED WON", style={"color": MUTED, "fontSize": "10px", "letterSpacing": "0.1em"}),
            html.Div(f"{cf_closed_won}", style={"color": WHITE, "fontSize": "20px", "fontWeight": "700"}),
            html.Div("Deals · $248,544", style={"color": MUTED, "fontSize": "10px"}),
        ], style={"flex":"1","padding":"10px 20px"}),
    ]),

    # ── Slide area ──
    html.Div(id="slide-area", style={"flex":"1","padding":"12px 28px","overflow":"hidden"}),

    # ── Slide dots ──
    html.Div(style={
        "display":"flex","justifyContent":"center","gap":"10px",
        "padding":"8px 0","flexShrink":"0",
    }, children=[
        html.Div(id=f"dot-{i}", style={
            "width":"8px","height":"8px","borderRadius":"50%",
            "backgroundColor": TEAL_LT if i == 0 else MUTED,
            "transition":"background-color 0.3s",
        }) for i in range(len(SLIDES))
    ]),

    # ── Ticker ──
    html.Div(style={
        "backgroundColor": CARD,
        "borderTop": f"1px solid {TEAL}",
        "padding": "8px 0",
        "overflow": "hidden",
        "flexShrink": "0",
        "position": "relative",
    }, children=[
        html.Div(
            "  ·  ".join(TICKER_ITEMS) + "   " + "  ·  ".join(TICKER_ITEMS),
            id="ticker-text",
            style={
                "color": MUTED, "fontSize": "12px", "whiteSpace": "nowrap",
                "display": "inline-block",
                "animation": "ticker 60s linear infinite",
                "letterSpacing": "0.04em",
            }
        ),
    ]),
])

# ─── CALLBACKS ─────────────────────────────────────────────────────────────────
@app.callback(
    Output("current-slide", "data"),
    Input("slide-timer", "n_intervals"),
    prevent_initial_call=True,
)
def advance_slide(n):
    return n % len(SLIDES)

@app.callback(
    Output("slide-area", "children"),
    Output("slide-label", "children"),
    Input("current-slide", "data"),
)
def update_slide(idx):
    slide = SLIDES[idx]
    graph = dcc.Graph(
        figure=slide["figure"],
        config={"displayModeBar": False},
        style={"height": "100%"},
        className="slide-in",
    )
    label = f"{idx + 1} / {len(SLIDES)}  —  {slide['label']}"
    return graph, label

# ─── RUN ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8052, debug=False)
