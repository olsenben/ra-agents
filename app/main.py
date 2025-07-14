from agents.extractor_agent import extract_paper_summary
from agents.hypothesis_agent import generate_hypothesis
from agents.clustering_agent import cluster_papers
from paper_search.papersearch import search_papers
import json


def build_pipeline(query:str, num_papers: int = 3) -> dict:
    print(f"\n Searching for papers about: {query}")
    papers = search_papers(query, limit=num_papers)
    print(f"Extracting summaries from {len(papers)} papers... \n")

    summarized_papers = []

    for i, paper in enumerate(papers, start=1):
        result = extract_paper_summary(
            title=paper['title'],
            abstract=paper['abstract'],
            url=paper['url']
        )
        summarized_papers.append(result)

        print(f"\n=== Paper #{i} ===")
        print(f"Title: {result['title']}")
        print(f"URL: {result['url']}")
        print(f"\n Extracted Summary:\n{result['summary']}")
        print("\n------------------------\n")

    print("Clustering...")
    clusters = cluster_papers(summarized_papers)

    print("Generating hypothesis... ")
    hypothesis = generate_hypothesis(clusters)

    return {
        "query" : query,
        "papers" : summarized_papers,
        "clusters" : clusters,
        "follow_up_hypothesis" : hypothesis
    }

if __name__=="__main__":
    topic = input("Enter a research topic: ")
    num_papers = int(input("Enter top number of results: "))
    while not isinstance(num_papers, int): 
        num_papers  = int(input("Enter top number of results: "))
    output = build_pipeline(topic, num_papers)
    print(json.dumps(output, indent=2))


