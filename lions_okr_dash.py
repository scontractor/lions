import base64
import os

import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Lions Intelligence brand colors
BRAND_DARK = "#0a0a0a"
BRAND_GOLD = "#D4A84B"
BRAND_WHITE = "#ffffff"
BRAND_GRAY = "#6b7280"

# 1. Adoption: Seat utilization 65% → 95%
seat_util_current_pct = 65  # %
seat_util_target_pct = 95   # %

# 2. Retention/Habit: 3+ visits/week for 70% of assigned users
habit_current_pct = 28  # Current % at 3+ visits/week
habit_target_pct = 70

# 3. Support & Trust: Resolution Velocity + Weekly Ticket Volume
resolution_weeks = ["3mo ago", "2mo ago", "1mo ago", "Current", "+1mo", "+2mo", "+3mo"]
resolution_pct = [58, 62, 65, 72, 78, 85, 90]  # % within SLA (improving)
resolution_target_pct = 90
ticket_volume = [52, 44, 36, 28, 20, 14, 8]    # Weekly ticket volume: ~50 → target <10/week

# 3b. Feature Adoption Rate (live): AI Assistant vs Search bar
feature_ai_pct = 28                       # % of active users using AI Assistant
feature_search_pct = 100 - feature_ai_pct # % using only Search

# 3c. Stickiness history (DAU / MAU) for line chart
# Past 3 months, current, and next 3 months (for target projection)
stickiness_weeks = ["3mo ago", "2mo ago", "1mo ago", "Current", "+1mo", "+2mo", "+3mo"]
stickiness_history = [10, 16, 6, 3, None, None, None]

# Engagement: WAU / DAU / MAU
total_seats = 867
wau = 196    # Weekly Active Users
dau = 48     # Daily Active Users
mau = 260    # Monthly Active Users
stickiness_pct = round(dau / mau * 100)  # DAU / MAU as %

# 4. Adoption by Team: AI adoption % by team
teams = ["Team A", "Team B", "Team C", "Team D", "Team E"]
current_adoption = [80, 70, 12, 8, 5]
target_adoption = [95, 90, 75, 75, 75]

# Plotly Dashboard - Row 0: header for logo, Rows 1-3: OKRs + Feature Adoption + Stickiness
fig = make_subplots(
    rows=4, cols=2,
    specs=[
        [{"type": "xy", "colspan": 2}, None],  # Row 0: header (logo goes here)
        [{"type": "indicator"}, {"type": "indicator"}],
        [{"type": "xy", "secondary_y": True}, {"type": "xy"}],
        [{"type": "domain"}, {"type": "xy"}],  # Row 3: feature adoption ring + stickiness line
    ],
    subplot_titles=(
        "",
        "Adoption: Seat Utilisation",
        "Workflow Integration: 3+ Weekly Queries/User",
        "Support Tickets: Resolution Velocity & Volume",
        "AI assistant: Penetration by BrandCo Teams",
        "Feature Adoption: AI Assistant vs Search bar",
        "Stickiness: DAU / MAU",
    ),
    vertical_spacing=0.20,
    horizontal_spacing=0.12,
    row_heights=[0.10, 0.30, 0.30, 0.30],
)

# --- OKR 1: Adoption - Seat Utilisation 65% → 95% ---
fig.add_trace(
    go.Indicator(
        mode="gauge+number+delta",
        value=seat_util_current_pct,
        number={"suffix": "%"},
        delta={"reference": seat_util_target_pct, "position": "top", "relative": False},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": BRAND_GRAY, "ticksuffix": "%"},
            "bar": {"color": BRAND_GOLD},
            "bgcolor": "#1a1a1a",
            "borderwidth": 2,
            "bordercolor": BRAND_GRAY,
            "steps": [
                {"range": [0, seat_util_current_pct], "color": BRAND_GOLD},
                {"range": [seat_util_current_pct, seat_util_target_pct], "color": "#2a2a2a"},
            ],
            "threshold": {
                "line": {"color": "red", "width": 4},
                "thickness": 0.75,
                "value": seat_util_target_pct,
            },
        },
    ),
    row=2, col=1,
)

# --- OKR 2: Retention/Habit - 70% at 3+ visits/week ---
fig.add_trace(
    go.Indicator(
        mode="gauge+number+delta",
        value=habit_current_pct,
        number={"suffix": "%"},
        delta={"reference": habit_target_pct, "position": "top", "relative": False},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": BRAND_GRAY, "ticksuffix": "%"},
            "bar": {"color": BRAND_GOLD},
            "bgcolor": "#1a1a1a",
            "borderwidth": 2,
            "bordercolor": BRAND_GRAY,
            "steps": [
                {"range": [0, habit_current_pct], "color": BRAND_GOLD},
                {"range": [habit_current_pct, habit_target_pct], "color": "#2a2a2a"},
            ],
            "threshold": {
                "line": {"color": "red", "width": 4},
                "thickness": 0.75,
                "value": habit_target_pct,
            },
        },
    ),
    row=2, col=2,
)

