"""
로또 번호 1~45 속성 정의
"""

# 오행 매핑 (5로 나눈 나머지)
# 1: 수, 2: 화, 3: 목, 4: 금, 0: 토
ELEMENT_MAP = {
    1: "수", 6: "수", 11: "수", 16: "수", 21: "수", 26: "수", 31: "수", 36: "수", 41: "수",
    2: "화", 7: "화", 12: "화", 17: "화", 22: "화", 27: "화", 32: "화", 37: "화", 42: "화",
    3: "목", 8: "목", 13: "목", 18: "목", 23: "목", 28: "목", 33: "목", 38: "목", 43: "목",
    4: "금", 9: "금", 14: "금", 19: "금", 24: "금", 29: "금", 34: "금", 39: "금", 44: "금",
    5: "토", 10: "토", 15: "토", 20: "토", 25: "토", 30: "토", 35: "토", 40: "토", 45: "토",
}

# 오행 한글 → 영문 매핑
ELEMENT_TO_ENGLISH = {
    "수": "water",
    "화": "fire", 
    "목": "wood",
    "금": "metal",
    "토": "earth"
}

# 오행 상생 관계
ELEMENT_CYCLE = {
    "wood": "fire",   # 목생화
    "fire": "earth",  # 화생토
    "earth": "metal", # 토생금
    "metal": "water", # 금생수
    "water": "wood",  # 수생목
}

# 오행 상극 관계
ELEMENT_CONFLICT = {
    "wood": "earth",  # 목극토
    "earth": "water", # 토극수
    "water": "fire",  # 수극화
    "fire": "metal",  # 화극금
    "metal": "wood",  # 금극목
}


def get_element(number: int) -> str:
    """번호의 오행 반환"""
    return ELEMENT_MAP.get(number, "토")


def get_element_english(number: int) -> str:
    """번호의 오행 영문 반환"""
    element_kr = get_element(number)
    return ELEMENT_TO_ENGLISH.get(element_kr, "earth")


def get_yin_yang(number: int) -> str:
    """음양 반환 (홀수=양, 짝수=음)"""
    return "양" if number % 2 == 1 else "음"


def get_zone(number: int) -> str:
    """번호 구간 반환"""
    if 1 <= number <= 15:
        return "초반"
    elif 16 <= number <= 30:
        return "중반"
    else:
        return "후반"


def get_last_digit(number: int) -> int:
    """끝자리 반환"""
    return number % 10


def get_number_attributes(number: int) -> dict:
    """번호의 모든 속성 반환"""
    return {
        "number": number,
        "element": get_element(number),
        "element_en": get_element_english(number),
        "yin_yang": get_yin_yang(number),
        "zone": get_zone(number),
        "last_digit": get_last_digit(number),
    }


# 모든 번호 속성 미리 계산
NUMBER_ATTRIBUTES = {n: get_number_attributes(n) for n in range(1, 46)}


def check_element_relation(element1: str, element2: str) -> str:
    """
    두 오행 간의 관계 반환
    상생, 상극, 중립
    """
    e1 = element1.lower()
    e2 = element2.lower()
    
    if ELEMENT_CYCLE.get(e1) == e2:
        return "상생"
    elif ELEMENT_CONFLICT.get(e1) == e2:
        return "상극"
    elif e1 == e2:
        return "동일"
    else:
        return "중립"


def get_complementary_element(lacking: str) -> str:
    """
    부족한 오행을 보완하는 오행 반환
    """
    # 상생 역순으로 보완
    reverse_cycle = {v: k for k, v in ELEMENT_CYCLE.items()}
    return reverse_cycle.get(lacking, "earth")
