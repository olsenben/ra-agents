import re
import json
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
    # prompt = (
    #     "You are a research analyst reviewing scientific papers. Group them into clusters based on shared themes (titled with format: ### Cluster 1, ### Cluster 2 etc).\n\n"
    #     "For each cluster:\n"
    #     "1. Provide a short title summarizing the theme\n"
    #     "2. Summarize the theme in 1-2 sentences (if there are results discussed in the papers, include them in these sentences)(user sub header format '**Theme Summary**').\n"
    #     "3. List the titles of the papers for reference in the cluster (user header formatted: '**Papers**'\n\n"
    #     "After the clusters, identify any contradictions or gaps you observed across the papers (user header formated: ### Contradictions or Gaps Observed).\n\n"
    #     "Here are the papers:\n\n"
    #     + "\n\n".join(formatted_summaries)
    # )

    # messages = [
    #     {"role": "system", "content": "You are an assistant that clusters scientific papers by topic."},
    #     {"role": "user", "content": prompt}
    # ]

    # result = call_gpt4(messages).strip()

    # # -------------------------------
    # # Parse GPT response
    # # -------------------------------

    # # Sample expected format:
    # # ### Cluster 1: Immune Response Mechanisms
    # # Summary: These papers discuss...
    # # Papers:
    # # - Title A
    # # - Title B
    # #Contradictions or Gaps Observed
    
    # print(result)
    # clusters = []
    
    # parts = re.split(r"### Contradictions or Gaps Observed", result)
    # clusters_text = parts[0].strip()
    # contradictions_section = parts[1].strip() if len(parts) > 1 else ""

    # # Now split remaining by clusters
    # cluster_blocks = re.split(r"### Cluster \d+:", clusters_text)

    # for block in cluster_blocks:
    #     if not block.strip():
    #         continue  # skip empty strings

    #     # Extract theme title
    #     theme_match = re.match(r"\s*(.+?)\n", block)
    #     theme = theme_match.group(1).strip() if theme_match else "Unnamed Cluster"

    #     # Extract summary
    #     summary_match = re.search(
    #     r"\*\*Theme Summary\*\*.*?(?=\n### Cluster|\n### Contradictions|\Z)", 
    #         block, 
    #         re.DOTALL
    #     )        
    #     summary = summary_match.group(1).strip() if summary_match else "No summary found."

    #     # Extract paper titles (assumes numbered list)
    #     titles_match = re.findall(r'-\s*"?(.+?)"?$', block, re.MULTILINE)
    #     matched_papers = []

    #     for title in titles_match:
    #         match = get_close_matches(title, [p["title"] for p in paper_summaries], n=1, cutoff=0.7)
    #         if match:
    #             matched = next(p for p in paper_summaries if p["title"] == match[0])
    #             matched_papers.append(matched)

    #     clusters.append({
    #         "theme": theme,
    #         "summary": summary,
    #         "papers": matched_papers
    #     })
    # return {
    #     "clusters": clusters,
    #     "contradictions": contradictions_section.strip() if contradictions_section else ""
    # }

    prompt = (
        "You are a research analyst reviewing scientific papers. Group them into clusters based on shared themes.\n\n"
        "Return your response as a **valid JSON object** with this format:\n"
        "{\n"
        "  \"clusters\": [\n"
        "    {\n"
        "      \"theme\": \"<Short descriptive title for the theme>\",\n"
        "      \"summary\": \"<1-2 sentence summary of the theme. Include notable findings or insights, and cite relevant authors>\",\n"
        "      \"papers\": [\n"
        "        {\n"
        "          \"title\": \"<Paper title>\",\n"
        "          \"authors\": [\"Author One\", \"Author Two\"]\n"
        "        }\n"
        "      ]\n"
        "    }\n"
        "  ],\n"
        "  \"contradictions_or_gaps\": [\n"
        "    \"<Contradiction or gap 1>\",\n"
        "    \"<Contradiction or gap 1>\",\n"
        "    ...\n"
        "  ]\n"
        "}\n\n"
        "Return ONLY the JSON — no preamble, no explanation, no markdown formatting like triple backticks.\n\n"
        "Here are the papers:\n\n"
        + "\n\n".join(formatted_summaries)
    )

    messages = [
        {"role": "system", "content": "You are an assistant that clusters scientific papers by topic."},
        {"role": "user", "content": prompt}
    ]

    result = call_gpt4(messages).strip()
    parsed_result = json.loads(result)
    return parsed_result