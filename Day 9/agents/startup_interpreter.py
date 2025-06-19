def interpret_startup(startup_info, llm, tavily):
    import ast

    query = f"KPI priorities for a {startup_info['stage']} stage {startup_info['type']} startup"
    try:
        search_results = tavily.search(query=query, search_depth="advanced", max_results=3)
        context_snippets = "\n".join([res['content'] for res in search_results['results']])
    except Exception as e:
        context_snippets = "No relevant context found from Tavily."
        print("\u26a0\ufe0f Tavily failed:", e)

    prompt = f"""
You are a startup KPI expert.

Here is some context from web research on the startup type and stage:
{context_snippets}

Given the following startup information:
- Type: {startup_info["type"]}
- Stage: {startup_info["stage"]}

Analyze the startup model and stage to contextualize KPI needs.

Suggest what the startup's core metric focus should be at this stage (e.g., retention, GMV, engagement, churn, growth, etc.).
Return the output as a Python dictionary with keys: type, stage, relevant_metric_focus.
"""
    response = llm.invoke(prompt).content.strip()
    if "```" in response:
        response = response.split("```")[1].strip()
    try:
        return ast.literal_eval(response)
    except (ValueError, SyntaxError):
        return {
            "type": startup_info["type"],
            "stage": startup_info["stage"],
            "relevant_metric_focus": "growth"
        }
