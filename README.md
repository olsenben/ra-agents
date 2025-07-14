# Multi-Agent Research Assistant System

An autonomous LLM-powered agent team designed to extract, cluster, and reason over scientific papers — generating structured summaries, identifying thematic contradictions, and proposing follow-up experiments.

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
- **Memory Store**: None for now
- **Containerization**: Docker
- **Backend**: FastAPI
- **Frontend**: Streamlit


## RUN
run API ```uvicorn app.api:app --host 0.0.0.0 --port 8000```
launch streamlit ```cd frontend``` then ```streamlit run streamlit_app.py``` then navigate to ```http://localhost:8501/```

