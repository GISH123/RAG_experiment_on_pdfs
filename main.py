import os
import requests
import zipfile
import config

if __name__ == "__main__":

    def download_and_extract(url, save_path, extract_to):
        """Download and extract a ZIP file with proper handling."""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                        ' AppleWebKit/537.36 (KHTML, like Gecko)'
                        ' Chrome/58.0.3029.110 Safari/537.3'
        }

        if not os.path.exists(save_path):
            print(f"📥 Downloading from: {url}")
            try:
                response = requests.get(url, headers=headers, stream=True)
                
                if response.status_code == 200:
                    with open(save_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                    print("✅ Download completed!")
                else:
                    print(f"❌ Error: Status code {response.status_code}")
                    return

            except Exception as e:
                print(f"❌ Error during download: {e}")
                return

        # Extract ZIP
        if zipfile.is_zipfile(save_path):
            print("📂 Extracting files...")
            with zipfile.ZipFile(save_path, 'r') as zip_ref:
                zip_ref.extractall(extract_to)
            print("✅ Extraction completed!")
        else:
            print("❌ Error: File is not a valid ZIP file.")


    # ✅ Updated Dropbox Direct Download Link
    download_link = "https://dl.dropboxusercontent.com/scl/fi/09cxtix1366lv29svejpo/20250113_rag_1996_2024.zip?rlkey=5uqs5qoipvg8b5y1r74wnu7lh&st=fmwx1vbj"

    # Paths
    zip_path = "tmp/20250113_rag_1996_2024.zip"
    extract_to_folder = config.vector_db_path

    # Start download and extraction
    download_and_extract(download_link, zip_path, extract_to_folder)

    # Step 3: Launch Streamlit server
    print("🚀 Starting Streamlit server...")

    # Get PORT from environment or default to 8000 because Vercel have its own dynamic port
    port = int(os.environ.get("PORT", 8000))

    # Run Streamlit on the correct port and address
    # os.system(f"streamlit run Step3_query_engine_as_server.py --server.port={port} --server.address=0.0.0.0")
    print("🚀 Ready! Streamlit Cloud will handle server startup.")