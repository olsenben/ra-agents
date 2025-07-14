from agents.utils import call_gpt4

def extract_paper_summary(title: str, abstract: str, url: str) -> dict:
    prompt = f"""
You are a scientific assistant. Given the title and abstract of a research paper, 
extract the main claim and the key methods used. Respond in JSON format with keys: title, claim, methods.

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
        "summary" : output
    }