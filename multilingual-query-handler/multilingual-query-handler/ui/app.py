import streamlit as st
import sys
import os

# Most robust path fix for Streamlit apps running from the project root (via PYTHONPATH=.)
# This ensures Python can find modules inside the 'src' directory.
# We append the 'src' directory relative to the current working directory (which is the root).
if 'src' not in sys.path:
    # This path assumes you run the app from the parent directory of 'ui'
    sys.path.append(os.path.join(os.getcwd(), 'src'))


# Import application modules
from query_engine import QueryEngine
from embeddings import VectorStoreManager # Note: VectorStoreManager is imported but not used directly in the UI


# Page config
st.set_page_config(
    page_title="Multilingual Query Handler",
    page_icon="🌍",
    layout="wide"
)

# --- Initialization ---

# Initialize session state for QueryEngine (Knowledge Base connection)
if 'query_engine' not in st.session_state:
    st.session_state.query_engine = QueryEngine()
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# --- UI Layout ---

# Title
st.title("🌍 Real-Time Multilingual Query Handler")
st.markdown("Ask questions in any language - we'll translate and answer!")

# Sidebar
with st.sidebar:
    st.header("Settings")
    
    # Language selection dropdown
    language = st.selectbox(
        "Input Language",
        ["Auto-detect", "English", "Spanish", "French", "German", "Chinese", "Hindi", "Arabic"]
    )
    
    st.markdown("---")
    
    st.markdown("### About")
    st.info("This system translates your queries to English, searches our knowledge base, and provides accurate answers.")
    
    # Optional: Display the path for debugging (helpful for confirming context)
    # st.markdown(f"Current Working Dir: `{os.getcwd()}`")
    # st.markdown(f"Sys Path: `{sys.path}`")

# Main chat interface
user_input = st.text_input("Enter your question:", placeholder="Type your question in any language...")

if st.button("Submit", use_container_width=True) and user_input:
    with st.spinner("Processing your query..."):
        # Process query
        result = st.session_state.query_engine.process_query(
            user_input,
            language if language != "Auto-detect" else "auto"
        )
        
        # Add to history
        st.session_state.chat_history.append({
            "query": user_input,
            "result": result
        })
        
        # Display results
        st.success("✅ Query processed successfully!")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Query Information")
            st.write(f"**Detected Language:** {result['detected_language']}")
            st.write(f"**Original Query:** {result['original_query']}")
            if result['translated_query'] != result['original_query']:
                st.write(f"**Translated Query:** {result['translated_query']}")
        
        with col2:
            st.subheader("Answer")
            st.write(result['answer'])
        
        # Show sources
        with st.expander("View Sources"):
            for i, source in enumerate(result['sources'], 1):
                st.markdown(f"**Source {i}:** {source}")

# Display chat history
if st.session_state.chat_history:
    st.markdown("---")
    st.subheader("Chat History")
    # Display last 5 questions
    for i, chat in enumerate(reversed(st.session_state.chat_history[-5:]), 1):
        with st.expander(f"Q{i}: {chat['query'][:50]}..."):
            st.markdown(f"**Answer:** {chat['result']['answer']}")