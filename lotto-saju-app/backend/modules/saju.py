"""
사주 계산 모듈
만세력 기준 천간/지지 계산
"""
from datetime import datetime
from typing import Dict, Tuple

# 천간 (10개)
HEAVENLY_STEMS = ["갑", "을", "병", "정", "무", "기", "경", "신", "임", "계"]
HEAVENLY_STEMS_ELEMENTS = ["wood", "wood", "fire", "fire", "earth", "earth", "metal", "metal", "water", "water"]

# 지지 (12개)
EARTHLY_BRANCHES = ["자", "축", "인", "묘", "진", "사", "오", "미", "신", "유", "술", "해"]
EARTHLY_BRANCHES_ELEMENTS = ["water", "earth", "wood", "wood", "earth", "fire", "fire", "earth", "metal", "metal", "earth", "water"]

# 1924년 = 갑자년 (기준점)
BASE_YEAR = 1924


def get_year_pillar(year: int) -> Tuple[str, str]:
    """
    연주(년주) 계산
    1924년 = 갑자년
    """
    offset = year - BASE_YEAR
    stem_idx = offset % 10
    branch_idx = offset % 12
    return HEAVENLY_STEMS[stem_idx], EARTHLY_BRANCHES[branch_idx]


def get_month_pillar(year: int, month: int) -> Tuple[str, str]:
    """
    월주 계산
    간단한 규칙: 연도에 따른 월 시작점 + 월 오프셋
    """
    # 연간의 천간 인덱스
    year_offset = year - BASE_YEAR
    year_stem_idx = year_offset % 10
    
    # 월간은 연간에 따라 시작 (갑/기 → 병월 시작, 을/경 → 무월 시작...)
    month_stem_start = (year_stem_idx * 2) % 10
    month_stem_idx = (month_stem_start + month - 1) % 10
    
    # 월지는 정월=인월(2), 2월=묘월(3)...
    month_branch_idx = (month + 1) % 12  # 1월(1) → 인(2)
    
    return HEAVENLY_STEMS[month_stem_idx], EARTHLY_BRANCHES[month_branch_idx]


def get_day_pillar(year: int, month: int, day: int) -> Tuple[str, str]:
    """
    일주 계산
    1900년 1월 1일을 기준으로 오프셋 계산
    """
    # 기준일: 1900-01-01 = 임진일 (임=8, 진=4)
    base_date = datetime(1900, 1, 1)
    target_date = datetime(year, month, day)
    
    days_diff = (target_date - base_date).days
    
    # 임(8)진(4)에서부터 시작
    stem_idx = (8 + days_diff) % 10
    branch_idx = (4 + days_diff) % 12
    
    return HEAVENLY_STEMS[stem_idx], EARTHLY_BRANCHES[branch_idx]


def calculate_saju(birth_date: str) -> Dict:
    """
    생년월일로 사주 6자 계산
    
    Args:
        birth_date: "YYYY-MM-DD" 형식
    
    Returns:
        {
            "year_pillar": "계유",
            "month_pillar": "경신",
            "day_pillar": "신미",
            "elements": {"wood": 1, "fire": 0, "earth": 2, "metal": 2, "water": 1},
            "dominant": "metal",
            "lacking": "fire"
        }
    """
    date_obj = datetime.strptime(birth_date, "%Y-%m-%d")
    year, month, day = date_obj.year, date_obj.month, date_obj.day
    
    # 연주, 월주, 일주 계산
    year_stem, year_branch = get_year_pillar(year)
    month_stem, month_branch = get_month_pillar(year, month)
    day_stem, day_branch = get_day_pillar(year, month, day)
    
    # 오행 계산
    elements = {"wood": 0, "fire": 0, "earth": 0, "metal": 0, "water": 0}
    
    # 천간 오행
    for stem in [year_stem, month_stem, day_stem]:
        idx = HEAVENLY_STEMS.index(stem)
        elem = HEAVENLY_STEMS_ELEMENTS[idx]
        elements[elem] += 1
    
    # 지지 오행
    for branch in [year_branch, month_branch, day_branch]:
        idx = EARTHLY_BRANCHES.index(branch)
        elem = EARTHLY_BRANCHES_ELEMENTS[idx]
        elements[elem] += 1
    
    # 지배 오행 (가장 많은 것)
    dominant = max(elements, key=elements.get)
    
    # 부족한 오행 (가장 적은 것 전부)
    min_val = min(elements.values())
    lacking_list = [k for k, v in elements.items() if v == min_val]

    return {
        "year_pillar": f"{year_stem}{year_branch}",
        "month_pillar": f"{month_stem}{month_branch}",
        "day_pillar": f"{day_stem}{day_branch}",
        "year_stem": year_stem,
        "month_stem": month_stem,
        "day_stem": day_stem,
        "year_branch": year_branch,
        "month_branch": month_branch,
        "day_branch": day_branch,
        "elements": elements,
        "dominant": dominant,
        "lacking": lacking_list[0],
        "lacking_all": lacking_list,
    }


def get_today_energy(target_date: str) -> Dict:
    """
    오늘 날짜의 기운 계산
    
    Args:
        target_date: "YYYY-MM-DD" 형식
    
    Returns:
        {
            "heavenly_stem": "병",
            "earthly_branch": "술",
            "element": "화",
        }
    """
    date_obj = datetime.strptime(target_date, "%Y-%m-%d")
    
    # 오늘의 천간/지지 = 일주와 동일한 방식으로 계산
    stem, branch = get_day_pillar(date_obj.year, date_obj.month, date_obj.day)
    
    # 오행
    stem_idx = HEAVENLY_STEMS.index(stem)
    element = HEAVENLY_STEMS_ELEMENTS[stem_idx]
    
    return {
        "heavenly_stem": stem,
        "earthly_branch": branch,
        "element": element,
    }


def calculate_relation(user_day_stem: str, today_stem: str) -> str:
    """
    사용자 일간과 오늘 천간의 관계
    """
    user_idx = HEAVENLY_STEMS.index(user_day_stem)
    today_idx = HEAVENLY_STEMS.index(today_stem)
    
    user_element = HEAVENLY_STEMS_ELEMENTS[user_idx]
    today_element = HEAVENLY_STEMS_ELEMENTS[today_idx]
    
    if user_element == today_element:
        return "동일"
    elif (user_idx + 1) % 10 == today_idx or (user_idx + 2) % 10 == today_idx:
        return "상생"
    elif (user_idx - 1) % 10 == today_idx or (user_idx - 2) % 10 == today_idx:
        return "상극"
    else:
        return "중립"


# 테스트
if __name__ == "__main__":
    # 1993-08-18 테스트
    result = calculate_saju("1993-08-18")
    print("사주 계산 결과:", result)
    
    today = get_today_energy("2026-03-20")
    print("오늘의 기운:", today)
