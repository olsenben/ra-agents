from agents.utils import call_gpt4

def generate_hypothesis(title: str, abstract: str, url: str) -> dict:
    prompt = f"""
You are a scientific researcher. Based on the following paper's title and abstract, 
suggest one or two follow-up research questions or experiments. 

Title: {title}
Abstract: {abstract}
"""
    
    messages = [
        {"role": "system", "content": "You are an assistant that extracts scientific insights."},
        {"role" : "user", "content": prompt}
    ]

    hypothesis = call_gpt4(messages)

    return {
        "title" : title,
        "url" : url,
        "hypothesis" : hypothesis
    }