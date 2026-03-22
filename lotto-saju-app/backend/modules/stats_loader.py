"""
lotto_rounds 테이블에서 직접 번호 통계를 계산하는 모듈
"""
import os
from typing import Dict

# 캐시 (서버 실행 중 한번만 계산)
_cached_stats: Dict | None = None


def load_stats_from_supabase() -> Dict:
    """lotto_rounds에서 직접 통계 계산"""
    global _cached_stats
    if _cached_stats is not None:
        return _cached_stats

    supabase_url = os.getenv("SUPABASE_URL", "")
    supabase_key = os.getenv("SUPABASE_ANON_KEY", "")

    if not supabase_url or not supabase_key:
        raise RuntimeError("SUPABASE_URL, SUPABASE_ANON_KEY 환경변수가 설정되지 않았습니다.")

    from supabase import create_client
    client = create_client(supabase_url, supabase_key)

    # 전체 라운드 데이터 로드 (round_number 오름차순)
    all_rows = []
    page_size = 1000
    offset = 0
    while True:
        response = client.table("lotto_rounds") \
            .select("round_number,numbers") \
            .order("round_number") \
            .range(offset, offset + page_size - 1) \
            .execute()
        rows = response.data
        if not rows:
            break
        all_rows.extend(rows)
        if len(rows) < page_size:
            break
        offset += page_size

    if not all_rows:
        raise RuntimeError("lotto_rounds 테이블에 데이터가 없습니다.")

    total_rounds = len(all_rows)

    # 1~45 통계 초기화
    stats = {n: {
        "total_frequency": 0,
        "recent_5_frequency": 0,
        "recent_20_frequency": 0,
        "last_seen_round": 0,
    } for n in range(1, 46)}

    # 계산
    for idx, row in enumerate(all_rows):
        round_num = row["round_number"]
        numbers = row["numbers"]
        for num in numbers:
            if 1 <= num <= 45:
                stats[num]["total_frequency"] += 1
                stats[num]["last_seen_round"] = round_num

                if idx >= total_rounds - 5:
                    stats[num]["recent_5_frequency"] += 1
                if idx >= total_rounds - 20:
                    stats[num]["recent_20_frequency"] += 1

    _cached_stats = stats
    print(f"[OK] lotto_rounds {total_rounds}회 데이터에서 통계 계산 완료")
    return stats


def clear_stats_cache():
    """캐시 초기화"""
    global _cached_stats
    _cached_stats = None