# --- OKR 3: Support & Trust - Resolution Velocity + Weekly Ticket Volume ---
fig.add_trace(
    go.Scatter(
        x=resolution_weeks,
        y=resolution_pct,
        mode="lines+markers",
        line=dict(color=BRAND_GOLD, width=4),
        marker=dict(size=10),
        name="% Within SLA",
        showlegend=True,
    ),
    row=3, col=1,
)
fig.add_trace(
    go.Scatter(
        x=[resolution_weeks[0], resolution_weeks[-1]],
        y=[resolution_target_pct, resolution_target_pct],
        mode="lines",
        line=dict(color="red", width=2, dash="dot"),
        name="SLA Target",
        showlegend=True,
    ),
    row=3, col=1,
)
fig.add_trace(
    go.Scatter(
        x=resolution_weeks,
        y=ticket_volume,
        mode="lines+markers",
        line=dict(color=BRAND_WHITE, width=3, dash="dash"),
        marker=dict(size=8),
        name="Weekly ticket volume",
        showlegend=True,
    ),
    row=3, col=1,
    secondary_y=True,
)
fig.update_xaxes(title_text="", row=3, col=1)
fig.update_yaxes(title_text="% Within SLA", range=[0, 100], row=3, col=1)
fig.update_yaxes(title_text="Weekly ticket volume", range=[0, 60], row=3, col=1, secondary_y=True)

# --- OKR 4: Adoption by Team ---
fig.add_trace(
    go.Bar(name="Current", x=teams, y=current_adoption, marker_color=BRAND_WHITE),
    row=3, col=2,
)
fig.add_trace(
    go.Bar(name="90-Day Target", x=teams, y=target_adoption, marker_color=BRAND_GOLD),
    row=3, col=2,
)
fig.update_xaxes(title_text="", row=3, col=2)
fig.update_yaxes(title_text="% Adoption", range=[0, 100], row=3, col=2)

# --- Feature Adoption Rate: AI Assistant vs Search bar (live ring) ---
fig.add_trace(
    go.Pie(
        labels=["AI Assistant", "Search bar"],
        values=[feature_ai_pct, feature_search_pct],
        hole=0.65,
        marker=dict(
            colors=[BRAND_GOLD, "#222222"],
            line=dict(color=BRAND_WHITE, width=1),
        ),
        textinfo="label+percent",
        textposition="outside",
        sort=False,
        direction="clockwise",
        showlegend=False,
    ),
    row=4, col=1,
)

# --- Stickiness Ratio: DAU / MAU (line chart) ---
fig.add_trace(
    go.Scatter(
        x=stickiness_weeks,
        y=stickiness_history,
        mode="lines+markers",
        line=dict(color=BRAND_GOLD, width=3),
        marker=dict(size=8),
        name="DAU / MAU (actual)",
        showlegend=True,
    ),
    row=4, col=2,
)

# Target stickiness line across all months at 15%
stickiness_target_pct = 15  # target DAU/MAU %
fig.add_trace(
    go.Scatter(
        x=stickiness_weeks,
        y=[stickiness_target_pct] * len(stickiness_weeks),
        mode="lines",
        line=dict(color="red", width=2, dash="dot"),
        name="Target stickiness",
        showlegend=True,
    ),
    row=4, col=2,
)
fig.update_xaxes(title_text="", showgrid=False, row=4, col=2)
fig.update_yaxes(
    title_text="Stickiness % (DAU / MAU)",
    range=[0, 40],
    showgrid=True,
    row=4, col=2,
)

# Load logo for embedding
_logo_path = os.path.join(os.path.dirname(__file__), "lions_logo.png")
with open(_logo_path, "rb") as f:
    _logo_base64 = base64.b64encode(f.read()).decode()

# Hide axes for header row (row 1, col 1)
fig.update_xaxes(showticklabels=False, showgrid=False, zeroline=False, showline=False, row=1, col=1)
fig.update_yaxes(showticklabels=False, showgrid=False, zeroline=False, showline=False, row=1, col=1)

# Layout Styling (Lions Intelligence Brand)
fig.update_layout(
    title={"text": ""},
    template="plotly_dark",
    paper_bgcolor=BRAND_DARK,
    plot_bgcolor=BRAND_DARK,
    showlegend=False,  # no global legend box
    height=950,
    font=dict(family="Segoe UI, system-ui, sans-serif", size=11, color=BRAND_WHITE),
    margin=dict(t=100, b=55, l=55, r=55),
    images=[
        {
            "source": f"data:image/png;base64,{_logo_base64}",
            "xref": "paper",
            "yref": "paper",
            "x": 0.5,
            "y": 1.02,
            "xanchor": "center",
            "yanchor": "top",
            "sizex": 0.35,
            "sizey": 0.10,
            "layer": "above",
        }
    ],
)

# Update subplot titles: bold, slightly smaller, extra space for first two gauges
for ann in fig.layout.annotations:
    if not ann.text:
        continue

    original_text = ann.text.replace("<b>", "").replace("</b>", "")
    ann.update(
        text=f"<b>{original_text}</b>",
        font=dict(size=14, color=BRAND_WHITE),
    )

    # Base offset for all subplot titles
    ann.update(y=ann.y + 0.02, yref="paper")

    # Extra offset for the first two gauge titles so they clear the dials
    if "Adoption: Seat Utilisation" in original_text or "Workflow Integration: 3+ Weekly Queries/User" in original_text:
        ann.update(y=ann.y + 0.02)

# Add title below logo
fig.add_annotation(
    text="BrandCo Strategic Health Reset: OKR Dashboard",
    xref="paper",
    yref="paper",
    x=0.5,
    y=0.90,
    xanchor="center",
    yanchor="top",
    font=dict(size=28, color=BRAND_WHITE),
    showarrow=False,
)

fig.write_html(
    "lions_okr_dashboard.html",
    auto_open=True,
    include_plotlyjs="cdn",
    full_html=True,
)