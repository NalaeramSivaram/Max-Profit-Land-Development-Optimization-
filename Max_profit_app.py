# app.py
"""
Max Profit Scheduler — Enhanced (Scenario Testing removed)
Features:
- Comparison of build types
- Efficiency score
- Enhanced Summary PDF (ReportLab)
Pure Python Streamlit app; uses Plotly for visuals and ReportLab for PDF (optional).
Run: pip install streamlit pandas plotly reportlab==3.6.12
     streamlit run app.py
"""

import streamlit as st
import pandas as pd
import io
import plotly.graph_objects as go
from datetime import datetime

# Try reportlab for PDF generation
REPORTLAB_AVAILABLE = True
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet
except Exception:
    REPORTLAB_AVAILABLE = False

st.set_page_config(page_title="Max Profit Scheduler (Enhanced)", layout="wide", initial_sidebar_state="expanded")

# Basic colors (used in Plotly)
PRIMARY_COLOR = "#0b4f6c"
ACCENT_COLOR = "#6ba5c4"
ACCENT2 = "#f6a01a"

# Default author for PDF
DEFAULT_AUTHOR = "Nalaeram Sivaram — XYZ Institute"

# ------------------------
# Core DP logic
# ------------------------
def max_profit(n, build_time, rate, labels):
    f = [0] * (n + 1)
    choice = [-1] * (n + 1)
    for t in range(n - 1, -1, -1):
        best = 0
        best_choice = -1
        for i in range(len(build_time)):
            finish = t + build_time[i]
            if finish <= n:
                earn_now = rate[i] * (n - finish)
                total = earn_now + f[finish]
                if total > best:
                    best = total
                    best_choice = i
        f[t] = best
        choice[t] = best_choice

    schedule = []
    t = 0
    while t < n and choice[t] != -1:
        i = choice[t]
        start = t
        end = t + build_time[i]
        revenue = rate[i] * (n - end)
        schedule.append({
            "start": start,
            "end": end,
            "type": labels[i],
            "duration": build_time[i],
            "revenue": int(revenue),
            "index": i
        })
        t = end

    counts = {lbl: 0 for lbl in labels}
    total_time_used = 0
    for s in schedule:
        counts[s["type"]] += 1
        total_time_used += s["duration"]

    return f[0], counts, schedule, f, total_time_used

# ------------------------
# PDF generator (ReportLab) - enhanced summary
# ------------------------
def generate_pdf_bytes(schedule_df, profit, counts, n, build_time, rate, labels, dp_array, total_time_used, author=DEFAULT_AUTHOR):
    if not REPORTLAB_AVAILABLE:
        raise RuntimeError("ReportLab not available. Install it with: pip install reportlab==3.6.12")

    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()
    story = []

    # Title & meta
    story.append(Paragraph("Max Profit Builder Scheduler — Summary", styles["Title"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph(f"<b>Author:</b> {author} &nbsp;&nbsp; <b>Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles["Normal"]))
    story.append(Spacer(1, 12))

    # Problem definition
    story.append(Paragraph("<b>Problem Definition</b>", styles["Heading2"]))
    prob = "Building types: " + ", ".join([f"{labels[i]} (time={build_time[i]}, rate={rate[i]})" for i in range(len(labels))]) + "."
    story.append(Paragraph(prob, styles["Normal"]))
    story.append(Spacer(1, 8))

    # KPIs + Efficiency
    story.append(Paragraph("<b>Key Results & Efficiency</b>", styles["Heading2"]))
    utilization = round(100 * (total_time_used / n), 2) if n > 0 else 0.0
    avg_rev_per_build = int(profit / sum(counts.values())) if sum(counts.values()) > 0 else 0
    eff_text = (
        f"<b>Max Earnings:</b> ${int(profit):,}<br/>"
        f"<b>Total Builds:</b> {sum(counts.values())}<br/>"
        f"<b>Total Time Used:</b> {total_time_used} / {n} ({utilization}%)<br/>"
        f"<b>Avg Revenue / Build:</b> ${avg_rev_per_build:,}"
    )
    story.append(Paragraph(eff_text, styles["Normal"]))
    story.append(Spacer(1, 8))

    # Schedule table
    story.append(Paragraph("<b>Schedule</b>", styles["Heading2"]))
    if schedule_df.empty:
        story.append(Paragraph("No scheduled builds for the horizon.", styles["Normal"]))
    else:
        data = [["start", "end", "type", "duration", "revenue"]]
        for _, row in schedule_df.iterrows():
            data.append([str(row["start"]), str(row["end"]), str(row["type"]), str(row["duration"]), f"${int(row['revenue']):,}"])
        tbl = Table(data, hAlign="LEFT", colWidths=[48,48,72,60,80])
        tbl.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.HexColor(PRIMARY_COLOR)),
            ("TEXTCOLOR", (0,0), (-1,0), colors.white),
            ("ALIGN", (0,0), (-1,-1), "CENTER"),
            ("GRID", (0,0), (-1,-1), 0.5, colors.grey)
        ]))
        story.append(tbl)
    story.append(Spacer(1, 10))

    # DP array sample
    story.append(Paragraph("<b>DP array (sample)</b>", styles["Heading2"]))
    sample_len = min(len(dp_array), 60)
    dp_rows = [["t", "f[t]"]] + [[str(t), str(dp_array[t])] for t in range(sample_len)]
    dp_table = Table(dp_rows, hAlign="LEFT", colWidths=[40,100])
    dp_table.setStyle(TableStyle([("GRID", (0,0), (-1,-1), 0.25, colors.grey)]))
    story.append(dp_table)
    story.append(Spacer(1, 8))

    # Conclusion
    story.append(Paragraph("<b>Conclusion</b>", styles["Heading2"]))
    conclusion = (
        "The dynamic programming solver identifies the schedule that maximizes revenue for the planning horizon. "
        "Efficiency metrics (utilization and average revenue per build) are included to support decision analysis."
    )
    story.append(Paragraph(conclusion, styles["Normal"]))
    story.append(Spacer(1, 8))

    doc.build(story)
    pdf_bytes = buf.getvalue()
    buf.close()
    return pdf_bytes

