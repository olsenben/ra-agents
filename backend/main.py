from agents.extractor_agent import extract_paper_summary
from agents.hypothesis_agent import generate_hypothesis
from agents.clustering_agent import cluster_papers
from paper_search.papersearch import search_papers


def build_pipeline(query:str, limit: int = 3) -> dict:
    print(f"\nSearching for papers about: {query}")
    papers = search_papers(query, limit=limit)
    print(f"Extracting summaries from {len(papers)} papers... \n")

    summarized_papers = []

    for i, paper in enumerate(papers, start=1):
        result = extract_paper_summary(paper)
        summarized_papers.append(result)

        print(f"\n=== Paper #{i} ===")
        print(f"Title: {result['title']}")
        print(f"Authors: {result['authors']}")
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
    results = build_pipeline(topic, num_papers)
    #print(json.dumps(results, indent=2))

    for i, cluster in enumerate(results['clusters']['clusters'], 1):
        print(f"\n=== Cluster #{i} ===")
        print(f"Theme: {cluster['theme']}")
        print(f"Summary: {cluster['summary']}")
        print(f"\nPapers:")
        for paper in cluster["papers"]:
            title = paper.get("title", "")
            print(f"- {title}")
    
    print("\n------------------------\n")

    print(f"\n=== Contradictions or Gaps ===")
    for gap in results['clusters']['contradictions_or_gaps']:
        print(f"- {gap}")

    print(f"\n=== Suggested Follow-up Hypothesis ===")
    print(results.get('follow_up_hypothesis',{}).get('hypothesis'))