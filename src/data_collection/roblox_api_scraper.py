import requests
import pandas as pd
from datetime import datetime
import os
import time

# 1. Konfigurasi ID Game Roblox
# Catatan: API Roblox menggunakan 'Universe ID', bukan ID dari URL Web biasa.
# Blox Fruits Universe ID: 994732206
# Bee Swarm Simulator Universe ID: 601130232
UNIVERSE_IDS = "994732206,601130232"
API_URL = f"https://games.roproxy.com/v1/games?universeIds={UNIVERSE_IDS}"

def fetch_roblox_telemetry():
    print("[INFO] Mengirim request ke Roblox Web API...")
    try:
        # Menambahkan Header User-Agent agar tidak diblokir oleh Anti-Bot Roblox
        headers = {
            "User-Agent": "RobloxUXResearchBot/1.0 (Academic Project; randysta.putra@binus.ac.id)",
            "Accept": "application/json"
        }

        time.sleep(2)

        response = requests.get(API_URL, headers=headers)
        response.raise_for_status() 
        data = response.json()["data"]
        
        # 2. Parsing dan Ekstraksi Metrik
        extracted_data = []
        for game in data:
            extracted_data.append({
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Game_Name": game.get("name"),
                "Genre_Category": "RPG" if game.get("name") == "Blox Fruits" else "Simulator",
                "Concurrent_Players": game.get("playing"),
                "Total_Visits": game.get("visits"),
                "Favorites": game.get("favorited")
            })
            
        return pd.DataFrame(extracted_data)
        
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Gagal menarik data dari API: {e}")
        return None

if __name__ == "__main__":
    df_telemetry = fetch_roblox_telemetry()
    
    if df_telemetry is not None and not df_telemetry.empty:
        print("\n[PREVIEW DATA METRIK]")
        print(df_telemetry.to_string(index=False))
        
        # 3. Pengaturan Jalur Simpan File CSV
        # Menyimpan data mundur dua tingkat ke luar folder src, masuk ke folder data/raw/
        output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "raw")
        
        # Memastikan folder data/raw/ benar-benar ada
        os.makedirs(output_dir, exist_ok=True)
        
        output_file = os.path.join(output_dir, "roblox_telemetry.csv")
        
        # Menyimpan DataFrame ke dalam CSV
        # Menggunakan mode='a' (append) jika ingin menjalankan skrip ini berkali-kali untuk tracking waktu
        df_telemetry.to_csv(output_file, index=False)
        print(f"\n[SUKSES] Data telemetri berhasil disimpan di: {output_file}")