# ------------------------
# Utility visualizations
# ------------------------
def plot_build_comparison(n, build_time, rate, labels):
    # For each build type compute: rate, duration, potential_revenue_if_start_at_0 = rate * (n - duration)
    potential = []
    for i in range(len(labels)):
        pot = rate[i] * max(0, (n - build_time[i]))
        potential.append(pot)

    fig = go.Figure()
    fig.add_trace(go.Bar(x=labels, y=rate, name="Rate (per unit)", marker_color=PRIMARY_COLOR))
    fig.add_trace(go.Bar(x=labels, y=build_time, name="Duration", marker_color=ACCENT_COLOR))
    fig.add_trace(go.Bar(x=labels, y=potential, name="Potential revenue if started early", marker_color=ACCENT2))
    fig.update_layout(barmode='group', title="Build Type Comparison", yaxis_title="Value", height=420)
    return fig

def plot_schedule_contribution(schedule_df, labels):
    # show how many builds each type contributes and percentage
    if schedule_df.empty:
        fig = go.Figure()
        fig.update_layout(title="No schedule to display", height=300)
        return fig
    counts = schedule_df['type'].value_counts()
    labels_order = list(counts.index)
    values = [counts[lbl] for lbl in labels_order]
    fig = go.Figure(data=[go.Pie(labels=labels_order, values=values, hole=0.4)])
    fig.update_layout(title="Schedule Composition by Build Type", height=350)
    return fig

# ------------------------
# Defaults & sidebar
# ------------------------
DEFAULT_BUILD_TIME = [5, 4, 10]
DEFAULT_RATE = [1500, 1000, 2000]
DEFAULT_LABELS = ["T", "P", "C"]

st.sidebar.title("Max Profit Scheduler (Enhanced)")
page = st.sidebar.radio("Navigation", ["Home", "Optimizer", "Visualization", "Comparison", "Download Center", "About"])

# ------------------------
# HOME
# ------------------------
if page == "Home":
    st.title("Max Profit Builder Scheduler")
    st.subheader("Optimization tool for time-based planning")
    st.write(
        "Compute a schedule of builds to maximize revenue within a fixed horizon. "
        "Configure build durations and rates, inspect the optimal schedule, analyze efficiency, and export a summary report."
    )
    st.markdown("---")
    st.subheader("Problem statement")
    st.write(
        "**Given** multiple activity types with different durations and earning rates, determine which activities to perform and when to maximize total earnings within time `n`.\n\n"
        "**Method:** Dynamic Programming (computes the optimal value `f[t]` for every start time `t`)."
    )
    st.markdown("---")
    st.subheader("Quick actions")
    st.write("- Go to **Optimizer** to configure inputs and run.\n- Use **Visualization** and **Comparison** to inspect charts.\n- Use **Download Center** to export a summary PDF or CSV.")

