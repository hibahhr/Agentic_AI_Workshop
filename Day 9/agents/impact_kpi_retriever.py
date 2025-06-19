def retrieve_impact_kpis(context, qa_chain):
    query = f"What are the most impactful KPIs for a {context['type']} startup in the {context['stage']} stage focused on {context['relevant_metric_focus']}?"
    result = qa_chain.run(query)
    return [kpi.strip("-\u2022 ").strip() for kpi in result.split("\n") if kpi.strip()]
