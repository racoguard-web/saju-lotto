# -*- coding: utf-8 -*-
"""
Donghaeng Lottery Lotto Data Crawler
Fetches 1-1241 round data and saves to Supabase
"""
import requests
from bs4 import BeautifulSoup
import psycopg2
import time
import sys
import os
from datetime import datetime
from typing import Optional, Dict, List
from dotenv import load_dotenv

load_dotenv()

# Supabase connection info (from .env)
SUPABASE_DB_HOST = os.getenv("SUPABASE_DB_HOST", "")
SUPABASE_DB_NAME = os.getenv("SUPABASE_DB_NAME", "postgres")
SUPABASE_DB_USER = os.getenv("SUPABASE_DB_USER", "postgres")
SUPABASE_DB_PASSWORD = os.getenv("SUPABASE_DB_PASSWORD", "")
SUPABASE_DB_PORT = int(os.getenv("SUPABASE_DB_PORT", "5432"))


def get_db_connection():
    """Connect to Supabase PostgreSQL"""
    return psycopg2.connect(
        host=SUPABASE_DB_HOST,
        database=SUPABASE_DB_NAME,
        user=SUPABASE_DB_USER,
        password=SUPABASE_DB_PASSWORD,
        port=SUPABASE_DB_PORT,
        sslmode="require"
    )


def create_tables():
    """Create necessary tables"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Lotto rounds table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lotto_rounds (
            round_number INTEGER PRIMARY KEY,
            draw_date DATE,
            numbers INTEGER[] NOT NULL,
            bonus_number INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Number stats table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS number_stats (
            number INTEGER PRIMARY KEY,
            total_frequency INTEGER DEFAULT 0,
            recent_5_frequency INTEGER DEFAULT 0,
            recent_20_frequency INTEGER DEFAULT 0,
            last_seen_round INTEGER DEFAULT 0,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    cursor.close()
    conn.close()
    print("[OK] Tables created")


def fetch_lotto_round(round_no: int) -> Optional[Dict]:
    """
    Fetch specific round data from Donghaeng Lottery
    """
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
                # "2026년 03월 20일 추첨" format
                date_part = date_text.split('추첨')[0].strip()
                date_part = date_part.replace(' ', '')
                draw_date = datetime.strptime(date_part, "%Y년%m월%d일").date()
            except Exception as e:
                print(f"  [WARN] Date parsing failed: {date_text}, error: {e}")
        
        return {
            "round_number": round_no,
            "draw_date": draw_date,
            "numbers": numbers,
            "bonus_number": bonus_number
        }
    
    except requests.exceptions.RequestException as e:
        print(f"  [ERROR] Round {round_no}: Network error - {e}")
        return None
    except Exception as e:
        print(f"  [ERROR] Round {round_no}: Processing error - {e}")
        return None


def save_rounds_to_db(rounds_data: List[Dict]):
    """Save round data to database"""
    if not rounds_data:
        return
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # UPSERT (update if exists, insert if not)
    for data in rounds_data:
        cursor.execute("""
            INSERT INTO lotto_rounds (round_number, draw_date, numbers, bonus_number)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (round_number) 
            DO UPDATE SET 
                draw_date = EXCLUDED.draw_date,
                numbers = EXCLUDED.numbers,
                bonus_number = EXCLUDED.bonus_number,
                created_at = CURRENT_TIMESTAMP
        """, (
            data["round_number"],
            data["draw_date"],
            data["numbers"],
            data["bonus_number"]
        ))
    
    conn.commit()
    cursor.close()
    conn.close()


def calculate_and_save_stats():
    """Calculate and save number statistics"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get all round data
    cursor.execute("""
        SELECT round_number, numbers 
        FROM lotto_rounds 
        ORDER BY round_number ASC
    """)
    rows = cursor.fetchall()
    
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
    for idx, (round_num, numbers) in enumerate(rows):
        for num in numbers:
            stats[num]["total_frequency"] += 1
            stats[num]["last_seen_round"] = round_num
            
            # Recent 5
            if idx >= total_rounds - 5:
                stats[num]["recent_5_frequency"] += 1
            
            # Recent 20
            if idx >= total_rounds - 20:
                stats[num]["recent_20_frequency"] += 1
    
    # Save to DB
    for num, stat in stats.items():
        cursor.execute("""
            INSERT INTO number_stats 
            (number, total_frequency, recent_5_frequency, recent_20_frequency, last_seen_round, updated_at)
            VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
            ON CONFLICT (number) 
            DO UPDATE SET 
                total_frequency = EXCLUDED.total_frequency,
                recent_5_frequency = EXCLUDED.recent_5_frequency,
                recent_20_frequency = EXCLUDED.recent_20_frequency,
                last_seen_round = EXCLUDED.last_seen_round,
                updated_at = CURRENT_TIMESTAMP
        """, (
            stat["number"],
            stat["total_frequency"],
            stat["recent_5_frequency"],
            stat["recent_20_frequency"],
            stat["last_seen_round"]
        ))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print(f"[OK] Statistics calculated for numbers 1-45")


def crawl_all_lotto_data(start_round: int = 1, end_round: int = 1241, batch_size: int = 10):
    """
    Crawl all lotto data
    """
    print("=" * 50)
    print("Donghaeng Lottery Lotto Data Crawler")
    print(f"Target: Round {start_round} ~ {end_round}")
    print(f"Batch size: {batch_size}")
    print("=" * 50)
    
    # Create tables
    create_tables()
    
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
            print(f"[FAIL] Round {round_no}: Collection failed")
        
        # Batch save
        if len(batch_data) >= batch_size:
            save_rounds_to_db(batch_data)
            print(f"[DB] Saved {len(batch_data)} rounds")
            batch_data = []
        
        # Rate limiting
        time.sleep(0.3)
        
        # Progress report (every 100 rounds)
        if round_no % 100 == 0:
            print(f"\n[PROGRESS] {round_no}/{end_round} rounds ({round_no/end_round*100:.1f}%)")
            print(f"   Success: {success_count}, Failed: {fail_count}\n")
    
    # Save remaining data
    if batch_data:
        save_rounds_to_db(batch_data)
        print(f"[DB] Saved remaining {len(batch_data)} rounds")
    
    print("=" * 50)
    print(f"[DONE] Crawling complete!")
    print(f"   Total: {end_round - start_round + 1} rounds")
    print(f"   Success: {success_count}, Failed: {fail_count}")
    
    # Calculate statistics
    print("\n[INFO] Calculating number statistics...")
    calculate_and_save_stats()
    
    print("\n[COMPLETE] All tasks finished!")


def get_latest_round_from_db() -> int:
    """Get latest round number from DB"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(round_number) FROM lotto_rounds")
        result = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return result or 0
    except:
        return 0


if __name__ == "__main__":
    # Command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "incremental":
            # Incremental update (only new rounds)
            latest = get_latest_round_from_db()
            print(f"[INFO] Latest round in DB: {latest}")
            if latest < 1241:
                print(f"[INFO] Incremental crawl from {latest + 1} to 1241")
                crawl_all_lotto_data(latest + 1, 1241)
            else:
                print("[OK] Already up to date")
        elif sys.argv[1] == "stats-only":
            # Recalculate stats only
            calculate_and_save_stats()
        else:
            # Specific range
            start = int(sys.argv[1])
            end = int(sys.argv[2]) if len(sys.argv) > 2 else start
            crawl_all_lotto_data(start, end, batch_size=5)
    else:
        # Full crawl (1-1241)
        crawl_all_lotto_data(1, 1241, batch_size=10)