# ------------------------
# OPTIMIZER
# ------------------------
elif page == "Optimizer":
    st.header("Optimizer — Configure & Run")
    with st.form("inputs_form", clear_on_submit=False):
        cols = st.columns(len(DEFAULT_LABELS))
        labels = []
        build_times = []
        rates = []
        for i in range(len(DEFAULT_LABELS)):
            with cols[i]:
                lab = st.text_input(f"Label #{i+1}", value=DEFAULT_LABELS[i], key=f"lbl_{i}")
                labels.append(lab)
                bt = st.number_input(f"Build time ({lab})", min_value=1, value=DEFAULT_BUILD_TIME[i], key=f"bt_{i}")
                build_times.append(int(bt))
                rt = st.number_input(f"Rate ({lab})", min_value=0, value=DEFAULT_RATE[i], key=f"rt_{i}")
                rates.append(int(rt))

        n = st.number_input("Total time units (n)", min_value=0, value=30, step=1, key="n_input")
        submitted = st.form_submit_button("Compute")

    if submitted:
        profit, counts, schedule, dp_array, total_time_used = max_profit(n, build_times, rates, labels)
        st.success("Optimization complete")

        # Professional KPI cards: profit, total builds, avg revenue per build, efficiency
        total_builds = sum(counts.values())
        avg_rev_per_build = int(profit / total_builds) if total_builds > 0 else 0
        utilization_pct = round(100 * total_time_used / n, 2) if n > 0 else 0.0
        efficiency_score = round(profit / total_time_used, 2) if total_time_used > 0 else 0.0

        col_a, col_b, col_c, col_d = st.columns([2,1,1,1.6])
        with col_a:
            st.metric("Max Earnings", f"${int(profit):,}")
        with col_b:
            st.metric("Total Builds", f"{total_builds}")
        with col_c:
            st.metric("Avg Rev / Build", f"${avg_rev_per_build:,}")
        with col_d:
            st.metric("Utilization", f"{utilization_pct}%")
            st.write(f"Efficiency: ${efficiency_score}/time")

        st.subheader("Build counts")
        cnt_df = pd.DataFrame(list(counts.items()), columns=["Type", "Count"])
        st.table(cnt_df)

        st.subheader("Schedule")
        if schedule:
            df = pd.DataFrame(schedule)[["start", "end", "type", "duration", "revenue"]]
            df["revenue"] = df["revenue"].map(lambda x: f"${int(x):,}")
            st.dataframe(df.reset_index(drop=True), use_container_width=True)
            # store latest for visualization/export pages
            st.session_state["latest_result"] = {
                "n": n,
                "labels": labels,
                "build_times": build_times,
                "rates": rates,
                "profit": int(profit),
                "counts": counts,
                "schedule_df": df,
                "dp_array": dp_array,
                "total_time_used": total_time_used
            }
        else:
            st.info("No builds scheduled for this horizon.")

# ------------------------
# VISUALIZATION
# ------------------------
elif page == "Visualization":
    st.header("Visualization & Analysis")
    if "latest_result" not in st.session_state:
        st.warning("Run the Optimizer first to produce results.")
    else:
        res = st.session_state["latest_result"]
        df = res["schedule_df"].copy()
        n = res["n"]
        labels = res["labels"]
        build_times = res["build_times"]
        rates = res["rates"]
        profit = res["profit"]
        counts = res["counts"]
        total_time_used = res["total_time_used"]

        st.subheader("Build distribution (counts)")
        cnt_items = sorted(counts.items(), key=lambda x: x[0])
        names = [k for k, _ in cnt_items]
        vals = [v for _, v in cnt_items]
        bar_fig = go.Figure(data=[go.Bar(x=names, y=vals, marker_color=PRIMARY_COLOR)])
        bar_fig.update_layout(title="Counts by Build Type", xaxis_title="Type", yaxis_title="Count", height=360)
        st.plotly_chart(bar_fig, use_container_width=True)

        st.subheader("Schedule timeline")
        if not df.empty:
            timeline_fig = go.Figure()
            for idx, row in df.reset_index().iterrows():
                timeline_fig.add_trace(go.Bar(
                    x=[row["duration"]],
                    y=[f"Build {idx+1}"],
                    base=[row["start"]],
                    orientation='h',
                    name=row["type"],
                    hovertemplate=f"Type: {row['type']}<br>Start: {row['start']}<br>End: {row['end']}<br>Revenue: {row['revenue']}"
                ))
            timeline_fig.update_layout(title="Schedule Timeline", xaxis_title="Time", yaxis=dict(autorange="reversed"), height=380)
            st.plotly_chart(timeline_fig, use_container_width=True)

        st.markdown("---")
        st.subheader("Efficiency & utilization")
        utilization_pct = round(100 * total_time_used / n, 2) if n > 0 else 0.0
        efficiency_score = round(profit / total_time_used, 2) if total_time_used > 0 else 0.0
        st.write(f"Total time used: **{total_time_used}** out of **{n}** ({utilization_pct}%).")
        st.write(f"Efficiency (profit per time unit used): **${efficiency_score}**")

