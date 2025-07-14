from agents.extractor_agent import extract_paper_summary
from agents.hypothesis_agent import generate_hypothesis
from agents.clustering_agent import cluster_papers
from paper_search.papersearch import search_papers


def run_extraction_pipeline(query:str, num_papers: int = 3):
    print(f"\n Searching for papers about: {query}")
    papers = search_papers(query, limit=num_papers)

    print(f"Running extractor agent on top {len(papers)} papers... \n")
    for i, paper in enumerate(papers, start=1):
        result = extract_paper_summary(
            title=paper['title'],
            abstract=paper['abstract'],
            url=paper['url']
        )

        hypothesis = generate_hypothesis(
            title=paper['title'],
            abstract=paper['abstract'],
            url=paper['url']
        )

        print(f"\n=== Paper #{i} ===")
        print(f"Title: {result['title']}")
        print(f"URL: {result['url']}")
        print(f"\n Extracted Summary:\n{result['summary']}")
        print("\n------------------------\n")

    

if __name__=="__main__":
    topic = input("Enter a research topic: ")
    num_papers = int(input("Enter top number of results: "))
    while num_papers is not int: 
        num_papers  = int(input("Enter top number of results: "))
    run_extraction_pipeline(topic, num_papers)

