import streamlit as st
import requests

API_URL = "http://localhost:8000/analyze"

st.title("Multi-Agent Research Assistant")

query = st.text_input("Enter a research topic", "glioblastoma")
limit = st.slider("Number of papers to analyze", 1,20,5)

if st.button("Analyze"):
    with st.spinner("Running multi-agent pipeline..."):
        try:
            response = requests.get(API_URL, params={"query" : query, "limit" : limit})
            response.raise_for_status()
            data = response.json()

            #display summarized papers
            for idx, paper in enumerate(data['papers'], 1):
                with st.expander(f"**{idx}. {paper['title']}**"):
                    authors_str = ",".join(paper.get('authors',[])) or "Unknown authors"
                    st.markdown(f"**Authors:** {authors_str}")
                    st.markdown(f"**URL:** [{paper['url']}]({paper['url']})")
                    st.markdown(f"**Summary:** {paper['summary']}")

            st.success(f"Found {len(data['clusters'])} Thematic Clusters...")

            #display clusters 
            for idx, cluster in enumerate(data['clusters']['clusters'], 1):
                st.subheader(f"Cluster: {idx}")
                st.markdown(cluster['theme'])    
                st.markdown(cluster['summary'])

            st.subheader("Contradicitons or Gaps")   
            contradictions = data['clusters'].get('contradictions', 'No Contradicitons Found')
            if contradictions: 
                st.write(contradictions)

            #display hypothesis
            st.subheader("Suggested Follow-up Hypothesis")
            hypothesis = data['follow_up_hypothesis']
            st.write(hypothesis)

        except requests.exceptions.RequestException as e:
            st.error(f"API request failed: {e}")