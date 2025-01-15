import os
import requests
import zipfile
import config

if __name__ == "__main__":

    # Step 1 因vector store過於龐大，我先上傳到我私人one drive，再下載到本地
    def download_and_extract(url, save_path, extract_to):
        """Download from a direct OneDrive link (ending with ?download=1) and extract the ZIP."""
        session = requests.Session()
        # Send a fairly standard User-Agent
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                        ' AppleWebKit/537.36 (KHTML, like Gecko)'
                        ' Chrome/58.0.3029.110 Safari/537.3'
        }

        # If the ZIP doesn't exist locally, download it
        if not os.path.exists(save_path):
            print("Downloading the vector store...")
            try:
                response = session.get(url, headers=headers, stream=True, allow_redirects=True)
                
                # 200 means OK, could be the final file or a landing page
                if response.status_code == 200:
                    print(f"Final download URL: {response.url}")
                    with open(save_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                    print("Download completed!")
                else:
                    print(f"Error: Received status code {response.status_code} from OneDrive.")
                    return
            except Exception as e:
                print(f"Error during download: {e}")
                return

        # Extract the ZIP if not already extracted
        if not os.path.exists(extract_to):
            print("Extracting files...")
            with zipfile.ZipFile(save_path, 'r') as zip_ref:
                zip_ref.extractall(extract_to)
            print("Extraction completed!")

    # https://1drv.ms/u/c/679e347b4c35424f/EZwKtVQAWfhNhDCz8BVT_D8BKzUD5e80Q_uB8HfQ-Z62xg?e=PZIkfB
    # OneDrive 分享連結（修改為直接下載格式）
    # Replace this with your direct OneDrive link that forces a download:
    # 我花了一些時間才找到方法，要先下載然後暫停才能複製連結
    onedrive_direct_download_link = "https://my.microsoftpersonalcontent.com/personal/679e347b4c35424f/_layouts/15/download.aspx?UniqueId=79c40ed4-8c7e-4eda-94bc-8b1cfa5bedff&Translate=false&tempauth=v1e.eyJzaXRlaWQiOiIwOTM0OTdiYy0yMTAwLTQ2YjktODliOS01MGM3ZWMxNjA1ODciLCJhcHBpZCI6IjAwMDAwMDAwLTAwMDAtMDAwMC0wMDAwLTAwMDA0ODE3MTBhNCIsImF1ZCI6IjAwMDAwMDAzLTAwMDAtMGZmMS1jZTAwLTAwMDAwMDAwMDAwMC9teS5taWNyb3NvZnRwZXJzb25hbGNvbnRlbnQuY29tQDkxODgwNDBkLTZjNjctNGM1Yi1iMTEyLTM2YTMwNGI2NmRhZCIsImV4cCI6IjE3MzY4NDc4NjQifQ.CAlYctTc1QiAQaroYeV3V0FDybsyH6cyVemlp_OBgwT7ZLvRVsyOL0pZ2A8DVctlk8Q6kyjvI5I5V9FSPd5klJ9FRWNDap34uExTfP7s3YQS8UVClQ6vAR7ZQSHFXajIKdU1HkCQsDG9xV6eE0TotRFQj1r5kPV8kS2g5K-6GSmESrartLb4kxIgm3KE7uiA2z9CbgjpVwzAlO2cXUK-_FO-2uK9N2KPjO1SJ9O_wDNBznsAzr5wUQOvHnBcjoJbP5hY2aHIBZmnfeRNlRJuU9SvleBorlkFfsE1VueTYYGSqTxN2QqXYkZzBTInUXSZRtoWqxG7-KS7MKbm8mCL-j2MRPwhL5shvHGT-rtmC7g6wKnkAz_Pb5VUhZOfQrPseyp03A-X7nN53OxaJrNDZQ.7GI-xGbJ93Rsfl631jPD567JuAQhebfreg-bxNx7rN0&ApiVersion=2.0&AVOverride=1"


    # zip_path = "20250113_rag_1996_2024.zip"
    # extract_to_folder = "20250113_rag_1996_2024"

    zip_path = "/tmp/20250113_rag_1996_2024.zip"
    extract_to_folder = config.vector_db_path

    download_and_extract(onedrive_direct_download_link, zip_path, extract_to_folder)

    # Step 2
    os.system("streamlit run Step3_query_engine_as_server.py --server.port=8000 --server.address=0.0.0.0")