# ------------------------
# COMPARISON (build types)
# ------------------------
elif page == "Comparison":
    st.header("Comparison: Build Types & Schedule Contribution")
    # require latest_result to compute potential revenue baseline using current n
    if "latest_result" not in st.session_state:
        st.info("Run the Optimizer first to get current inputs (n, build types).")
    else:
        res = st.session_state["latest_result"]
        n = res["n"]
        labels = res["labels"]
        build_times = res["build_times"]
        rates = res["rates"]
        df = res["schedule_df"].copy()

        st.subheader("Per-type comparison (rate, duration, potential revenue)")
        comp_fig = plot_build_comparison(n, build_times, rates, labels)
        st.plotly_chart(comp_fig, use_container_width=True)

        st.subheader("Schedule composition")
        contrib_fig = plot_schedule_contribution(df, labels)
        st.plotly_chart(contrib_fig, use_container_width=True)

        st.markdown("---")
        st.write("Use these charts to explain why the optimizer prefers certain builds (rate vs duration trade-off).")

# ------------------------
# DOWNLOAD CENTER
# ------------------------
elif page == "Download Center":
    st.header("Export results & Summary PDF")
    if "latest_result" not in st.session_state:
        st.warning("Run the Optimizer first to produce exportable results.")
    else:
        res = st.session_state["latest_result"]
        df = res["schedule_df"].copy()
        profit = res["profit"]
        counts = res["counts"]
        n = res["n"]
        labels = res["labels"]
        build_times = res["build_times"]
        rates = res["rates"]
        dp_array = res["dp_array"]
        total_time_used = res["total_time_used"]

        st.subheader("CSV export")
        csv_buf = io.StringIO()
        save_df = df.copy()
        save_df["revenue"] = save_df["revenue"].replace('[\$,]', '', regex=True).astype(int)
        save_df.to_csv(csv_buf, index=False)
        st.download_button("Download schedule CSV", data=csv_buf.getvalue(), file_name="schedule.csv", mime="text/csv")

        st.markdown("---")
        st.subheader("Summary PDF (ReportLab required)")
        st.write("The PDF includes KPIs, efficiency metrics, schedule, and a DP sample.")
        if REPORTLAB_AVAILABLE:
            name = st.text_input("Name (for report)", value=DEFAULT_AUTHOR, key="report_name")
            if st.button("Generate & Download Summary PDF"):
                try:
                    pdf_bytes = generate_pdf_bytes(save_df, profit, counts, n, build_times, rates, labels, dp_array, total_time_used, author=name)
                    st.success("PDF generated.")
                    st.download_button("Download Summary PDF", data=pdf_bytes, file_name="max_profit_summary.pdf", mime="application/pdf")
                except Exception as e:
                    st.error(f"PDF generation failed: {e}")
        else:
            st.error("ReportLab not installed. Install with:")
            st.code("pip install reportlab==3.6.12", language="bash")
            st.info("After installing, re-run the app to enable PDF generation.")

# ------------------------
# ABOUT
# ------------------------
elif page == "About":
    st.header("About & Technical Notes")
    st.markdown(
        """
        Project: Max Profit Builder Scheduler — Enhanced

        Approach: Dynamic Programming — compute f[t] = max achievable profit from time t to n; reconstruct schedule with choices.
        Enhancements in this version:
        - Build type comparison charts
        - Efficiency & utilization KPIs
        - Enhanced PDF summary including efficiency metrics

        Stack: Streamlit, Python, Pandas, Plotly, ReportLab (for PDF output).
        """
    )
    st.markdown("---")
    st.write("This app is intended to present a compact optimization tool with analysis features suitable for demonstration and decision support.")

# End of file
