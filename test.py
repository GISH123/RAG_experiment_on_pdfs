from astrapy import DataAPIClient
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.vector_stores.astra_db import AstraDBVectorStore
import getpass
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
)
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

api_endpoint = os.getenv('api_endpoint')
print(api_endpoint)
    # "\nPlease enter your Database Endpoint URL "

token = os.getenv('token')
print(token)
    # "\nPlease enter your 'Database Administrator' Token"

astra_db_store = AstraDBVectorStore(
    token=token,
    api_endpoint=api_endpoint,
    collection_name="cier2_collection",  # Existing collection
    embedding_dimension=1536
)

embed_model = OpenAIEmbedding(model_name="text-embedding-3-small")

storage_context = StorageContext.from_defaults(vector_store=astra_db_store)

# ⚠️ FIX: Load index from vector store instead of from_documents
index = VectorStoreIndex.from_vector_store(
    vector_store=astra_db_store,
    storage_context=storage_context,
    embed_model=embed_model
)

# print("Question 1 ==========================================")
# query_engine = index.as_query_engine()
# query = """ 請問這些文件的重點是什麼 """
# print("Question 1: ", query)
# response = query_engine.query(query)
# print(response.response)
# print("=====================================================")

# # by astraDB : 這些文件的重點主要涵蓋了計畫工作查核重點說明、APEC 時程概況、APEC 全體經濟體占全球比率、APEC 主題暨優先事項、APEC 2023 年主辦國—美國主題暨優先事項、APEC 2023 年主辦國—美國會議行事曆、化學對話概況、歷屆化學對話會議地點、APEC 暨化學對話會議重要資訊來源、規劃翻譯之三份文件等內容。對於第二份文件，重點在於計畫目標、實施方法、資料架構、使用者介面、資通安全、結論及後續規劃等方面。  

# # chatgpt(無痕網頁):
# # Prompt : 請問這些文件的重點是什麼
# # ChatGPT 說：
# # ChatGPT
# # 請上傳文件或提供具體的內容，這樣我可以幫助你總結出重點。

# print("Question 2 ==========================================")
# query_engine = index.as_query_engine()
# query = """ 請問何年成立WTO中心 """
# print("Question 2: ", query)
# response = query_engine.query(query)
# print(response.response)
# print("=====================================================")

# # by astraDB : WTO中心成立於2001年。

# # chatgpt(無痕網頁):
# # Prompt : 請問何年成立WTO中心
# # ChatGPT 說：
# # ChatGPT
# # 世界貿易組織（WTO，World Trade Organization）的總部位於瑞士日內瓦，成立於 1995年。WTO的設立是基於對原來的「關稅暨貿易總協定」（GATT）的繼承與擴展，旨在促進國際貿易的自由化和規範。



# print("Question 3 ==========================================")
# query_engine = index.as_query_engine()
# query = """請回答 AI對勞動市場的影響"""
# print("Question 3: ", query)
# response = query_engine.query(query)
# print(response.response)
# print("=====================================================")

# by astraDB : 
# AI對勞動市場的影響包括可能導致部分工作被取代，例如電話銷售員、客服、倉庫工人等高度重複性工作容易受到影響。同時，AI也可能創造新的就業機會，例如需要開發和部署新興前瞻技術的人。因此，AI對勞動
# 市場的影響是一個複雜的議題，需要平衡取代性和創造性的影響。

# 用我的vector db 回答 得到的結果
# Q2: 請回答 AI對勞動市場的影響

# A2: AI對勞動市場的影響可能在短期內產生負面影響，但長期來看有助於提高生產力。AI有望幫助人類節省更多勞力，尤其是在知識型工作領域，同時創造更多就業機會。此外，AI也可以與現有的勞動力互補，提高整體生產力。雖然AI的影響尚不明確，但一些國家已經開始投入相關資源，將AI應用於就業服務領域，例如尋職、就業媒合和資訊提供等方面。

# chatgpt(無痕網頁):
# AI對勞動市場的影響是深遠且多面的，主要表現在以下幾個方面：

