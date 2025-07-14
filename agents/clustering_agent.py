from agents.utils import call_gpt4

def cluster_papers(paper_summaries: list[dict]) -> dict:
    """
    Input format:
    [
        {"title": ..., "authors": ..., "summary": ...},
        ...
    ]

    Returns thematic clustering of summaries 
    """
    formatted_summaries = []

    for s in paper_summaries:
        authors_str = ",".join(s.get('authors',[])) or "Unknown authors"
        formatted_summaries.append(
            f"Title: {s['title']}\n"
            f"Authors: {authors_str}\n"
            f"Summary: {s['summary']}\n"
        )

    prompt = (
        "You are a research analyst reviewing scientific paper summaries. "
        "Group the papers into thematic clusters based on their summaries. "
        "Label each cluster and list the papers (with authors) under each. "
        "Then identify any contradictions or disagreements across the summaries.\n\n"
        "Return two sections:\n"
        "1. Theme Clusters\n2. Contradictions or Gaps in Findings\n\n"
        "Here are the papers:\n\n"
        + "\n\n".join(formatted_summaries)
    )

    
    messages = [
        {"role" : "system", "content": "You are an assistant that clusters scientific papers by topic."},
        {"role" : "user", "content" : prompt}
    ]

    result =  call_gpt4(messages)
    full_output = result.strip()

    if "Contradictions" in full_output:
        theme_part, contradiction_part = full_output.split("Contradictions", 1)
        theme_part = theme_part.replace("Theme Clusters", "").strip()
        contradiction_part = contradiction_part.replace("Contradictions", "").strip()
    else:
        theme_part = full_output
        contradiction_part = "No contradictions were found or specified"


    return {
        "clusters" : {
            "theme_summaries" : theme_part,
            "contradictions" : contradiction_part
        }
    }