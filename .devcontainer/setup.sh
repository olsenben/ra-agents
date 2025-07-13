#!/bin/bash

# Install requirements
pip install -r /workspaces/ra-agents/requirements.txt

# Add PYTHONPATH to ~/.bashrc so it's available in every terminal/session
echo "export PYTHONPATH=/workspaces/ra-agents/agents:/workspaces/ra-agents/paper_search" >> ~/.bashrc
