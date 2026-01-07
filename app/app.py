import streamlit as st
import sys
import os

OTHER_DIR_PATH = os.path.abspath(".")
if OTHER_DIR_PATH not in sys.path:
    sys.path.append(OTHER_DIR_PATH)

from hybrid_search import SearchEngine, load_function_names  # import your updated file

st.set_page_config(page_title="Code Search")

@st.cache_resource
def get_engine():
    csv_location = os.path.join(OTHER_DIR_PATH, "raw_code.csv")
    functions = load_function_names(csv_location)
    return SearchEngine(functions)

st.title("Code Search")
st.markdown("Search across the codebase using semantic embeddings (similarity ≥ 0.5).")

with st.spinner("Initializing search engine..."):
    try:
        engine = get_engine()
        st.success("Ready")
    except Exception as e:
        st.error(f"Initialization failed: {e}")
        st.stop()

query = st.text_input("Enter search term", placeholder="Type your query here")

if query:
    st.divider()
    results = engine.semantic_search(query, threshold=0.5)
    
    if results:
        st.write(f"Found {len(results)} matches")
        for i, r in enumerate(results, 1):
            st.markdown(f"{i}. {r['name']} (similarity: {r['similarity']:.3f})")
    else:
        st.warning("No matches found")

with st.sidebar:
    st.header("Status")
    st.write(f"Functions indexed: {len(engine.function_names)}")
    st.info("Ensure 'raw_code.csv' exists in the same directory as hybrid_search.py")
