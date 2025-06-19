import gradio as gr
import plotly.graph_objects as go

def display_kpi_dashboard(critique_result, rag_impact_kpis, real_world_kpis):
    # Classify KPIs into Vanity or Impact based on critique
    vanity_kpis = []
    impact_kpis = []

    for kpi, feedback in critique_result.items():
        label = feedback.lower()
        if "vanity" in label:
            vanity_kpis.append((kpi, "Low Relevance"))
        elif "impact" in label or "core" in label:
            impact_kpis.append((kpi, "High Relevance"))
        else:
            impact_kpis.append((kpi, "Medium Relevance"))

    # Combine with other KPI sources
    for kpi in rag_impact_kpis:
        impact_kpis.append((kpi, "High Relevance"))
    for kpi in real_world_kpis:
        if kpi not in [v[0] for v in impact_kpis]:
            impact_kpis.append((kpi, "Medium Relevance"))

    # Prepare data for Plotly charts
    vanity_labels = [k[0] for k in vanity_kpis]
    vanity_values = [1] * len(vanity_kpis)  # dummy values
    vanity_tags = [k[1] for k in vanity_kpis]

    impact_labels = [k[0] for k in impact_kpis]
    impact_values = [1] * len(impact_kpis)
    impact_tags = [k[1] for k in impact_kpis]

    # Vanity KPI Chart
    fig_vanity = go.Figure(data=[
        go.Bar(
            x=vanity_values,
            y=vanity_labels,
            orientation='h',
            marker=dict(color='tomato'),
            text=vanity_tags,
            textposition="outside",
            name="Vanity Metrics"
        )
    ])
    fig_vanity.update_layout(title="Vanity Metrics", xaxis_visible=False, height=400)

    # Impact KPI Chart
    fig_impact = go.Figure(data=[
        go.Bar(
            x=impact_values,
            y=impact_labels,
            orientation='h',
            marker=dict(color='mediumseagreen'),
            text=impact_tags,
            textposition="outside",
            name="Impact Metrics"
        )
    ])
    fig_impact.update_layout(title="Impact Metrics", xaxis_visible=False, height=400)

    # Gradio layout
    with gr.Blocks(title="KPI Insight Dashboard") as demo:
        gr.Markdown("## Insight Visualizer – Vanity vs Impact Metrics")

        with gr.Row():
            gr.Plot(fig_vanity, label="Vanity Metrics")
            gr.Plot(fig_impact, label="Impact Metrics")

        gr.Markdown("### Growth Relevance Tags")
        gr.Markdown("- **High Relevance** → Strategic for product/market fit\n"
                    "- **Medium Relevance** → Useful, but situational\n"
                    "- **Low Relevance** → Likely vanity or surface-level")

    demo.launch()
