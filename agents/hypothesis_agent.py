from agents.utils import call_gpt4

def generate_hypothesis(cluster_data: dict) -> dict:
    """
    accepts a clustering output dict with "theme_summaries" and "contradictions."

    returns a list of suggested follow-up research questions or hypothesis.
    """
    
    theme_summaries = cluster_data.get("clusters",{}).get("theme_summaries","")
    contradictions = cluster_data.get("clusters",{}).get("contradictions","")

    prompt = f"""
You are a scientific researcher assistant. Given the following thematic summary of several scientific papers
and a list of contradictions or gaps, suggest 3–5 specific follow-up research questions or hypotheses 
that could help address unresolved issues, validate uncertain findings, or build on promising directions.
Please directly reference authors and claims to support suggestions. 

### Thematic Summaries:
{theme_summaries}

### Contradictions or Gaps:
{contradictions}
"""
    
    messages = [
        {"role": "system", "content": "You are an assistant that extracts scientific insights."},
        {"role" : "user", "content": prompt}
    ]

    hypothesis = call_gpt4(messages)

    return {
        "hypothesis" : hypothesis.strip()
    }