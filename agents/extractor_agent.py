from agents.utils import call_gpt4

def extract_paper_summary(paper: dict) -> dict:
    "accepts dictionary of paper info and returns dictionary of paper info with summary"

    title = paper['title']
    abstract = paper['abstract']
    url = paper['url']
    authors = paper['authors']

    prompt = f"""
You are a scientific assistant. Given the title and abstract of a research paper, 
extract the main claim and the key methods used. Respond with sub headers claims and methods in markdown format.

Title: {title}
Abstract: {abstract}
"""
    
    messages = [
        {"role": "system", "content": "You are an assistant that extracts scientific insights."},
        {"role" : "user", "content": prompt}
    ]

    output = call_gpt4(messages)
    return {
        'title' : title,
        "abstract" : abstract,
        "url" : url, 
        "authors" : authors,
        "summary" : output
    }