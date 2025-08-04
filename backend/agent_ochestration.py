from agents.extractor_agent import extract_paper_summary
from agents.clustering_agent import cluster_papers
from agents.hypothesis_agent import generate_hypothesis
from paper_search.papersearch import search_papers

def build_pipeline(query:str, num_papers: int = 3) -> dict:
    
    papers = search_papers(query, limit=num_papers)

    summarized_papers = []

    for paper in papers:
        result = extract_paper_summary(paper)
        summarized_papers.append(result)


    clusters = cluster_papers(summarized_papers)

    hypothesis = generate_hypothesis(clusters)

    return {
        "query" : query,
        "papers" : summarized_papers,
        "clusters" : clusters,
        "follow_up_hypothesis" : hypothesis
    }