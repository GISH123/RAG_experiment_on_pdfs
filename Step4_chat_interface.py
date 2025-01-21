import time
import streamlit as st
import json
import os
from llama_index.core import StorageContext, load_index_from_storage
from use_openapi import use_openapi
import config
from datetime import datetime

CONVERSATIONS_FILE = "./tmp/conversations.json"

# -----------------------------
# Load/Save conversation data from disk
# -----------------------------
def load_conversations_from_file():
    """Load conversation data from local JSON, return as dict."""
    if os.path.exists(CONVERSATIONS_FILE):
        with open(CONVERSATIONS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {}

def save_conversations_to_file(conversations_data):
    """Save conversation data to local JSON."""
    with open(CONVERSATIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(conversations_data, f, ensure_ascii=False, indent=2)

# -----------------------------
# A helper function to name the chat automatically
# -----------------------------
def summarize_prompt_as_title(prompt: str, max_words: int = 5) -> str:
    """
    Generate a short conversation title from the first user prompt.
    e.g. "What is the future of AI in 2025?" -> "What is the future of..."
    """
    prompt = prompt.strip()
    if not prompt:
        return "Untitled Chat"

    words = prompt.split()
    short_title = " ".join(words[:max_words])
    if len(words) > max_words:
        short_title += "..."
    return short_title

# -----------------------------
# Caching: Load the index once
# -----------------------------
@st.cache_resource
def load_my_index(persist_dir):
    use_openapi()  # sets up your OPENAI_API_KEY, etc.
    storage_context = StorageContext.from_defaults(persist_dir=persist_dir)
    index = load_index_from_storage(storage_context)
    return index

def init_chat_engine(index):
    """
    Build a chat engine with memory. If as_chat_engine is unavailable in your
    LlamaIndex version, consult older docs or implement custom memory.
    """
    chat_engine = index.as_chat_engine(
        search_mode="hybrid",  # or "keyword"
        top_k=9999,
        # Additional conversation/memory parameters here
    )
    return chat_engine


# -----------------------------
# MAIN APP
# -----------------------------
def main():
    st.title("My RAG Chat App")

    # -----------------------------
    # 1) Load or initialize conversations from disk
    # -----------------------------
    if "conversations" not in st.session_state:
        # Load from JSON file
        st.session_state["conversations"] = load_conversations_from_file()

    # 2) Load the index if not done
    if "index" not in st.session_state:
        st.session_state["index"] = load_my_index(config.vector_db_path)

    # 3) Keep track of which conversation is selected
    if "selected_session" not in st.session_state:
        st.session_state["selected_session"] = None

    # -----------------------------
    # (Re)build the chat engine each run
    # We'll do it for each conversation on demand
    # -----------------------------
    # We'll store ephemeral chat engines in memory, but not in file.
    if "chat_engines" not in st.session_state:
        st.session_state["chat_engines"] = {}  # {convo_id: chat_engine}

    # -----------------------------
    # Ensure at least one conversation exists
    # -----------------------------
    if not st.session_state["conversations"]:
        # Create a brand new conversation
        convo_id = str(int(time.time()))  # simpler than UUID
        st.session_state["conversations"][convo_id] = {
            "title": "Untitled Chat",
            "messages": [],
            "last_updated": time.time(),
        }
        st.session_state["selected_session"] = convo_id
        save_conversations_to_file(st.session_state["conversations"])

    # If no session selected, pick the most recently updated
    if not st.session_state["selected_session"]:
        # Sort by most recent
        sorted_convos = sorted(
            st.session_state["conversations"].items(),
            key=lambda x: x[1].get("last_updated", 0),
            reverse=True
        )
        st.session_state["selected_session"] = sorted_convos[0][0]

    # -----------------------------
    # SIDEBAR: "New Chat" + list of convos
    # -----------------------------
    st.sidebar.header("Conversations")

    if st.sidebar.button("New Chat", key="new_chat"):
        new_id = str(int(time.time()))
        st.session_state["conversations"][new_id] = {
            "title": "Untitled Chat",
            "messages": [],
            "last_updated": time.time(),
        }
        st.session_state["selected_session"] = new_id
        save_conversations_to_file(st.session_state["conversations"])
        st.rerun()

    # Show all conversations in the sidebar, sorted by most recent first
    sorted_convos = sorted(
        st.session_state["conversations"].items(),
        key=lambda x: x[1].get("last_updated", 0),
        reverse=True
    )

    for convo_id, convo_data in sorted_convos:
        title = convo_data["title"]
        # If the user clicks on the conversation title, switch to it
        if st.sidebar.button(title, key=f"switch_{convo_id}"):
            st.session_state["selected_session"] = convo_id
            st.rerun()

    # -----------------------------
    # Active conversation
    # -----------------------------
    cur_session_id = st.session_state["selected_session"]
    cur_convo_data = st.session_state["conversations"][cur_session_id]
    messages = cur_convo_data["messages"]
    conversation_title = cur_convo_data["title"]

    # We might re-init the chat engine each time. If it doesn't exist in memory, create it.
    if cur_session_id not in st.session_state["chat_engines"]:
        st.session_state["chat_engines"][cur_session_id] = init_chat_engine(st.session_state["index"])
        # "Replay" all user messages so the engine has short-term memory
        # (Note: This can get expensive if there are many messages.)
        for role, text in messages:
            if role == "user":
                st.session_state["chat_engines"][cur_session_id].chat(text)

    chat_engine = st.session_state["chat_engines"][cur_session_id]

    # -----------------------------
    # Display existing conversation messages
    # -----------------------------
    for role, text in messages:
        with st.chat_message(role):
            st.write(text)

    # -----------------------------
    # Chat input
    # -----------------------------
    user_input = st.chat_input(placeholder="Ask something about the documents...")
    if user_input:
        # 1) Display user message
        messages.append(("user", user_input))
        with st.chat_message("user"):
            st.write(user_input)

        # 2) Possibly rename the conversation if it's still 'Untitled Chat'
        if conversation_title == "Untitled Chat":
            auto_title = summarize_prompt_as_title(user_input, max_words=5)
            cur_convo_data["title"] = auto_title
            conversation_title = auto_title  # update local var

        # 3) Query the chat engine
        start_time = time.time()
        response = chat_engine.chat(user_input)  # the short-term memory is inside chat_engine
        end_time = time.time()

        response_text = str(response) if response else "No response."

        # 4) Add the assistant response
        messages.append(("assistant", response_text))
        with st.chat_message("assistant"):
            st.write(response_text)
            st.caption(f"Query took {end_time - start_time:.2f}s")

        # 5) Update last_updated time
        cur_convo_data["last_updated"] = time.time()

    # -----------------------------
    # Persist changes
    # -----------------------------
    st.session_state["conversations"][cur_session_id]["messages"] = messages
    save_conversations_to_file(st.session_state["conversations"])


if __name__ == "__main__":
    main()