# 工作類型的變化： AI技術的應用，特別是在自動化、機器學習和自然語言處理等領域，正在替代一些重複性、高度標準化的工作，例如製造業中的生產線工人、客服代表、資料處理員等。此外，AI還能在一些複雜的領域中提供協助，如醫療診斷、法律分析等，這可能使一些傳統職位變得不再必要，並催生出新的職位。

# 技能需求的轉變： 隨著AI技術的普及，對勞動力的技能需求也發生了變化。未來的工作將更多依賴於高級技能，如編程、數據分析、AI模型訓練和維護、數位轉型等。這意味著，勞動市場需要加強對技術技能的培訓，並提高勞動者的數位素養。

# 勞動市場的不平等問題： AI的快速發展可能會加劇勞動市場的不平等。一方面，高技能工作者（如數據科學家、工程師等）將受益於技術進步，並能享有更高薪資；另一方面，低技能或受自動化影響的勞動者可能面臨失業或低薪困境，導致貧富差距的擴大。

# 創新和新職位的出現： 雖然AI可能會取代一些現有的工作，但它也有潛力創造出許多新職位。例如，在AI開發、維護、監管、倫理等方面將出現新的工作機會。此外，AI能夠提高工作效率和創造力，從而促進新興行業的發展，例如人工智慧顧問、AI倫理學家、數據保護專家等新興職位。

# 遠程工作和靈活工作的增長： AI的普及促進了遠程工作和靈活工作的發展。許多工作不再需要固定的地理位置，AI工具使員工可以更有效地協作和完成任務，這為勞動市場提供了更多彈性，也改變了企業對工作場所的需求。

# 勞動市場的全球化： AI和自動化技術降低了跨國合作的門檻，讓企業能夠聘用來自世界各地的優秀人才。這一點促使勞動市場不僅是本地或國內市場，更變成了全球競爭的場域。

# 總的來說，AI對勞動市場的影響既有正面，也有負面。面對這一變革，政策制定者、企業和教育機構應加強協作，提供適應未來工作的培訓，並確保在AI帶來的變革中能夠實現社會的包容性和公平性。


print("Question 4 ==========================================")
query_engine = index.as_query_engine()
query = """請問這些文件的出版者是誰"""
print("Question 4: ", query)
response = query_engine.query(query)
print(response.response)
print("=====================================================")

# by astraDB : The publisher of these documents is "經濟前瞻" (Economic Outlook).


# 用我的vector db 回答 得到的結果
# Q5: 請問這些文件的出版者是誰

# A5: 中經院出版社

# chatgpt(無痕網頁):
# 請問這些文件的出版者是誰
# ChatGPT 說：
# ChatGPT
# 請上傳文件，我會幫您查看出版者是誰。














# print("Question 1 ==========================================")
# query_engine = index.as_query_engine()
# query = """用 1000字繁體中文簡述 "Determinants of Highly-Skilled Migration –
# Taiwan’s Experiences" 的內容, 不知道就說不知道 """
# print("Question 1: ", query)
# response = query_engine.query(query)
# print(response.response)
# print("=====================================================")

# print("Question 2 ==========================================")
# query_engine = index.as_query_engine()
# query = """請翻譯 "Determinants of Highly-Skilled Migration – Taiwan's Experiences""" 
# print("Question 2: ", query)
# response = query_engine.query(query)
# print(response.response)
# print("=====================================================")

# print("Question 3 ==========================================")
# query_engine = index.as_query_engine()
# query = """用 1000字繁體中文簡述 "高技能移民的決定因素" , 不知道就說不知道"""
# print("Question 3: ", query)
# response = query_engine.query(query)
# print(response.response)
# print("=====================================================")

# print("Question 4 ==========================================")
# query_engine = index.as_query_engine()
# query = """用 1000字繁體中文簡述, 從台灣經驗中, 高技能移民的決定因素, 不知道就說不知道"""
# print("Question 4: ", query)
# response = query_engine.query(query)
# print(response.response)
# print("=====================================================")




