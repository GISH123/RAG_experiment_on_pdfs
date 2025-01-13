from llama_index.core import StorageContext, load_index_from_storage
from use_openapi import use_openapi

# use open_api
use_openapi()

# 1) Create a storage context pointing to the persist directory
storage_context = StorageContext.from_defaults(persist_dir="20250113_rag_1996_2024")

# 2) Load the index from storage (no re-embedding needed!)
index = load_index_from_storage(storage_context)

# =========新增 檢查index的chunk=========
docstore = storage_context.docstore

# Iterate over stored documents (or "nodes"), printing their text
for docstore_id in docstore.docs.keys(): #
    doc = docstore.docs[docstore_id] 

    if "CB202401" in doc.ref_doc_id:

        text = getattr(doc, 'text', None)
        if text is None:
            # If doc.text doesn't exist, try doc.get_text() or doc.get_content()
            if hasattr(doc, 'get_text'):
                text = doc.get_text()
            elif hasattr(doc, 'get_content'):
                text = doc.get_content()
            else:
                text = "No text attribute found."

        print(f"=== Document/Chunk ID: {doc.ref_doc_id}, docstore_id: {docstore_id} ===")
        print(text[:50])  # Print just the first 100 characters
        print("=================================\n")