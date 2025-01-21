import os
import requests
import zipfile
import config
import streamlit as st  # Import Streamlit for UI logging
import Step3_chat_interface

st.write("✅ main.py started!")  # Debug log

if __name__ == "__main__":
    # Ensure the /tmp directory exists
    os.makedirs('./tmp', exist_ok=True)  # Create the tmp directory if it doesn't exist

    # Step 3: Launch Streamlit server (handled by Streamlit Cloud)
    st.info("🚀 Ready! Streamlit Cloud will handle server startup.")
    Step3_chat_interface.main()