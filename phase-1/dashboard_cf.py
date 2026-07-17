import dash
from dash import dcc, html
import plotly.graph_objects as go

app = dash.Dash(__name__)

closed_won_deals = 88
closed_won_revenue = 248544
trial_activated_deals = 135
trial_activated_revenue = 312022
revenue_gap = trial_activated_revenue - closed_won_revenue

self_serve_amy = 169
self_serve_juan = 86
self_serve_total = self_serve_amy + self_serve_juan
self_serve_deals = 151

se_names = ["Neidhart", "Hernandez", "Dominguez", "Reynolds", "Sanchez Rojas", "Cox (New)"]
se_deals = [18, 19, 20, 15, 9, 2]
se_revenue = [58376, 56356, 51922, 42601, 18035, 6638]
se_colors = ["#1A6B72","#1A6B72","#1A6B72","#1A6B72","#CC0000","#2196F3"]

plan_names = ["Pro", "Plus", "Unlimited", "Standard", "Basic"]
plan_counts = [60, 33, 31, 7, 3]
plan_colors = ["#1A6B72", "#2196F3", "#4CAF50", "#FF9800", "#9C27B0"]

weeks = ["W22 Jun 1-7", "W23 Jun 8-14", "W24 Jun 15-21", "W25 Jun 22-30"]
week_counts = [44, 26, 26, 30]

days = ["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26"]
daily_counts = [16,15,15,32,20,3,5,15,22,6,12,9,4,1,14,16,13,14,17,2,2,25,18,21,27,3]

pipeline_stages = ["Demo Scheduled", "Demo Completed", "Trial Activated", "Trial At Risk"]
pipeline_deals_p = [173, 346, 167, 36]
pipeline_weighted = [173*0.05*2654, 346*0.10*2654, 167*0.70*2654, 36*0.60*2654]
pipeline_colors = ["#FF9800", "#2196F3", "#4CAF50", "#CC0000"]

forecast_scenarios = ["Worst Case", "Likely Case", "Best Case"]
forecast_deals_f = [58, 92, 120]
forecast_revenue_f = [58*2654, 92*2654, 120*2654]
forecast_colors = ["#CC0000", "#1A6B72", "#4CAF50"]

june_metrics = ["Closed Won Deals", "Closed Won Revenue", "Trial Activations"]
june_vals = [88, 248544, 135]
july_vals = [92, 244168, 142]

DARK = "#0f1117"
CARD = "#1e2130"
TEAL = "#1A6B72"
WHITE = "white"
GRAY = "#888"

def kpi(label, value, color):
    return html.Div(style={"backgroundColor": CARD, "borderRadius": "10px", "padding": "20px", "flex": "1", "minWidth": "140px", "borderLeft": f"4px solid {color}"}, children=[
        html.P(label, style={"color": GRAY, "margin": "0", "fontSize": "12px"}),
        html.H2(value, style={"color": WHITE, "margin": "5px 0", "fontSize": "24px"})
    ])

def section(title):
    return html.H2(title, style={"color": TEAL, "borderBottom": f"2px solid {TEAL}", "paddingBottom": "8px", "marginTop": "32px", "marginBottom": "16px", "fontSize": "18px"})

