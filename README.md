# Multi-Agent Research Assistant System

An autonomous LLM-powered agent team designed to extract, cluster, and reason over scientific papers — generating structured reviews, identifying thematic contradictions, and proposing follow-up experiments.

## Project Goals

- Automate literature review workflows
- Cross-reference research papers by methods, outcomes, and contradictions
- Propose follow-up experiments using LLM reasoning

## System Overview

This system uses a team of large language model agents:
- `ExtractorAgent`: parses raw papers (PDF/HTML/text) into structured JSON (title, abstract, methods, results)
- `ClusteringAgent`: identifies topic clusters or conflicting findings
- `HypothesisAgent`: generates new questions or experimental ideas

Each agent runs independently, shares memory, and collaborates via a central controller.

## Technologies

- **LLM Backend**: OpenAI GPT-4 or Claude 3
- **Orchestration**: LangChain (or AutoGen / CrewAI)
- **Memory Store**: FAISS or ChromaDB
- **Containerization**: Docker
- **Frontend (optional)**: Streamlit, Gradio, or FastAPI