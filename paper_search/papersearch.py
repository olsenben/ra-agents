import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("SEMANTIC_SCHOLAR_API_KEY")


BASE_URL = 'https://api.semanticscholar.org/graph/v1'
SEARCH_ENDPOINT = f'{BASE_URL}/paper/search'

#fields to match what agents needs
FIELDS = 'title,abstract,url,authors'

HEADERS = {"x-api-key": api_key}

def search_papers(query, limit = 10):
    """
    Search Semantic Scholar for papers matching a topic. 
    REturns list of papers dicts with title, abstract, url and authors. 
    """

    params = {
        "query" : query,
        "limit" : limit,
        "fields": FIELDS
    }

    response = requests.get(SEARCH_ENDPOINT, params=params, headers=HEADERS)
    response.raise_for_status()

    papers = response.json().get("data", [])

    #reformat
    results = []
    for paper in papers: 
        results.append({
            "title" : paper.get('title'),
            "abstract" : paper.get('abstract'),
            "url" : paper.get('url'),
            "authors" : [a.get('name') for a in paper.get('authors', [])]
        })

    return results