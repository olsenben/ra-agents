import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()


password = st.text_input("Password", type="password")
if password != st.secrets["STREAMLIT_PASSWORD"]:
    st.stop()

API_URL = "https://ra-agents.fly.dev/analyze"
API_KEY = os.environ.get("FLY_API_TOKEN") 

st.title("Multi-Agent Research Assistant")

query = st.text_input("Enter a research topic", "glioblastoma")
limit = st.slider("Number of papers to analyze", 1,20,5)

if st.button("Analyze"):
    
    with st.spinner("Running multi-agent pipeline..."):
        try:
            response = requests.get(
                API_URL, 
                params={
                    "query" : query,
                    "limit" : limit
                    },
                headers = {
                    "X-API-Key": API_KEY
                    })
            
            response.raise_for_status()
            data = response.json()

            st.header(f"Found Papers: {len(data['papers'])}")

            #display summarized papers
            for idx, paper in enumerate(data['papers'], 1):
                with st.expander(f"**{idx}. {paper['title']}**"):
                    authors_str = " ,".join(paper.get('authors',[])) or "Unknown authors"
                    st.markdown(f"**Authors:** {authors_str}")
                    st.markdown(f"**URL:** [{paper['url']}]({paper['url']})")
                    #st.markdown(f"**Summary:**")
                    st.markdown(f"{paper['summary']}")


            st.success(f"Found {len(data['clusters']['clusters'])} Thematic Clusters...")
            
            st.header("Clusters")

            #display clusters 
            for idx, cluster in enumerate(data['clusters']['clusters'], 1):
                cluster_theme = cluster.get('theme', "")
                st.subheader(f"Cluster {idx}: {cluster_theme}")
                st.markdown(cluster['summary'])
                st.write("\nPapers:")
                for paper in cluster["papers"]:
                    title = paper.get("title", "")
                    st.markdown(f"- {title}") 

            st.header("Contradicitons or Gaps")   
            contradictions = data['clusters'].get('contradictions_or_gaps', '### No Contradicitons Found')
            if contradictions: 
                for gap in contradictions:
                    st.markdown(f"- {gap}")

            #display hypothesis
            st.header("Suggested Follow-up Hypothesis")
            hypothesis = data.get('follow_up_hypothesis',{})
            hypothesis_text = hypothesis.get("hypothesis","")
            st.markdown(hypothesis_text)

        except requests.exceptions.RequestException as e:
            st.error(f"API request failed: {e}")