"""
로또 추천 엔진
사주 + 오늘 날짜 + 히스토리 기반 결정형 알고리즘
"""
import hashlib
import random
from typing import List, Tuple, Dict
from datetime import datetime

from .saju import calculate_saju, get_today_energy
from .number_props import (
    get_element, get_element_english, get_number_attributes,
    ELEMENT_CYCLE, ELEMENT_CONFLICT, check_element_relation,
    get_complementary_element
)


def generate_seed(birth_date: str, target_date: str, version: str = "NEO_V1") -> int:
    """
    결정형 랜덤을 위한 시드 생성
    같은 입력이면 항상 같은 시드
    """
    seed_input = f"{birth_date}|{target_date}|{version}"
    hash_value = hashlib.sha256(seed_input.encode()).hexdigest()
    return int(hash_value, 16)


def calculate_saju_score(number: int, saju: Dict) -> float:
    """
    사주 적합도 점수 (0~1)
    부족한 오행 보완, 과한 오행 억제
    """
    score = 0.5  # 기본 점수
    
    number_element = get_element_english(number)
    lacking_all = saju.get("lacking_all", [saju["lacking"]])
    dominant = saju["dominant"]

    # 부족한 오행 보완 (+0.3) - 부족한 오행이 여러 개면 전부 반영
    if number_element in lacking_all:
        score += 0.3
    
    # 과한 오행 억제 (-0.2)
    if number_element == dominant:
        score -= 0.2
    
    # 일간과 상생 관계 (+0.2)
    day_stem = saju["day_stem"]
    # 간단한 상생 체크
    
    return max(0.0, min(1.0, score))


def calculate_today_score(number: int, today: Dict, saju: Dict) -> float:
    """
    오늘 적합도 점수 (0~1)
    오늘 기운과 조화
    """
    score = 0.5
    
    number_element = get_element_english(number)
    today_element = today["element"]
    
    relation = check_element_relation(today_element, number_element)
    
    if relation == "상생":
        score += 0.3
    elif relation == "상극":
        score -= 0.2
    elif relation == "동일":
        score += 0.1
    
    return max(0.0, min(1.0, score))


def calculate_history_score(number: int, stats: Dict) -> float:
    """
    히스토리 보정 점수 (0~1)
    과열/냉각 번호 보정
    """
    score = 0.5
    
    if number not in stats:
        return score
    
    stat = stats[number]
    
    # 전체 출현 빈도 (정규화)
    total_freq = stat.get("total_frequency", 0)
    # 평균보다 낮으면 가점, 높으면 감점
    if total_freq < 150:  # 상대적으로 적게 나옴
        score += 0.1
    elif total_freq > 250:  # 상대적으로 많이 나옴
        score -= 0.1
    
    # 최근 5회 과열 체크
    recent_5 = stat.get("recent_5_frequency", 0)
    if recent_5 >= 2:  # 최근 5회 중 2회 이상
        score -= 0.15
    
    return max(0.0, min(1.0, score))


def seed_noise(number: int, rng: random.Random) -> float:
    """
    시드 기반 미세 변동 (0~1)
    같은 시드면 항상 같은 값
    """
    return rng.random()


def calculate_all_scores(
    birth_date: str,
    target_date: str,
    stats: Dict
) -> List[Tuple[int, float]]:
    """
    1~45 모든 번호 점수 계산
    """
    # 사주 계산
    saju = calculate_saju(birth_date)
    today = get_today_energy(target_date)
    
    # 시드 생성
    seed = generate_seed(birth_date, target_date)
    rng = random.Random(seed)
    
    scores = []
    
    for n in range(1, 46):
        saju_score = calculate_saju_score(n, saju)
        today_score = calculate_today_score(n, today, saju)
        history_score = calculate_history_score(n, stats)
        noise = seed_noise(n, rng)
        
        # 최종 점수: 사주 50% + 오늘 30% + 히스토리 15% + 시드 5%
        final_score = (
            50 * saju_score +
            30 * today_score +
            15 * history_score +
            5 * noise
        )
        
        scores.append((n, final_score))
    
    return scores, saju, today


