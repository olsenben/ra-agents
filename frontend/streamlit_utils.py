import streamlit as st
import requests


def display_summaries(data: dict):
    """formats and displays summary data from results"""
    #display summarized papers
    for idx, paper in enumerate(data['papers'], 1):
        with st.expander(f"**{idx}. {paper['title']}**"):
            authors_str = " ,".join(paper.get('authors',[])) or "Unknown authors"
            st.markdown(f"**Authors:** {authors_str}")
            st.markdown(f"**URL:** [{paper['url']}]({paper['url']})")
            #st.markdown(f"**Summary:**")
            st.markdown(f"{paper['summary']}")

def display_clusters(data: dict):
    """formats and displays cluster data"""
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

def display_hypothesis(data: dict):
    """formats and displays hypothesis"""

    st.header("Suggested Follow-up Hypothesis")
    hypothesis = data.get('follow_up_hypothesis',{})
    hypothesis_text = hypothesis.get("hypothesis","")
    st.markdown(hypothesis_text)

def fetch_history(url, headers, limit=10):

    if not isinstance(headers, dict):
        raise ValueError("Expected headers to be dictionary, got", type(headers))
    
    history = requests.get(
                f'{url}'+'/results', 
                headers = headers,
                params={
                    "limit" : limit
                    },
                )
    history.raise_for_status()
    runs = history.json()
    return runs

def fetch_data(query, url, headers, limit=10):
    """
    runs query pipeline
    """
    if not isinstance(headers, dict):
        raise ValueError("Expected headers to be dictionary, got", type(headers))

    response = requests.get(
                f'{url}'+'/analyze', 
                headers = headers,
                params={
                    "query" : query,
                    "limit" : limit
                    }
                )
            
    response.raise_for_status()
    data = response.json()
    return data

def display_data(data:dict):
    """
    format and display all fetched data 
    """

    st.header(f"Found Papers: {len(data['papers'])}")

    #display summarized papers
    display_summaries(data)

    st.success(f"Found {len(data['clusters']['clusters'])} Thematic Clusters...")
    
    #display clusters
    display_clusters(data)

    #display hypothesis
    display_hypothesis(data)

def update_sidebar(API_URL, headers, limit=20):
    #load history
    runs = fetch_history(API_URL, headers, limit)

    #use sidebar to display previous queries
    with st.sidebar:
        st.header("Previous Queries")
        query_options = [f"{run['query']}" for run in runs]
        options = [""] + query_options
        selected_query = st.selectbox(
            "Choose Previous",
            options=options,
            index=0 if runs else None,
        )

    if selected_query:
        st.session_state["selected_query"] = selected_query


    #find matching result for selected query
    # if  selected_query and runs: 
    #     selected_run = next(run for run in runs if f"{run['query']}" == selected_query)
    #     display_data(selected_run)
    # else:
    #     st.write("Analyze or select a previous query from the sidebar.")

    # if selected_query != "":
    #     delete_button = st.button("Delete this entry")

    #     if delete_button:
    #         response = requests.delete(f"{API_URL}/delete/{selected_run['_id']}")
    #         if response.status_code == 200:
    #             st.success("Entry deleted successfully")
    #         else:
    #             st.error("Failed to delete entry")
    

