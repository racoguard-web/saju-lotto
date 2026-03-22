"""
동행복권 로또 데이터 크롤러
"""
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
from typing import List, Dict, Optional
import sqlite3
import time


def fetch_lotto_round(round_no: int) -> Optional[Dict]:
    """
    특정 회차의 로또 데이터 가져오기
    """
    url = f"https://www.dhlottery.co.kr/gameResult.do?method=byWin&drwNo={round_no}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 당첨 번호 추출
        win_nums = soup.select('.win_result .num.win .ball_645')
        if not win_nums:
            return None
        
        numbers = [int(num.text.strip()) for num in win_nums[:6]]
        
        # 보너스 번호
        bonus_elem = soup.select_one('.win_result .num.bonus .ball_645')
        bonus_number = int(bonus_elem.text.strip()) if bonus_elem else None
        
        # 추첨일
        date_elem = soup.select_one('.win_result .desc')
        draw_date = None
        if date_elem:
            date_text = date_elem.text.strip()
            # "2026년 03월 20일 추첨" 형식 파싱
            try:
                draw_date = datetime.strptime(date_text.split()[0], "%Y년%m월%d일").strftime("%Y-%m-%d")
            except:
                pass
        
        return {
            "round_number": round_no,
            "draw_date": draw_date,
            "numbers": numbers,
            "bonus_number": bonus_number
        }
    
    except Exception as e:
        print(f"Error fetching round {round_no}: {e}")
        return None


def fetch_all_lotto_data(start_round: int = 1, end_round: int = 1241) -> List[Dict]:
    """
    모든 로또 데이터 수집
    """
    results = []
    
    for round_no in range(start_round, end_round + 1):
        data = fetch_lotto_round(round_no)
        if data:
            results.append(data)
            print(f"✓ Round {round_no} fetched")
        else:
            print(f"✗ Round {round_no} failed")
        
        # Rate limiting
        time.sleep(0.5)
    
    return results


def save_to_sqlite(data: List[Dict], db_path: str = "lotto_data.db"):
    """
    SQLite에 데이터 저장
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 테이블 생성
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lotto_rounds (
            round_number INTEGER PRIMARY KEY,
            draw_date TEXT,
            numbers TEXT,
            bonus_number INTEGER
        )
    """)
    
    # 데이터 삽입
    for item in data:
        cursor.execute("""
            INSERT OR REPLACE INTO lotto_rounds (round_number, draw_date, numbers, bonus_number)
            VALUES (?, ?, ?, ?)
        """, (
            item["round_number"],
            item["draw_date"],
            json.dumps(item["numbers"]),
            item["bonus_number"]
        ))
    
    conn.commit()
    conn.close()
    print(f"✓ Saved {len(data)} rounds to {db_path}")


def calculate_number_stats(db_path: str = "lotto_data.db") -> Dict[int, Dict]:
    """
    번호별 통계 계산
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT round_number, numbers FROM lotto_rounds ORDER BY round_number")
    rows = cursor.fetchall()
    
    conn.close()
    
    if not rows:
        return {}
    
    # 번호별 통계 초기화
    stats = {n: {
        "number": n,
        "total_frequency": 0,
        "recent_5_frequency": 0,
        "recent_20_frequency": 0,
        "last_seen_round": 0
    } for n in range(1, 46)}
    
    total_rounds = len(rows)
    
    for round_num, numbers_json in rows:
        numbers = json.loads(numbers_json)
        
        for num in numbers:
            stats[num]["total_frequency"] += 1
            stats[num]["last_seen_round"] = round_num
            
            # 최근 5회
            if round_num > total_rounds - 5:
                stats[num]["recent_5_frequency"] += 1
            
            # 최근 20회
            if round_num > total_rounds - 20:
                stats[num]["recent_20_frequency"] += 1
    
    return stats


def save_stats_to_sqlite(stats: Dict[int, Dict], db_path: str = "lotto_data.db"):
    """
    통계 데이터를 SQLite에 저장
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS number_stats (
            number INTEGER PRIMARY KEY,
            total_frequency INTEGER,
            recent_5_frequency INTEGER,
            recent_20_frequency INTEGER,
            last_seen_round INTEGER
        )
    """)
    
    for num, data in stats.items():
        cursor.execute("""
            INSERT OR REPLACE INTO number_stats 
            (number, total_frequency, recent_5_frequency, recent_20_frequency, last_seen_round)
            VALUES (?, ?, ?, ?, ?)
        """, (
            data["number"],
            data["total_frequency"],
            data["recent_5_frequency"],
            data["recent_20_frequency"],
            data["last_seen_round"]
        ))
    
    conn.commit()
    conn.close()
    print(f"✓ Saved stats for 45 numbers to {db_path}")


if __name__ == "__main__":
    # 테스트: 최근 10회만 가져오기
    print("Fetching recent 10 rounds...")
    data = fetch_all_lotto_data(1232, 1241)
    
    if data:
        save_to_sqlite(data)
        stats = calculate_number_stats()
        save_stats_to_sqlite(stats)