app.layout = html.Div(style={"backgroundColor": DARK, "minHeight": "100vh", "fontFamily": "Arial", "padding": "24px"}, children=[

    html.Div(style={"textAlign": "center", "marginBottom": "32px"}, children=[
        html.H1("Contractor Foreman - RevOps Dashboard", style={"color": TEAL, "fontSize": "32px", "marginBottom": "4px"}),
        html.P("June 2026  |  Built by Jose Arzaga  |  Verified Zoho CRM Jun 26, 2026", style={"color": GRAY, "fontSize": "13px"}),
    ]),

    html.Div(style={"display": "flex", "gap": "12px", "marginBottom": "24px", "flexWrap": "wrap"}, children=[
        kpi("Closed Won Deals", f"{closed_won_deals}", "#1A6B72"),
        kpi("Closed Won Revenue", f"${closed_won_revenue:,}", "#2196F3"),
        kpi("Trial Activations", f"{trial_activated_deals}", "#4CAF50"),
        kpi("Trial Revenue", f"${trial_activated_revenue:,}", "#FF9800"),
        kpi("Trial to Close Gap", f"${revenue_gap:,}", "#f44336"),
        kpi("Self-Serve Customers", f"{self_serve_total}", "#9C27B0"),
    ]),

    section("Sales Executive Performance"),
    html.Div(style={"display": "flex", "gap": "16px", "marginBottom": "24px", "flexWrap": "wrap"}, children=[
        html.Div(style={"backgroundColor": CARD, "borderRadius": "10px", "padding": "20px", "flex": "1.5", "minWidth": "300px"}, children=[
            html.H3("Closed Won by SE", style={"color": TEAL, "marginTop": "0"}),
            dcc.Graph(figure=go.Figure(
                data=[
                    go.Bar(name="Revenue", x=se_names, y=se_revenue, marker_color=se_colors, yaxis="y", opacity=0.85),
                    go.Scatter(name="Deals", x=se_names, y=se_deals, mode="lines+markers+text", text=se_deals, textposition="top center", line=dict(color="#FF9800", width=2), marker=dict(size=8), yaxis="y2")
                ],
                layout=go.Layout(plot_bgcolor=CARD, paper_bgcolor=CARD, font=dict(color=WHITE), yaxis=dict(title="Revenue ($)", gridcolor="#333", tickprefix="$"), yaxis2=dict(title="Deals", overlaying="y", side="right", gridcolor="#333"), legend=dict(bgcolor=CARD), margin=dict(t=20, b=40))
            ), style={"height": "320px"})
        ]),
        html.Div(style={"backgroundColor": CARD, "borderRadius": "10px", "padding": "20px", "flex": "1", "minWidth": "260px"}, children=[
            html.H3("Trial Plan Mix", style={"color": TEAL, "marginTop": "0"}),
            dcc.Graph(figure=go.Figure(
                data=[go.Pie(labels=plan_names, values=plan_counts, marker=dict(colors=plan_colors), hole=0.4, textinfo="label+percent")],
                layout=go.Layout(plot_bgcolor=CARD, paper_bgcolor=CARD, font=dict(color=WHITE), showlegend=False, margin=dict(t=20, b=20, l=20, r=20), annotations=[dict(text=f"{trial_activated_deals} Trials", x=0.5, y=0.5, font_size=13, showarrow=False, font=dict(color=WHITE))])
            ), style={"height": "320px"})
        ]),
    ]),

    section("Self-Serve Channel"),
    html.Div(style={"display": "flex", "gap": "16px", "marginBottom": "24px", "flexWrap": "wrap"}, children=[
        html.Div(style={"backgroundColor": CARD, "borderRadius": "10px", "padding": "20px", "flex": "1", "minWidth": "260px"}, children=[
            html.H3("Self-Serve vs SE-Assisted", style={"color": TEAL, "marginTop": "0"}),
            dcc.Graph(figure=go.Figure(
                data=[go.Bar(x=["Amy Smith\n(Organic)", "Juan Balderas\n(SDR)", "SE Assisted\n(Closed Won)"], y=[self_serve_amy, self_serve_juan, closed_won_deals], marker_color=["#9C27B0", "#2196F3", "#1A6B72"], text=[self_serve_amy, self_serve_juan, closed_won_deals], textposition="outside")],
                layout=go.Layout(plot_bgcolor=CARD, paper_bgcolor=CARD, font=dict(color=WHITE), yaxis=dict(gridcolor="#333"), xaxis=dict(gridcolor="#333"), margin=dict(t=20, b=60))
            ), style={"height": "300px"})
        ]),
        html.Div(style={"backgroundColor": CARD, "borderRadius": "10px", "padding": "20px", "flex": "1", "minWidth": "260px"}, children=[
            html.H3("Channel Mix", style={"color": TEAL, "marginTop": "0"}),
            dcc.Graph(figure=go.Figure(
                data=[go.Pie(labels=["Amy Smith (Organic)", "Juan Balderas (SDR)", "SE Assisted"], values=[self_serve_amy, self_serve_juan, closed_won_deals], marker=dict(colors=["#9C27B0", "#2196F3", "#1A6B72"]), hole=0.4, textinfo="label+percent")],
                layout=go.Layout(plot_bgcolor=CARD, paper_bgcolor=CARD, font=dict(color=WHITE), showlegend=False, margin=dict(t=20, b=20, l=20, r=20), annotations=[dict(text="All\nChannels", x=0.5, y=0.5, font_size=11, showarrow=False, font=dict(color=WHITE))])
            ), style={"height": "300px"})
        ]),
        html.Div(style={"backgroundColor": CARD, "borderRadius": "10px", "padding": "20px", "flex": "1", "minWidth": "260px"}, children=[
            html.H3("Self-Serve Summary", style={"color": TEAL, "marginTop": "0"}),
            dcc.Graph(figure=go.Figure(
                data=[go.Table(
                    columnwidth=[180, 120, 100],
                    header=dict(values=["Channel", "Customers", "Deals"], fill_color=TEAL, font=dict(color=WHITE, size=13), align="center"),
                    cells=dict(values=[["Amy Smith (Organic)", "Juan Balderas (SDR)", "Combined Self-Serve", "SE Assisted"], [self_serve_amy, self_serve_juan, self_serve_total, "-"], [107, 44, self_serve_deals, closed_won_deals]], fill_color=[["#2a2f3f", CARD, "#1A3A3A", "#2a2f3f"]], font=dict(color=WHITE, size=12), align="center", height=36)
                )],
                layout=go.Layout(paper_bgcolor=CARD, margin=dict(t=10, b=10))
            ), style={"height": "300px"})
        ]),
    ]),

    section("Pipeline Health"),
    html.Div(style={"display": "flex", "gap": "16px", "marginBottom": "24px", "flexWrap": "wrap"}, children=[
        html.Div(style={"backgroundColor": CARD, "borderRadius": "10px", "padding": "20px", "flex": "1.5", "minWidth": "300px"}, children=[
            html.H3("Weighted Pipeline by Stage", style={"color": TEAL, "marginTop": "0"}),
            dcc.Graph(figure=go.Figure(
                data=[go.Bar(x=pipeline_weighted, y=pipeline_stages, orientation="h", marker_color=pipeline_colors, text=[f"${v:,.0f}" for v in pipeline_weighted], textposition="outside")],
                layout=go.Layout(plot_bgcolor=CARD, paper_bgcolor=CARD, font=dict(color=WHITE), xaxis=dict(gridcolor="#333", tickprefix="$"), yaxis=dict(gridcolor="#333"), margin=dict(t=20, b=40, l=140))
            ), style={"height": "280px"})
        ]),
        html.Div(style={"backgroundColor": CARD, "borderRadius": "10px", "padding": "20px", "flex": "1", "minWidth": "220px"}, children=[
            html.H3("Pipeline Deal Count", style={"color": TEAL, "marginTop": "0"}),
            dcc.Graph(figure=go.Figure(
                data=[go.Bar(x=pipeline_stages, y=pipeline_deals_p, marker_color=pipeline_colors, text=pipeline_deals_p, textposition="outside")],
                layout=go.Layout(plot_bgcolor=CARD, paper_bgcolor=CARD, font=dict(color=WHITE, size=10), xaxis=dict(gridcolor="#333", tickangle=-20), yaxis=dict(gridcolor="#333"), margin=dict(t=20, b=80))
            ), style={"height": "280px"})
        ]),
    ]),

    section("July 2026 Forecast"),
    html.Div(style={"display": "flex", "gap": "16px", "marginBottom": "24px", "flexWrap": "wrap"}, children=[
        html.Div(style={"backgroundColor": CARD, "borderRadius": "10px", "padding": "20px", "flex": "1", "minWidth": "260px"}, children=[
            html.H3("Revenue Scenarios", style={"color": TEAL, "marginTop": "0"}),
            dcc.Graph(figure=go.Figure(
                data=[go.Bar(x=forecast_scenarios, y=forecast_revenue_f, marker_color=forecast_colors, text=[f"${v:,}" for v in forecast_revenue_f], textposition="outside")],
                layout=go.Layout(plot_bgcolor=CARD, paper_bgcolor=CARD, font=dict(color=WHITE), yaxis=dict(gridcolor="#333", tickprefix="$"), xaxis=dict(gridcolor="#333"), margin=dict(t=20, b=40))
            ), style={"height": "300px"})
        ]),
        html.Div(style={"backgroundColor": CARD, "borderRadius": "10px", "padding": "20px", "flex": "1", "minWidth": "260px"}, children=[
            html.H3("Deal Count Scenarios", style={"color": TEAL, "marginTop": "0"}),
            dcc.Graph(figure=go.Figure(
                data=[go.Bar(x=forecast_scenarios, y=forecast_deals_f, marker_color=forecast_colors, text=forecast_deals_f, textposition="outside")],
                layout=go.Layout(plot_bgcolor=CARD, paper_bgcolor=CARD, font=dict(color=WHITE), yaxis=dict(gridcolor="#333"), xaxis=dict(gridcolor="#333"), margin=dict(t=20, b=40))
            ), style={"height": "300px"})
        ]),
        html.Div(style={"backgroundColor": CARD, "borderRadius": "10px", "padding": "20px", "flex": "1", "minWidth": "260px"}, children=[
            html.H3("June vs July Trend", style={"color": TEAL, "marginTop": "0"}),
            dcc.Graph(figure=go.Figure(
                data=[go.Bar(name="June Actual", x=june_metrics, y=june_vals, marker_color="#1A6B72"), go.Bar(name="July Forecast", x=june_metrics, y=july_vals, marker_color="#FF9800")],
                layout=go.Layout(plot_bgcolor=CARD, paper_bgcolor=CARD, font=dict(color=WHITE), barmode="group", yaxis=dict(gridcolor="#333"), xaxis=dict(gridcolor="#333", tickangle=-15), legend=dict(bgcolor=CARD), margin=dict(t=20, b=60))
            ), style={"height": "300px"})
        ]),
    ]),

    section("Activity Trends"),
    html.Div(style={"display": "flex", "gap": "16px", "marginBottom": "24px", "flexWrap": "wrap"}, children=[
        html.Div(style={"backgroundColor": CARD, "borderRadius": "10px", "padding": "20px", "flex": "2", "minWidth": "300px"}, children=[
            html.H3("Daily Activity - June 2026", style={"color": TEAL, "marginTop": "0"}),
            dcc.Graph(figure=go.Figure(
                data=[go.Bar(x=[f"Jun {d}" for d in days], y=daily_counts, marker_color=[TEAL if c >= 20 else "#2196F3" if c >= 10 else "#555" for c in daily_counts], text=daily_counts, textposition="outside")],
                layout=go.Layout(plot_bgcolor=CARD, paper_bgcolor=CARD, font=dict(color=WHITE, size=11), xaxis=dict(gridcolor="#333", tickangle=-45), yaxis=dict(gridcolor="#333"), margin=dict(t=20, b=60))
            ), style={"height": "280px"})
        ]),
        html.Div(style={"backgroundColor": CARD, "borderRadius": "10px", "padding": "20px", "flex": "1", "minWidth": "220px"}, children=[
            html.H3("Weekly Trend", style={"color": TEAL, "marginTop": "0"}),
            dcc.Graph(figure=go.Figure(
                data=[go.Bar(x=weeks, y=week_counts, marker_color=["#1A6B72", "#2196F3", "#4CAF50", "#FF9800"], text=week_counts, textposition="outside")],
                layout=go.Layout(plot_bgcolor=CARD, paper_bgcolor=CARD, font=dict(color=WHITE, size=11), xaxis=dict(gridcolor="#333", tickangle=-20), yaxis=dict(gridcolor="#333"), margin=dict(t=20, b=80))
            ), style={"height": "280px"})
        ]),
    ]),

    html.Div(style={"backgroundColor": CARD, "borderRadius": "10px", "padding": "20px", "marginBottom": "24px"}, children=[
        html.H3("SE Leaderboard - Closed Won June 2026", style={"color": TEAL, "marginTop": "0"}),
        dcc.Graph(figure=go.Figure(
            data=[go.Table(
                columnwidth=[200, 100, 150, 120],
                header=dict(values=["Sales Executive", "Deals", "Revenue", "Avg Deal Value"], fill_color=TEAL, font=dict(color=WHITE, size=13), align="center"),
                cells=dict(values=[se_names, se_deals, [f"${r:,}" for r in se_revenue], [f"${r//d:,}" for r, d in zip(se_revenue, se_deals)]], fill_color=[["#2a2f3f" if i % 2 == 0 else CARD for i in range(len(se_names))]], font=dict(color=WHITE, size=13), align="center", height=36)
            )],
            layout=go.Layout(paper_bgcolor=CARD, margin=dict(t=10, b=10))
        ), style={"height": "300px"})
    ]),

    html.P("Contractor Foreman RevOps  |  Jose Arzaga 2026  |  Zoho CRM verified Jun 26, 2026",
           style={"color": "#444", "textAlign": "center", "fontSize": "12px"})
])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050, debug=False)
