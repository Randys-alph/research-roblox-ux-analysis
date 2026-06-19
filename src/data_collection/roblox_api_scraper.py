import pandas as pd
from datetime import datetime
import os
import time
from curl_cffi import requests

UNIVERSE_IDS = "994732206,601130232"
API_URL_GAMES = f"https://games.roblox.com/v1/games?universeIds={UNIVERSE_IDS}"
API_URL_VOTES = f"https://games.roblox.com/v1/games/votes?universeIds={UNIVERSE_IDS}"

def fetch_telemetry_cffi():
    print("[INFO] Mengeksekusi penarikan data murni via curl_cffi...")
    
    # Daftar profil penyamaran modern. Skrip akan mencoba satu per satu.
    browser_profiles = ["chrome120", "chrome116", "edge101", "safari15_3"]
    games_json = None
    votes_json = None
    
    for profile in browser_profiles:
        print(f"[*] Mencoba menyamar sebagai: {profile}...")
        try:
            # verify=False ditambahkan untuk mengabaikan intersepsi SSL dari ISP/Antivirus lokal
            response_games = requests.get(API_URL_GAMES, impersonate=profile, timeout=15, verify=False)
            
            if response_games.status_code == 200:
                games_json = response_games.json()["data"]
                
                time.sleep(2) # Jeda aman
                response_votes = requests.get(API_URL_VOTES, impersonate=profile, timeout=15, verify=False)
                votes_json = response_votes.json()["data"]
                
                print(f"[SUKSES] Firewall berhasil ditembus menggunakan profil: {profile}")
                break # Keluar dari loop jika berhasil
                
        except Exception as e:
            print(f"[-] Gagal dengan profil {profile}. Mencoba profil selanjutnya...")
            
    # Jika setelah semua profil dicoba tetap gagal
    if not games_json or not votes_json:
        print("[ERROR] Semua jalur penyamaran diblokir oleh jaringan atau Cloudflare.")
        return None
        
    # Ekstraksi Data
    try:
        votes_dict = {vote["id"]: vote for vote in votes_json}
        extracted_data = []
        
        for game in games_json:
            univ_id = game.get("id")
            game_votes = votes_dict.get(univ_id, {})
            upvotes = game_votes.get("upVotes", 0)
            downvotes = game_votes.get("downVotes", 0)
            
            total_votes = upvotes + downvotes
            approval_rating = round((upvotes / total_votes * 100), 2) if total_votes > 0 else 0
            
            extracted_data.append({
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Game_Name": game.get("name"),
                "Genre_Category": "RPG" if game.get("name") == "Blox Fruits" else "Simulator",
                "Concurrent_Players": game.get("playing"),
                "Total_Visits": game.get("visits"),
                "Upvotes": upvotes,
                "Downvotes": downvotes,
                "Approval_Rating_%": approval_rating
            })
            
        return pd.DataFrame(extracted_data)
        
    except Exception as parse_err:
        print(f"[ERROR] Kegagalan saat memproses struktur data JSON: {parse_err}")
        return None

if __name__ == "__main__":
    import urllib3
    # Menonaktifkan peringatan terminal terkait penggunaan verify=False
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    df_telemetry = fetch_telemetry_cffi()
    
    if df_telemetry is not None and not df_telemetry.empty:
        print("\n[PREVIEW DATA OTOMATIS]")
        print(df_telemetry.to_string(index=False))
        
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        output_dir = os.path.join(base_dir, "data", "raw")
        os.makedirs(output_dir, exist_ok=True)
        
        output_file = os.path.join(output_dir, "roblox_telemetry_comprehensive.csv")
        header_condition = not os.path.exists(output_file)
        df_telemetry.to_csv(output_file, mode='a', index=False, header=header_condition)
        print(f"\n[SUKSES] Data ditambahkan ke: {output_file}")