from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings, Document
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.node_parser import SentenceSplitter
from use_openapi import use_openapi
from collections import defaultdict
from llama_index.readers.file import PyMuPDFReader

import os

# use open_api
use_openapi()

def load_and_chunk_pdfs_with_custom_ids(folder_path):
    all_docs = SimpleDirectoryReader(
        input_dir=folder_path,
        required_exts=[".pdf"],
        recursive=True,
        filename_as_id=True,
        encoding="utf-8",
        file_extractor={
            ".pdf": PyMuPDFReader()
        }
    ).load_data()
    # all_docs might have multiple Document objects per PDF
    # e.g., a 40-page PDF could be returned as 40 separate Documents

    def combine_pages_into_single_doc(page_docs):
        """
        Combine multiple 'page-level' Documents from a single PDF
        into one big Document representing the entire PDF.
        """
        if not page_docs:
            return None

        # 1) Extract the file_path from the first doc (assuming all share same PDF)
        file_path = page_docs[0].metadata.get("file_path", "unknown.pdf")
        filename = os.path.basename(file_path)

        # 2) Combine all page texts
        full_text = "\n".join(doc.text for doc in page_docs if doc.text)

        # 3) Create a single Document
        combined_doc = Document(
            text=full_text,
            doc_id=filename,  # or some custom ID
            metadata={"filename": filename}
        )
        return combined_doc

    # 1) Group each PDF's pages in a dictionary
    pdf_groups = defaultdict(list)
    for d in all_docs: # all docs(list) have page-level Documents, for example 40 pages = 40 Documents
        path = d.metadata.get("file_path", None)
        pdf_groups[path].append(d)
    # pdf_groups = { 'C:\\Users\\Gish.AI\\Desktop\\rag實驗\\test\\CA0055.pdf': [Document(id_='3dca6a85-440b-4577-a4a8-2ab6210920f7', .......] }


    # 2) Build one Document per PDF
    merged_docs = []
    for path, page_docs in pdf_groups.items():
        merged = combine_pages_into_single_doc(page_docs)
        if merged: 
            merged_docs.append(merged) 

    splitter = SentenceSplitter(chunk_size=512, chunk_overlap=20)
    all_chunked_docs = []

    for doc in merged_docs:
        # doc.text is the entire PDF's text
        chunks = splitter.split_text(doc.text)
        for i, chunk_text in enumerate(chunks):
            chunked_docs = Document(
                text=chunk_text,
                doc_id=f"{doc.doc_id}-chunk{i}",
                metadata={"filename": doc.metadata["filename"],
                        #   "my_doc_id": f"{doc.doc_id}-chunk{i}"
                          }
            )
            all_chunked_docs.append(chunked_docs)

    return all_chunked_docs


folder_path = "./rag_experiment/1996-2024年全球經濟展望專書)(29本)(8本)"
# folder_path = "./rag_experiment/1996-2024年全球經濟展望專書)(29本)(8本)"

# Load documents, customizing doc_id with filename
chunked_docs = load_and_chunk_pdfs_with_custom_ids(folder_path)

# test seeing chunked_docs have correct doc_id
# for i in chunked_docs:
#     print(i.doc_id)
# 40 pages into 32 chunks, the chunk boundaries do not align one-to-one with pages

# Build your index
index = VectorStoreIndex.from_documents(chunked_docs)

# Persist
index.storage_context.persist(persist_dir="20250113_rag_1996_2024")