def is_valid_combination(current: List[int], candidate: int) -> bool:
    """
    조합 필터 조건 체크
    """
    if not current:
        return True
    
    test_list = current + [candidate]
    
    # 1. 홀짝 몰림 방지 (6:0 또는 0:6 금지)
    odd_count = sum(1 for n in test_list if n % 2 == 1)
    if odd_count == 0 or odd_count == 6:
        return False
    
    # 2. 구간 몰림 방지 (한 구간에 4개 이상 금지)
    low = sum(1 for n in test_list if 1 <= n <= 15)
    mid = sum(1 for n in test_list if 16 <= n <= 30)
    high = sum(1 for n in test_list if 31 <= n <= 45)
    if low >= 4 or mid >= 4 or high >= 4:
        return False
    
    # 3. 연속수 3개 방지
    sorted_list = sorted(test_list)
    for i in range(len(sorted_list) - 2):
        if sorted_list[i+2] - sorted_list[i] == 2:
            return False
    
    # 4. 끝자리 몰림 방지 (같은 끝자리 3개 이상)
    last_digits = [n % 10 for n in test_list]
    for digit in set(last_digits):
        if last_digits.count(digit) >= 3:
            return False
    
    # 5. 오행 몰림 방지 (같은 오행 4개 이상)
    elements = [get_element(n) for n in test_list]
    for elem in set(elements):
        if elements.count(elem) >= 4:
            return False
    
    return True


def generate_reason(numbers: List[int], saju: Dict, today: Dict, user_name: str = "") -> str:
    """
    추천 이유 문구 생성
    """
    element_kr = {
        "wood": "목(木)", "fire": "화(火)", "earth": "토(土)",
        "metal": "금(金)", "water": "수(水)"
    }

    name_prefix = f"{user_name}님의" if user_name else "회원님의"
    lacking = saju["lacking"]
    today_elem = today.get("element", "")

    lacking_all = saju.get("lacking_all", [lacking]) if lacking else []
    lacking_kr_list = [element_kr.get(l, l) for l in lacking_all]
    lacking_text = "·".join(lacking_kr_list) if lacking_kr_list else ""
    today_kr = element_kr.get(today_elem, today_elem) if today_elem else ""

    if lacking_text and today_kr:
        return f"역대 로또 번호를 분석하여 {name_prefix} 사주에서 부족한 {lacking_text} 기운을 보완한 번호 중 오늘의 {today_kr} 행운 기운과 조합하여 선별했습니다."
    elif lacking_text:
        return f"역대 로또 번호를 분석하여 {name_prefix} 사주에서 부족한 {lacking_text} 기운을 보완한 번호를 선별했습니다."
    else:
        return f"역대 로또 번호를 분석하여 오늘의 행운 기운과 조합하여 선별했습니다."


def generate_lotto_numbers(
    birth_date: str,
    target_date: str,
    stats: Dict,
    user_name: str = ""
) -> Dict:
    """
    🎯 핵심 함수: 1세트 로또 번호 생성
    
    흐름:
    1. Seed 생성 (결정형)
    2. 1~45 점수 계산 (사주 50% + 오늘 30% + 히스토리 15% + 시드 5%)
    3. 상위 15개 후보 추출
    4. 시드 기반 셔플
    5. 필터 적용하여 6개 선택
    6. 오름차순 정렬
    """
    # 1~2. 점수 계산
    scores, saju, today = calculate_all_scores(birth_date, target_date, stats)
    
    # 3. 점수 순 정렬
    scores.sort(key=lambda x: x[1], reverse=True)
    
    # 4. 후보군 추출 (상위 15개)
    candidates = [n for n, _ in scores[:15]]
    
    # 5. 시드 기반 셔플
    seed = generate_seed(birth_date, target_date)
    rng = random.Random(seed)
    shuffled = candidates.copy()
    rng.shuffle(shuffled)
    
    # 6. 필터 적용 6개 선택
    result = []
    for n in shuffled:
        if is_valid_combination(result, n):
            result.append(n)
        if len(result) == 6:
            break
    
    # 7. 최종 정렬
    result.sort()
    
    # 8. 추천 이유 생성
    reason = generate_reason(result, saju, today, user_name)
    
    return {
        "numbers": result,
        "reason": reason,
        "saju": saju,
        "today": today
    }


if __name__ == "__main__":
    # 테스트
    stats = {n: {"total_frequency": 200, "recent_5_frequency": 1} for n in range(1, 46)}
    
    result = generate_lotto_numbers("1993-08-18", "2026-03-20", stats)
    print("생성된 번호:", result["numbers"])
    print("추천 이유:", result["reason"])
