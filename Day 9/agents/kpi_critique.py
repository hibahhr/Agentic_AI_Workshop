def critique_kpis_with_llm(kpis, context, llm):
    import ast

    prompt = f"""
You are a KPI analysis expert for startups.

Startup Type: {context['type']}
Startup Stage: {context['stage']}

Classify each of the following KPIs as either a 'Vanity Metric' or an 'Impact Metric'.
Provide your answer as a Python dictionary in the following format:

{{
  "App Downloads": "Vanity Metric - Downloads don't guarantee active usage.",
  "GMV": "Impact Metric - Reflects actual transactional volume.",
  "Instagram Likes": "Vanity Metric - Indicates visibility but not conversions."
}}

Only return the dictionary. Do not add extra explanation or formatting.

KPIs to evaluate: {', '.join(kpis)}
"""
    response = llm.invoke(prompt).content.strip()
    if "```" in response:
        response = response.split("```")[1].strip()
        if response.startswith("python") or response.startswith("json"):
            response = "\n".join(response.split("\n")[1:]).strip()
    try:
        return ast.literal_eval(response)
    except (ValueError, SyntaxError):
        print("\u26a0\ufe0f Failed to parse cleaned response:\n", response)
        return {k: "Unclassified - Unable to parse response" for k in kpis}
