import time
from tqdm import tqdm
from llama_index.core import StorageContext, load_index_from_storage
from use_openapi import use_openapi
import streamlit as st
import config

st.write("✅ Step3_query_engine_as_server.py started!")  # Debug log

@st.cache_resource
def init_query_engine_with_4_bars(vector_db_path):
    """
    Initializes the query engine with 4 separate tqdm progress bars,
    each representing one step. Displayed in the server console.
    """

    # STEP 1: Setting up OpenAI environment
    progress1 = tqdm(range(1), desc="Step 1: Setting up environment", position=0, leave=True)
    for _ in progress1:
        use_openapi()  # your function that sets up OPENAI_API_KEY, etc.
        time.sleep(1)  # simulate a bit of work

    # STEP 2: Loading StorageContext
    progress2 = tqdm(range(1), desc="Step 2: Loading StorageContext", position=1, leave=True)
    for _ in progress2:
        storage_context = StorageContext.from_defaults(persist_dir=vector_db_path)
        time.sleep(1)  # simulate some I/O

    # STEP 3: Loading Index
    progress3 = tqdm(range(1), desc="Step 3: Loading index", position=2, leave=True)
    for _ in progress3:
        index = load_index_from_storage(storage_context)
        time.sleep(1)

    # STEP 4: Creating Query Engine
    progress4 = tqdm(range(1), desc="Step 4: Building query engine", position=3, leave=True)
    for _ in progress4:
        
        # 這邊可以調整query的方式，會影響準度
        
        # 法1 用top_k的方式去找出最相關的幾個chunk，限制:無法看到所有的文件
        # ===
        # query_engine = index.as_query_engine()

        # query_engine = index.as_query_engine(
        #     top_k=9999
        # )
        # ===

        # 法2 search_mode="hybrid"
        # ===
        query_engine = index.as_query_engine(
            search_mode="hybrid",  # or "keyword"
            top_k=9999
        )
        # ===

        time.sleep(1)

    st.info("Initialization complete!")
    return query_engine

def main():
    st.title("My RAG Q&A App")

    # If we haven't initialized the engine yet, do so now
    if "query_engine" not in st.session_state:
        st.session_state["query_engine"] = init_query_engine_with_4_bars(config.vector_db_path)

    # Ask a question
    user_query = st.text_input("Ask a question about the stored documents:")

    # Pressing "Submit" or hitting Enter
    if st.button("Submit") or (user_query and st.session_state.get("auto_submit", False)):
        # We measure how long the query takes
        start_time = time.time()

        # Retrieve query_engine from session_state
        query_engine = st.session_state["query_engine"]
        response = query_engine.query(user_query)

        end_time = time.time()

        # Display the answer and time taken
        st.write("**Answer:**", response)
        st.write(f"*(Query took {end_time - start_time:.2f} seconds.)*")

        # Optionally, store the Q&A in a chat history
        if "history" not in st.session_state:
            st.session_state["history"] = []
        st.session_state["history"].append((user_query, str(response)))

    # Display chat history below
    if "history" in st.session_state:
        st.write("---")
        st.write("### Conversation History")
        for i, (q, a) in enumerate(st.session_state["history"]):
            st.markdown(f"**Q{i+1}:** {q}")
            st.markdown(f"**A{i+1}:** {a}")
            st.write("---")

if __name__ == "__main__":
    main()