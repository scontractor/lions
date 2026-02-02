import base64
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Lions Intelligence brand colors
BRAND_DARK = "#0a0a0a"
BRAND_GOLD = "#D4A84B"
BRAND_WHITE = "#ffffff"
BRAND_GRAY = "#6b7280"
# Live tracker accent colors
LIVE_GREEN = "#00ff88"
LIVE_CYAN = "#00d4ff"

# OKR Data
# 1. Adoption: Seat utilization 65% → 95% via Activation Sprint
seat_util_current_pct = 65  # %
seat_util_target_pct = 95   # %

# 2. Retention/Habit: 3+ visits/week for 70% of assigned users
habit_current_pct = 28  # Current % at 3+ visits/week
habit_target_pct = 70

# 3. Support & Trust: Resolution Velocity + Ticket Volume
resolution_weeks = ["3mo ago", "2mo ago", "1mo ago", "Current", "+1mo", "+2mo", "+3mo"]
resolution_pct = [58, 62, 65, 72, 78, 85, 90]  # % within SLA (improving)
resolution_target_pct = 90
ticket_volume = [195, 168, 145, 120, 95, 75, 60]  # Going down: was high, target lower

# Engagement: WAU / DAU (per seat, max = total_seats)
total_seats = 867
wau = 196    # Weekly Active Users (per seat)
dau = 48    # Daily Active Users (per seat)

# 4. Adoption by Team: AI adoption % by team
teams = ["Strategy", "Insights", "Creative", "Media", "Brand"]
current_adoption = [80, 70, 12, 8, 5]
target_adoption = [95, 90, 75, 75, 75]

# Plotly Dashboard - Row 0: header for logo, Rows 1-2: 4 OKRs
fig = make_subplots(
    rows=3, cols=2,
    specs=[
        [{"type": "xy", "colspan": 2}, None],  # Row 0: header (logo goes here)
        [{"type": "indicator"}, {"type": "indicator"}],
        [{"type": "xy", "secondary_y": True}, {"type": "xy"}],
    ],
    subplot_titles=(
        "",
        "Adoption: Seat Utilisation",
        "Workflow Integration: 3+ Weekly Queries/User",
        "Support Tickets: Resolution Velocity & Volume",
        "AI assistant: Usage by BrandCo Teams",
    ),
    vertical_spacing=0.28,
    horizontal_spacing=0.12,
    row_heights=[0.14, 0.43, 0.43],  # Row 0: 14% for logo header
)

# --- OKR 1: Adoption - Seat Utilisation 65% → 95% ---
fig.add_trace(go.Indicator(
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
    title={"text": "Activation Sprint Target", "font": {"size": 11}},
), row=2, col=1)

# --- OKR 2: Retention/Habit - 70% at 3+ visits/week ---
fig.add_trace(go.Indicator(
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
    title={"text": "Time-to-Value Adoption Target", "font": {"size": 11}},
), row=2, col=2)

# --- OKR 3: Support & Trust - Resolution Velocity + Ticket Volume ---
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
        name="Target",
        showlegend=False,
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
        name="Ticket Volume",
        showlegend=True,
    ),
    row=3, col=1,
    secondary_y=True,
)
fig.update_xaxes(title_text="", row=3, col=1)
fig.update_yaxes(title_text="% Within SLA", range=[0, 100], row=3, col=1)
fig.update_yaxes(title_text="Ticket Volume", range=[0, 250], row=3, col=1, secondary_y=True)

# --- OKR 4: Adoption by Team ---
fig.add_trace(go.Bar(name="Current", x=teams, y=current_adoption, marker_color=BRAND_WHITE), row=3, col=2)
fig.add_trace(go.Bar(name="90-Day Target", x=teams, y=target_adoption, marker_color=BRAND_GOLD), row=3, col=2)
fig.update_xaxes(title_text="", row=3, col=2)
fig.update_yaxes(title_text="% Adoption", range=[0, 100], row=3, col=2)

# Load logo for embedding
_logo_path = os.path.join(os.path.dirname(__file__), "lions_logo.png")
with open(_logo_path, "rb") as f:
    _logo_base64 = base64.b64encode(f.read()).decode()

# Hide axes for header row (row 1, col 1)
fig.update_xaxes(showticklabels=False, showgrid=False, zeroline=False, showline=False, row=1, col=1)
fig.update_yaxes(showticklabels=False, showgrid=False, zeroline=False, showline=False, row=1, col=1)

# Layout Styling (Lions Intelligence Brand)
# Logo first (top), then title below
fig.update_layout(
    title={"text": ""},
    template="plotly_dark",
    paper_bgcolor=BRAND_DARK,
    plot_bgcolor=BRAND_DARK,
    showlegend=True,
    legend=dict(
        x=0.98,
        y=0.23,
        xanchor="right",
        yanchor="top",
        bgcolor="rgba(10,10,10,0.8)",
        bordercolor=BRAND_GRAY,
        borderwidth=1,
    ),
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

# Update subplot titles: bold, font 16, spacing below heading
# Note: header row (colspan 2) has no annotation; annotations 0-3 = Adoption, Retention, Education, Financial
for ann in fig.layout.annotations:
    ann.update(
        text=f"<b>{ann.text}</b>",
        font=dict(size=16, color=BRAND_WHITE),
        y=ann.y + 0.05,
        yref="paper",
    )

# Add title below logo
fig.add_annotation(
    text="BrandCo Strategic Health Reset: Path to 95% Utilisation",
    xref="paper", yref="paper",
    x=0.5, y=0.90,
    xanchor="center", yanchor="top",
    font=dict(size=28, color=BRAND_WHITE),
    showarrow=False,
)

# Live tracker strip (narrow box, text-fit with margins)
fig.add_shape(
    type="rect",
    xref="paper", yref="paper",
    x0=0.40, y0=0.76, x1=0.60, y1=0.81,
    line=dict(width=1, color="rgba(0,255,136,0.4)"),
    layer="below",
)
# Live tracker: WAU / DAU (fitted within box)
fig.add_annotation(
    text="● LIVE",
    xref="paper", yref="paper",
    x=0.41, y=0.785,
    xanchor="left", yanchor="middle",
    font=dict(size=11, color=LIVE_GREEN, family="monospace"),
    showarrow=False,
)
fig.add_annotation(
    text=f"<b>DAU =</b> {dau:,}",
    xref="paper", yref="paper",
    x=0.475, y=0.785,
    xanchor="center", yanchor="middle",
    font=dict(size=15, color=BRAND_GOLD),
    showarrow=False,
)
fig.add_annotation(
    text="·",
    xref="paper", yref="paper",
    x=0.5, y=0.785,
    xanchor="center", yanchor="middle",
    font=dict(size=15, color=BRAND_GRAY),
    showarrow=False,
)
fig.add_annotation(
    text=f"<b>WAU =</b> {wau:,}",
    xref="paper", yref="paper",
    x=0.55, y=0.785,
    xanchor="center", yanchor="middle",
    font=dict(size=15, color=BRAND_GOLD),
    showarrow=False,
)

fig.show()