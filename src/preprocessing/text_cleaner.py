import pandas as pd
import re
import string
import os
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Mengunduh dependensi bahasa NLTK secara otomatis
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)

def clean_for_vader(text):
    """
    JALUR 1 (VADER): Pembersihan ringan. 
    Menghapus link dan tag HTML, tetapi MEMPERTAHANKAN huruf kapital dan tanda baca.
    """
    if not isinstance(text, str):
        return ""
    # Hapus URL
    text = re.sub(r'http\S+|www\.\S+', '', text)
    # Hapus tag HTML
    text = re.sub(r'<.*?>', '', text)
    # Hapus karakter non-ASCII (seperti emoji aneh yang tidak terbaca VADER)
    text = text.encode('ascii', 'ignore').decode('utf-8')
    return text.strip()

def clean_for_bertopic(text, lemmatizer, stop_words):
    """
    JALUR 2 (BERTopic): Pembersihan dalam (Deep Cleaning).
    Huruf kecil semua, tanpa tanda baca, tanpa stopwords, dan dilematisasi.
    """
    if not isinstance(text, str):
        return ""
    
    # 1. Lowercase & hapus URL
    text = text.lower()
    text = re.sub(r'http\S+|www\.\S+', '', text)
    
    # 2. Hapus tanda baca dan angka
    text = re.sub(r'[%s]' % re.escape(string.punctuation), ' ', text)
    text = re.sub(r'\d+', '', text)
    
    # 3. Tokenisasi sederhana (pecah jadi kata-kata)
    words = text.split()
    
    # 4. Hapus Stopwords & Lemmatization
    cleaned_words = [
        lemmatizer.lemmatize(word) 
        for word in words 
        if word not in stop_words and len(word) > 2  # Abaikan kata super pendek seperti 'ah', 'ok'
    ]
    
    return ' '.join(cleaned_words)

def process_dual_stream():
    print("[INFO] Memulai Dual-Stream Preprocessing pada data opini Reddit...")
    
    # Pengaturan direktori
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    input_file = os.path.join(base_dir, "data", "raw", "reddit_opinions_raw.csv")
    output_file = os.path.join(base_dir, "data", "processed", "reddit_opinions_cleaned.csv")
    
    # Pastikan folder processed ada
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"[ERROR] File mentah tidak ditemukan di: {input_file}")
        return
        
    # Inisialisasi alat NLP
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    
    # Menambahkan Stopwords khusus Roblox/Gaming agar BERTopic tidak fokus ke kata yang tidak penting
    custom_stopwords = {'game', 'play', 'roblox', 'bloxfruit', 'blox', 'fruit', 'bee', 'swarm', 'simulator'}
    stop_words = stop_words.union(custom_stopwords)
    
    print("[*] Mengeksekusi Jalur 1: VADER (Mempertahankan intensitas sentimen)...")
    df['Text_VADER'] = df['Raw_Text_For_NLP'].apply(clean_for_vader)
    
    print("[*] Mengeksekusi Jalur 2: BERTopic (Lemmatization & Stopword removal)...")
    df['Text_BERTopic'] = df['Raw_Text_For_NLP'].apply(lambda x: clean_for_bertopic(x, lemmatizer, stop_words))
    
    # Menyimpan hasil akhir
    df.to_csv(output_file, index=False, encoding='utf-8')
    
    print(f"\n[SUKSES] Data berhasil diproses!")
    print(f"Total baris yang selamat: {len(df)}")
    print(f"File tersimpan di: {output_file}")
    
    print("\n[PREVIEW HASIL DUAL-STREAM]")
    preview_df = df[['Raw_Text_For_NLP', 'Text_VADER', 'Text_BERTopic']].head(2)
    for index, row in preview_df.iterrows():
        print(f"\n--- Sampel {index + 1} ---")
        print(f"RAW       : {row['Raw_Text_For_NLP'][:100]}...")
        print(f"VADER     : {row['Text_VADER'][:100]}...")
        print(f"BERTopic  : {row['Text_BERTopic'][:100]}...")

if __name__ == "__main__":
    process_dual_stream()