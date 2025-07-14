from agents.utils import call_gpt4

def generate_hypothesis(cluster_data: dict) -> dict:
    """
    accepts a clustering output dict with "theme_summaries" and "contradictions."

    returns a list of suggested follow-up research questions or hypothesis.
    """
    
    contradictions = cluster_data.get("contradictions","")

    theme_summaries = []

    for cluster in cluster_data.get('clusters', []):
        theme_summaries.append(
            f"Title: {cluster['theme']}\n"
            f"Authors: {cluster['summary']}\n"
            f"Summary: {cluster['papers']}\n"
        )

    prompt = (
        "You are a scientific research assistant.\n\n"
        "Below are the thematic summaries of several scientific papers and a list of contradictions or gaps in findings.\n"
        "Suggest 3–5 specific follow-up research questions or hypotheses based on these summaries.\n"
        "These suggestions should aim to address unresolved issues, validate uncertain findings, or build on promising directions.\n"
        "Please directly reference authors and claims to support your suggestions.\n\n"
        "### Thematic Summaries:\n"
        + "\n\n".join(theme_summaries) +
        "\n\n### Contradictions or Gaps:\n"
        + "\n\n".join(contradictions)
    )

    
    messages = [
        {"role": "system", "content": "You are an assistant that extracts scientific insights."},
        {"role" : "user", "content": prompt}
    ]

    hypothesis = call_gpt4(messages)

    return {
        "hypothesis" : hypothesis.strip()
    }