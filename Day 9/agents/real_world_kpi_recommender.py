def recommend_kpis_from_web(startup_context, critique, rag_kpis, llm, tavily):
    prompt_context = f"""
Startup Type: {startup_context['type']}
Startup Stage: {startup_context['stage']}
Metric Focus: {startup_context['relevant_metric_focus']}

Critiqued KPIs with classification:
{critique}

Suggested Impact KPIs from internal knowledge base (RAG):
{rag_kpis}
"""
    query = f"Real-world KPIs used by {startup_context['stage']} stage {startup_context['type']} startups focused on {startup_context['relevant_metric_focus']}"
    try:
        search_results = tavily.search(query=query, search_depth="advanced", max_results=3)
        web_context = "\n".join([res['content'] for res in search_results['results']])
    except Exception as e:
        print("\u26a0\ufe0f Tavily Web Search failed:", e)
        web_context = ""

    prompt = f"""
You are a KPI expert assistant helping a startup refine its metrics.

Here is internal analysis:
{prompt_context}

Here is web research content:
{web_context}

From the above, recommend 5-7 high-quality **impact KPIs** that align with the startup context and reflect real-world best practices.

Output a list of KPIs only. No explanation.
"""
    response = llm.invoke(prompt).content.strip()
    return [kpi.strip("-\u2022 ").strip() for kpi in response.split("\n") if kpi.strip()]
