import re
from difflib import get_close_matches
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

        # Create prompt for GPT
    prompt = (
        "You are a research analyst reviewing scientific papers. Group them into clusters based on shared themes.\n\n"
        "For each cluster:\n"
        "1. Provide a short title summarizing the theme\n"
        "2. Summarize the theme in 1-2 sentences\n"
        "3. List the titles of the papers in the cluster\n\n"
        "After the clusters, identify any contradictions or gaps you observed across the papers.\n\n"
        "Here are the papers:\n\n"
        + "\n\n".join(formatted_summaries)
    )

    messages = [
        {"role": "system", "content": "You are an assistant that clusters scientific papers by topic."},
        {"role": "user", "content": prompt}
    ]

    result = call_gpt4(messages).strip()

    # -------------------------------
    # Parse GPT response
    # -------------------------------

    # Sample expected format:
    # ### Cluster 1: Immune Response Mechanisms
    # Summary: These papers discuss...
    # Papers:
    # - Title A
    # - Title B

    clusters = []
    cluster_blocks = re.split(r"(?=### Cluster \d+:)", result)

    contradiction_text = ""
    if "Contradictions" in cluster_blocks[-1]:
        *cluster_blocks, contradiction_text = cluster_blocks

    for block in cluster_blocks:
        theme_match = re.search(r"### Cluster \d+: (.+)", block)
        summary_match = re.search(r"Summary: (.+?)\n(?:Papers|Paper Titles|–|—)", block, re.DOTALL)
        titles_match = re.findall(r"- (.+)", block)

        if not (theme_match and summary_match and titles_match):
            continue

        theme = theme_match.group(1).strip()
        summary = summary_match.group(1).strip()
        paper_titles = [t.strip() for t in titles_match]

        # Match back to original papers
        matched_papers = []
        for title in paper_titles:
            # Fuzzy match to handle slight GPT variation
            match = get_close_matches(title, [p["title"] for p in paper_summaries], n=1, cutoff=0.7)
            if match:
                matched = next(p for p in paper_summaries if p["title"] == match[0])
                matched_papers.append(matched)

        clusters.append({
            "theme": theme,
            "summary": summary,
            "papers": matched_papers
        })

    return {
        "clusters": clusters,
        "contradictions": [contradiction_text.strip()] if contradiction_text else []
    }