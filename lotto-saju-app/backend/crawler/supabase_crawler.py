# -*- coding: utf-8 -*-
"""
Donghaeng Lottery Lotto Data Crawler (Supabase REST API Version)
"""
import requests
from bs4 import BeautifulSoup
from supabase import create_client, Client
import time
import sys
import os
from datetime import datetime
from typing import Optional, Dict, List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Supabase configuration
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY", "")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def fetch_lotto_round(round_no: int) -> Optional[Dict]:
    """Fetch specific round data from Donghaeng Lottery"""
    url = f"https://www.dhlottery.co.kr/gameResult.do?method=byWin&drwNo={round_no}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        response.encoding = 'utf-8'
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract winning numbers
        win_nums = soup.select('.win_result .num.win .ball_645')
        if not win_nums or len(win_nums) < 6:
            print(f"  [WARN] Round {round_no}: Winning numbers not found")
            return None
        
        numbers = [int(num.text.strip()) for num in win_nums[:6]]
        
        # Bonus number
        bonus_elem = soup.select_one('.win_result .num.bonus .ball_645')
        bonus_number = int(bonus_elem.text.strip()) if bonus_elem else None
        
        # Parse draw date
        draw_date = None
        date_elem = soup.select_one('.win_result .desc')
        if date_elem:
            date_text = date_elem.text.strip()
            try:
                date_part = date_text.split('추첨')[0].strip()
                date_part = date_part.replace(' ', '')
                draw_date = datetime.strptime(date_part, "%Y년%m월%d일").date().isoformat()
            except Exception as e:
                print(f"  [WARN] Date parsing failed: {date_text}, error: {e}")
        
        return {
            "round_number": round_no,
            "draw_date": draw_date,
            "numbers": numbers,
            "bonus_number": bonus_number
        }
    
    except Exception as e:
        print(f"  [ERROR] Round {round_no}: {e}")
        return None


def save_rounds_to_supabase(rounds_data: List[Dict]):
    """Save round data to Supabase"""
    if not rounds_data:
        return
    
    for data in rounds_data:
        try:
            # Upsert: insert or update
            supabase.table("lotto_rounds").upsert(data).execute()
        except Exception as e:
            print(f"  [ERROR] Failed to save round {data['round_number']}: {e}")
    
    print(f"[DB] Saved {len(rounds_data)} rounds to Supabase")


def calculate_and_save_stats():
    """Calculate and save number statistics"""
    try:
        # Get all rounds from Supabase
        response = supabase.table("lotto_rounds").select("*").order("round_number").execute()
        rows = response.data
        
        if not rows:
            print("[WARN] No data for statistics calculation")
            return
        
        total_rounds = len(rows)
        print(f"[INFO] Calculating statistics from {total_rounds} rounds...")
        
        # Initialize stats
        stats = {n: {
            "number": n,
            "total_frequency": 0,
            "recent_5_frequency": 0,
            "recent_20_frequency": 0,
            "last_seen_round": 0
        } for n in range(1, 46)}
        
        # Process all rounds
        for idx, row in enumerate(rows):
            round_num = row["round_number"]
            numbers = row["numbers"]
            
            for num in numbers:
                stats[num]["total_frequency"] += 1
                stats[num]["last_seen_round"] = round_num
                
                # Recent 5
                if idx >= total_rounds - 5:
                    stats[num]["recent_5_frequency"] += 1
                
                # Recent 20
                if idx >= total_rounds - 20:
                    stats[num]["recent_20_frequency"] += 1
        
        # Save to Supabase
        for num, stat in stats.items():
            supabase.table("number_stats").upsert({
                "number": stat["number"],
                "total_frequency": stat["total_frequency"],
                "recent_5_frequency": stat["recent_5_frequency"],
                "recent_20_frequency": stat["recent_20_frequency"],
                "last_seen_round": stat["last_seen_round"]
            }).execute()
        
        print(f"[OK] Statistics calculated for numbers 1-45")
    
    except Exception as e:
        print(f"[ERROR] Statistics calculation failed: {e}")


def crawl_lotto_data(start_round: int = 1, end_round: int = 1241, batch_size: int = 10):
    """Crawl all lotto data"""
    print("=" * 50)
    print("Donghaeng Lottery Lotto Data Crawler (Supabase)")
    print(f"Target: Round {start_round} ~ {end_round}")
    print("=" * 50)
    
    success_count = 0
    fail_count = 0
    batch_data = []
    
    for round_no in range(start_round, end_round + 1):
        data = fetch_lotto_round(round_no)
        
        if data:
            batch_data.append(data)
            success_count += 1
            print(f"[OK] Round {round_no}: {data['numbers']} (Bonus: {data['bonus_number']})")
        else:
            fail_count += 1
            print(f"[FAIL] Round {round_no}")
        
        # Batch save
        if len(batch_data) >= batch_size:
            save_rounds_to_supabase(batch_data)
            batch_data = []
        
        # Rate limiting
        time.sleep(0.3)
        
        # Progress report
        if round_no % 100 == 0:
            print(f"\n[PROGRESS] {round_no}/{end_round} ({round_no/end_round*100:.1f}%)")
            print(f"   Success: {success_count}, Failed: {fail_count}\n")
    
    # Save remaining
    if batch_data:
        save_rounds_to_supabase(batch_data)
    
    print("=" * 50)
    print(f"[DONE] Crawling complete!")
    print(f"   Success: {success_count}, Failed: {fail_count}")
    
    # Calculate statistics
    print("\n[INFO] Calculating statistics...")
    calculate_and_save_stats()
    
    print("\n[COMPLETE] All tasks finished!")


def get_latest_round() -> int:
    """Get latest round from Supabase"""
    try:
        response = supabase.table("lotto_rounds").select("round_number").order("round_number", desc=True).limit(1).execute()
        if response.data:
            return response.data[0]["round_number"]
        return 0
    except:
        return 0


if __name__ == "__main__":
    # Test with latest 2 rounds first
    print("[TEST] Fetching latest 2 rounds...")
    for round_no in [1240, 1241]:
        data = fetch_lotto_round(round_no)
        if data:
            print(f"[TEST OK] Round {round_no}: {data}")
        else:
            print(f"[TEST FAIL] Round {round_no}")
    
    print("\n" + "=" * 50)
    print("Test complete. Ready for full crawl!")
    print("Run: python supabase_crawler.py full")