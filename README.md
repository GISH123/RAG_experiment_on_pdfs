https://gamma.app/docs/LlamaIndex-RAG--rix0jnlnfuepdr5?mode=doc

中經院內部文件檔案RAG專案實驗 - Chat UI 加強版  
此版用的是自行將8本全球經濟展望專書(每個文檔至少200頁以上)用open ai embed到vectordb的版本，即，local自建db版  
因RAG與成本的限制，每次prompt只會找出最相關的top 2文件做回答，所以一次要問八個書的資訊是不太可能(當然，如果code裡面硬性要求找出所有問件，除了時間成本，cost也會提高許多)  
這邊使用的是我去註冊的open api key，每次prompt都會花少量的錢，就不特別調整模型準度的部分了  
https://ragonmyvectordb.streamlit.app/  
因streamlit是deploy在網路上 用的是他們的server 速度會比local自己建還慢一點 每按一個動作都要等一點延遲  

=============================================================================================================================

2025/01/20 RAG chat UI 加強  

以下為claude 3.5 sonnet 製造出的readme:  

# RAG-Powered Economic Research Assistant

A Retrieval-Augmented Generation (RAG) chatbot that analyzes economic outlook reports, built with LlamaIndex and OpenAI.

## Project Overview

This project demonstrates the practical application of RAG technology to analyze complex economic documents. It currently processes 8 comprehensive global economic outlook reports (200+ pages each) to provide intelligent responses to economic queries.

### Key Features

- **Document Processing**: Custom PDF processing pipeline with PyMuPDF for accurate text extraction
- **Advanced RAG Implementation**: Hybrid search mode combining semantic and keyword search for improved accuracy
- **Conversational Memory**: Maintains chat history for contextual responses
- **Streamlit Web Interface**: User-friendly chat interface with conversation management
- **Automated Document Naming**: Smart conversation title generation based on initial queries

### Technical Stack

- **Framework**: LlamaIndex for RAG implementation
- **LLM**: OpenAI GPT-3.5/4 for response generation
- **Embeddings**: OpenAI text embeddings
- **Frontend**: Streamlit
- **Document Processing**: PyMuPDF, custom chunking with sentence splitting
- **Storage**: Local vector storage with persistence

## Live Demo

Try the application at: [https://ragonmyvectordb.streamlit.app/](https://ragonmyvectordb.streamlit.app/)  

![Chat Interface Screenshot](image.png)

## Example Queries

The system can handle various economic queries. Some examples:

1. **Policy Analysis**:
   ```
   Q: "請告訴我 五加二的創新產業"
   A: 五加二創新產業包括綠能、國防、生技醫療、亞洲矽谷、智慧機械、新農業和循環經濟。
   ```

2. **Economic Concepts**:
   ```
   Q: "請告訴我 新型舉國體制 的意義"
   A: 新型舉國體制的意義在於探索建立適合中國大陸科技創新的制度安排，尋求更有效的組織方法來應對當前和未來的挑戰和發展環境。
   ```

## Technical Implementation Details

- Custom document chunking strategy (512 tokens with 20-token overlap)
- Hybrid search implementation for optimal retrieval
- Persistent storage management for efficient data handling
- Automated ZIP file handling for document updates

## Future Enhancements

- Integration with more economic data sources
- Multi-language support enhancement
- Advanced analytics dashboard
- Real-time economic data integration

## Skills Demonstrated

- Large Language Model (LLM) Integration
- Vector Database Implementation
- RAG System Architecture
- Python Development
- Web Application Development
- Document Processing
- API Integration
- Data Engineering

## Contact

Feel free to connect with me on [LinkedIn](https://www.linkedin.com/in/gish-shao-196aab134/) for discussions about this project or AI/ML opportunities.
