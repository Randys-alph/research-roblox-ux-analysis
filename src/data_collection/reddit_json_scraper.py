import pandas as pd
from datetime import datetime
import os
import json
import glob

def process_bulk_local_json():
    print("[INFO] Membaca seluruh pecahan file JSON Reddit lokal...")
    
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    raw_dir = os.path.join(base_dir, "data", "raw")
    
    # Mencari semua file json dengan awalan blox_ dan bee_
    json_files = glob.glob(os.path.join(raw_dir, "blox_*.json")) + \
                 glob.glob(os.path.join(raw_dir, "bee_*.json"))
                 
    all_extracted_data = []
    
    for file_path in json_files:
        filename = os.path.basename(file_path)
        
        # Menentukan label subreddit berdasarkan nama awalan file
        if filename.startswith("blox_"):
            sub = "bloxfruits"
        elif filename.startswith("bee_"):
            sub = "BeeSwarmSimulator"
        else:
            continue
            
        print(f"[*] Memproses file: {filename}...")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data_json = json.load(f)
                
            children = data_json.get("data", {}).get("children", [])
            
            for post in children:
                post_data = post.get("data", {})
                
                title = post_data.get("title", "")
                selftext = post_data.get("selftext", "")
                raw_text = f"{title}. {selftext}".strip()
                
                # Filter kualitatif: Abaikan post tanpa teks opini yang memadai
                if len(raw_text) < 10:
                    continue
                
                created_utc = post_data.get("created_utc")
                timestamp = datetime.fromtimestamp(created_utc).strftime("%Y-%m-%d %H:%M:%S") if created_utc else None
                
                all_extracted_data.append({
                    "Timestamp": timestamp,
                    "Subreddit": sub,
                    "Post_Title": title,
                    "Post_Content": selftext,
                    "Upvotes": post_data.get("score", 0),
                    "Total_Comments": post_data.get("num_comments", 0),
                    "Raw_Text_For_NLP": raw_text
                })
                
        except Exception as e:
            print(f"[ERROR] Gagal memproses {filename}: {e}")
            
    # Konversi ke DataFrame dan bersihkan data ganda
    df = pd.DataFrame(all_extracted_data)
    
    if not df.empty:
        df.drop_duplicates(subset=['Post_Title', 'Post_Content'], inplace=True)
        print(f"\n[INFO] Total baris data unik berhasil dileburkan: {len(df)}")
        
    return df

if __name__ == "__main__":
    df_reddit = process_bulk_local_json()
    
    if df_reddit is not None and not df_reddit.empty:
        print("\n[PREVIEW DATA REDDIT NLP]")
        print(df_reddit[['Subreddit', 'Upvotes', 'Raw_Text_For_NLP']].head().to_string(index=False))
        
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        output_file = os.path.join(base_dir, "data", "raw", "reddit_opinions_raw.csv")
        
        df_reddit.to_csv(output_file, index=False, encoding='utf-8')
        print(f"\n[SUKSES] Kemenangan arsitektural! Data CSV siap digunakan di: {output_file}")
    else:
        print("\n[GAGAL] Tidak ada data yang diekstrak. Pastikan file json sudah ada di folder data/raw/.")