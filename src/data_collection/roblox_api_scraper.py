import cloudscraper
import pandas as pd
from datetime import datetime
import os
import time

UNIVERSE_IDS = "994732206,601130232"

# KEMBALI KE JALUR RESMI ROBLOX (Cloudscraper akan mengatasi firewall-nya)
API_URL_GAMES = f"https://games.roblox.com/v1/games?universeIds={UNIVERSE_IDS}"
API_URL_VOTES = f"https://games.roblox.com/v1/games/votes?universeIds={UNIVERSE_IDS}"

def fetch_roblox_telemetry():
    print("[INFO] Mengirim request ke Roblox Web API via Cloudscraper...")
    try:
        # Membuat sesi scraper yang menyamar sebagai Google Chrome di Windows
        scraper = cloudscraper.create_scraper(
            browser={
                'browser': 'chrome',
                'platform': 'windows',
                'desktop': True
            }
        )
        
        # 1. Menarik data dasar (Pemain Aktif & Kunjungan)
        time.sleep(1) 
        response_games = scraper.get(API_URL_GAMES)
        response_games.raise_for_status() 
        games_data = response_games.json()["data"]
        
        # 2. Menarik data metrik kepuasan (Upvotes & Downvotes)
        time.sleep(1) 
        response_votes = scraper.get(API_URL_VOTES)
        response_votes.raise_for_status()
        votes_data = response_votes.json()["data"]
        
        # Memetakan data votes ke dalam dictionary berdasarkan universeId
        votes_dict = {vote["id"]: vote for vote in votes_data}
        
        # 3. Menggabungkan dan mengkalkulasi metrik
        extracted_data = []
        for game in games_data:
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
        
    except Exception as e:
        print(f"[ERROR] Gagal menarik data dari API: {e}")
        return None

if __name__ == "__main__":
    df_telemetry = fetch_roblox_telemetry()
    
    if df_telemetry is not None and not df_telemetry.empty:
        print("\n[PREVIEW DATA METRIK KOMPREHENSIF]")
        print(df_telemetry.to_string(index=False))
        
        output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "raw")
        os.makedirs(output_dir, exist_ok=True)
        
        output_file = os.path.join(output_dir, "roblox_telemetry_comprehensive.csv")
        
        header_condition = not os.path.exists(output_file)
        df_telemetry.to_csv(output_file, mode='a', index=False, header=header_condition)
        
        print(f"\n[SUKSES] Data telemetri komprehensif berhasil disimpan di: {output_file}")