import pandas as pd
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def analyze_sentiment():
    print("[INFO] Memulai proses Analisis Sentimen VADER...")
    
    # Pengaturan direktori (membaca file hasil pembersihan tadi)
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    input_file = os.path.join(base_dir, "data", "processed", "reddit_opinions_cleaned.csv")
    output_file = os.path.join(base_dir, "data", "processed", "reddit_sentiments_scored.csv")
    
    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"[ERROR] File input tidak ditemukan: {input_file}")
        return

    # Inisialisasi Analyzer VADER
    analyzer = SentimentIntensityAnalyzer()

    # Fungsi internal untuk menghitung dan mengklasifikasikan
    def get_sentiment(text):
        if not isinstance(text, str):
            return 0.0, "Neutral"
        
        # VADER mengembalikan kamus: neg, neu, pos, dan compound
        scores = analyzer.polarity_scores(text)
        compound = scores['compound']
        
        # Logika klasifikasi sesuai Bab 3 Metodologi
        if compound >= 0.05:
            sentiment_label = "Positive"
        elif compound <= -0.05:
            sentiment_label = "Negative"
        else:
            sentiment_label = "Neutral"
            
        return compound, sentiment_label

    print("[*] Menghitung skor polaritas emosi untuk 1.845 baris data...")
    
    # Menerapkan fungsi ke kolom Text_VADER dan memecah hasilnya ke dua kolom baru
    df[['Vader_Compound_Score', 'Sentiment_Class']] = df.apply(
        lambda row: pd.Series(get_sentiment(row['Text_VADER'])), axis=1
    )
    
    # Menyimpan hasil akhir
    df.to_csv(output_file, index=False, encoding='utf-8')
    print(f"[SUKSES] Analisis selesai! Data tersimpan di: {output_file}\n")
    
    # --- MENCETAK LAPORAN STATISTIK UNTUK BAB 4 ---
    print("=== RINGKASAN HASIL SENTIMEN (UNTUK BAB 4) ===")
    
    # Menghitung total sentimen keseluruhan
    total_sentiment = df['Sentiment_Class'].value_counts()
    print("\n1. Distribusi Sentimen Keseluruhan:")
    print(total_sentiment.to_string())
    
    # Menghitung sentimen per game (Komparasi RPG vs Simulator)
    print("\n2. Komparasi Sentimen per Game:")
    comparison = pd.crosstab(df['Subreddit'], df['Sentiment_Class'], margins=True)
    print(comparison.to_string())

if __name__ == "__main__":
    analyze_sentiment()