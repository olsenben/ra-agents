# Multi-Agent Research Assistant System
![RA Agents Demo](https://i.imgur.com/vdE9Ezb.gif) 

An autonomous LLM-powered agent team designed to extract, cluster, and reason over scientific papers. It generates structured summaries, identifies thematic contradictions, and proposes follow-up experiments. 

## Project Goals

- Automate literature review workflows
- Cross-reference research papers by methods, outcomes, and contradictions
- Propose follow-up experiments using LLM reasoning

## System Overview

This system uses a team of large language model agents:
- `ExtractorAgent`: summarizes papers requested from semantic scholar API (I requested my own API key but publics keys are available)
- `ClusteringAgent`: identifies topic clusters and conflicting findings
- `HypothesisAgent`: generates new questions or experimental ideas

Each agent runs independently and collaborates via a central controller.

## Technologies

- **LLM Backend**: OpenAI GPT-4
- **Orchestration**: Custom
- **Memory Store**: MongoDB
- **Containerization**: Docker
- **Backend**: FastAPI, pydantic (schema validation), aioredis (rate limiting)
- **Frontend**: Streamlit
- **Auth**: Firebase



## RUN
- If you are using vscode, reopen the directory using the provided ```.devcontainer```.
- Add your API keys to your ```.env``` (example is included)
- To run API ```uvicorn app.api:app --host 0.0.0.0 --port 8000```
- To launch streamlit ```cd frontend``` then ```streamlit run streamlit_app.py``` then navigate to ```http://localhost:8501/``` or whichever is specified

**OR**
- To run via your terminal, run ```main.py```.

