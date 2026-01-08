import streamlit as st
import sys
import os
from hybrid_search import SearchEngine, load_function_names

OTHER_DIR_PATH = os.path.abspath(".")
if OTHER_DIR_PATH not in sys.path:
    sys.path.append(OTHER_DIR_PATH)

st.set_page_config(page_title="Code Search")

# Remove caching temporarily
try:
    csv_location = os.path.join(OTHER_DIR_PATH, "raw_code.csv")
    functions = load_function_names(csv_location)
    engine = SearchEngine(functions)
    st.success("Search engine ready")
except Exception as e:
    st.error(f"Initialization failed: {e}")
    st.stop()

st.title("Code Search")
st.markdown("Search across the codebase using semantic embeddings (similarity ≥ 0.5).")

query = st.text_input("Enter search term", placeholder="Type your query here")

if query:
    st.divider()
    try:
        results = engine.semantic_search(query, threshold=0.5)
        if results:
            st.write(f"Found {len(results)} matches")
            for i, r in enumerate(results, 1):
                st.markdown(f"{i}. {r['name']} (similarity: {r['similarity']:.3f})")
        else:
            st.warning("No matches found")
    except Exception as e:
        st.error(f"Search failed: {e}")

with st.sidebar:
    st.header("Status")
    st.write(f"Functions indexed: {len(engine.function_names)}")
    st.info("Ensure 'raw_code.csv' exists in the same directory as hybrid_search.py")
