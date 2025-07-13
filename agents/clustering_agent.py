from agents.utils import call_gpt4

def cluster_papers(paper_summaries: list[dict]) -> dict:
    """
    Input format:
    [
        {"title": ..., "claim": ..., "url": ...},
        ...
    ]
    """
    papers_text = "\n".join(
        f"- {p['title']}: {p.get('claim', 'No claim provided')}" for p in paper_summaries
    )

    prompt = f"""
You are a clustering assistant. Based on the following papers and their main claims,
group them into thematic clusters and identify any conflicting findings.
Respond in JSON with two keys:
- "clusters": list of cluster names and associated paper titles
- "conflicts": list of any contradictory findings

{papers_text}
"""
    
    messages = [
        {"role" : "system", "content": "You are an assistant that clusters scientific papers by topic."},
        {"role" : "user", "content" : prompt}
    ]

    result =  call_gpt4(messages)

    return {
        "input_papers" : paper_summaries,
        "clustering_result" : result
    }