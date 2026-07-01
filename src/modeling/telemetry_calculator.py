import pandas as pd
import os

def calculate_telemetry():
    print("[INFO] Membaca data historis API Roblox...")
    
    # Pengaturan direktori
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    input_file = os.path.join(base_dir, "data", "raw", "roblox_telemetry_comprehensive.csv")
    output_file = os.path.join(base_dir, "data", "processed", "telemetry_summary.csv")
    
    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"[ERROR] File tidak ditemukan: {input_file}")
        return
        
    # Mapping kolom persis sesuai struktur sampel CSV
    time_col = "Timestamp"
    game_col = "Game_Name"
    ccu_col = "Concurrent_Players"
    rating_col = "Approval_Rating_%"
    visit_col = "Total_Visits"
    
    games = df[game_col].unique()
    summary_data = []
    
    print("[*] Menghitung Median, Mean, dan Nilai Snapshot Terakhir...\n")
    
    for game in games:
        game_data = df[df[game_col] == game].copy()
        
        # Urutkan berdasarkan waktu dari paling lama ke paling baru
        game_data = game_data.sort_values(by=time_col)
        last_row = game_data.iloc[-1]
        
        # 1. Kalkulasi CCU (Median)
        ccu_val = int(game_data[ccu_col].median())
        
        # 2. Kalkulasi Upvote Ratio (Mean)
        rating_val = round(game_data[rating_col].mean(), 2)
        
        # 3. Kalkulasi Total Visits (Nilai Akhir)
        visit_val = int(last_row[visit_col])
        
        summary_data.append({
            "Game": game,
            "Concurrent Users (CCU)": ccu_val,
            "Upvote Ratio (%)": rating_val,
            "Total Visits": visit_val
        })

    # Konversi ke DataFrame untuk dicetak rapi
    summary_df = pd.DataFrame(summary_data)
    
    # Transpose tabel agar formatnya sesuai dengan draf artikel Bab 4.1
    summary_df.set_index("Game", inplace=True)
    final_table = summary_df.T
    final_table['Metode Kalkulasi'] = ['Median Historis', 'Rata-rata Historis', 'Snapshot Terakhir']
    
    # Simpan hasil untuk Joy
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    final_table.to_csv(output_file)
    
    print("=== FORMAT TABEL UNTUK COPY-PASTE JOY (BAB 4.1) ===")
    print(final_table.to_markdown())
    print(f"\n[SUKSES] File summary CSV telah dikunci di: {output_file}")

if __name__ == "__main__":
    calculate_telemetry()