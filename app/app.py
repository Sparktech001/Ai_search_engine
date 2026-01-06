import streamlit as st
import sys
import os

OTHER_DIR_PATH = os.path.abspath(".")


if OTHER_DIR_PATH not in sys.path:
    sys.path.append(OTHER_DIR_PATH)

from hybrid_search import SearchEngine, load_function_names

st.set_page_config(page_title="Code Search")

@st.cache_resource
def get_engine():
    csv_location = os.path.join(OTHER_DIR_PATH, "raw_code.csv")
    functions = load_function_names(csv_location)
    return SearchEngine(functions)

st.title("Code Search")
st.markdown("Search across the codebase using prefix and semantic matching.")

with st.spinner("Initializing search engine..."):
    try:
        engine = get_engine()
        st.success("Ready")
    except Exception as e:
        st.error(f"Initialization failed: {e}")
        st.stop()

query = st.text_input("Enter search term", placeholder="enter to search ")

if query:
    st.divider()
    results = engine.search(query)
    
    if results:
        st.write(f"Found {len(results)} matches")
        
        for i, res in enumerate(results, 1):
            if res.startswith(query):
                label = "Prefix match"
                color = "blue"
            else:
                label = "Semantic match"
                color = "orange"
                
            st.markdown(f"{i}. {res} :{color}[({label})]")
    else:
        st.warning("No matches found")

with st.sidebar:
    st.header("Status")
    st.write(f"Functions indexed: {len(engine.function_names)}")
    st.info("Ensure 'raw_code.csv' is available in the expected directory")
