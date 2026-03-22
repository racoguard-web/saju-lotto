"""
Pydantic models for request/response
"""
from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import date


class SajuInfo(BaseModel):
    """사주 정보"""
    year_pillar: str
    month_pillar: str
    day_pillar: str
    elements: Dict[str, int]
    dominant: str
    lacking: str


class TodayEnergy(BaseModel):
    """오늘의 기운"""
    heavenly_stem: str
    earthly_branch: str
    element: str
    relation_to_user: str


class RecommendationResponse(BaseModel):
    """추천 번호 응답"""
    type: str
    numbers: List[int]
    reason: str


class LottoRecommendRequest(BaseModel):
    """로또 추천 요청"""
    birth_date: str  # YYYY-MM-DD
    target_date: Optional[str] = None  # YYYY-MM-DD, default: today


class LottoRecommendResponse(BaseModel):
    """로또 추천 응답"""
    user_saju: SajuInfo
    today_energy: TodayEnergy
    recommendation: RecommendationResponse
