import pandas as pd
import os
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer

def run_topic_modeling():
    print("[INFO] Memulai Pemodelan Topik menggunakan BERTopic...")
    
    # Pengaturan direktori (Membaca file hasil skor sentimen VADER sebelumnya)
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    input_file = os.path.join(base_dir, "data", "processed", "reddit_sentiments_scored.csv")
    output_file = os.path.join(base_dir, "data", "processed", "reddit_topics_final.csv")
    
    if not os.path.exists(input_file):
        print(f"[ERROR] File input tidak ditemukan: {input_file}")
        return
        
    df = pd.read_csv(input_file)
    
    # Antisipasi nilai kosong (NaN) pada kolom BERTopic teks
    df['Text_BERTopic'] = df['Text_BERTopic'].fillna("")
    df = df[df['Text_BERTopic'].str.strip() != ""].reset_index(drop=True)
    
    print("[*] Memuat Arsitektur Embedding 'all-MiniLM-L6-v2'...")
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    
    print("[*] Melatih BERTopic pada 1.845 dokumen opini (Mengekstrak klaster UX)...")
    # Mengatur min_topic_size=15 agar klaster yang terbentuk berbobot dan tidak terlalu serpihan
    topic_model = BERTopic(embedding_model=embedding_model, min_topic_size=15)
    
    docs = df['Text_BERTopic'].tolist()
    topics, probs = topic_model.fit_transform(docs)
    
    # Memasukkan array hasil topik ke dalam DataFrame utama
    df['Topic_ID'] = topics
    
    # Mendapatkan detail nama representasi kata kunci tiap topik
    topic_info = topic_model.get_topic_info()
    
    # Map nama kata kunci topik ke dataframe utama agar mudah dibaca Joy
    topic_mapping = dict(zip(topic_info['Topic'], topic_info['Name']))
    df['Topic_Name'] = df['Topic_ID'].map(topic_mapping)
    
    # Menyimpan Dataset Final (Sudah punya teks bersih, skor sentimen, dan id topik)
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    df.to_csv(output_file, index=False, encoding='utf-8')
    print(f"[SUKSES] Dataset komprehensif berhasil dikunci di: {output_file}\n")
    
    # --- OUTPUT MATRIX UNTUK DIAGRAM / TABEL BAB 4 ---
    print("=== TOP 10 KLASTER TOPIK TERBESAR YANG DITEMUKAN ===")
    print(topic_info[['Topic', 'Count', 'Name']].head(11).to_string(index=False))
    
    print("\n=== MATRIKS KOMPARASI: TOPIK UX VS SUBREDDIT GAME ===")
    cross_tab = pd.crosstab(df['Topic_Name'], df['Subreddit'])
    print(cross_tab.to_string())

if __name__ == "__main__":
    run_topic_modeling()