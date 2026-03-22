"""
FastAPI 메인 애플리케이션
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from datetime import date

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.recommender import generate_lotto_numbers
from modules.saju import calculate_saju, get_today_energy

app = FastAPI(
    title="사주 로또 추천 API",
    description="생년월일 기반 개인화 로또 번호 추천 시스템",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 특정 도메인으로 제한
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LottoRequest(BaseModel):
    birth_date: str  # YYYY-MM-DD
    target_date: Optional[str] = None  # YYYY-MM-DD
    user_name: Optional[str] = None  # 사용자 이름


class LottoResponse(BaseModel):
    numbers: list[int]
    reason: str
    user_saju: dict
    today_energy: dict


@app.get("/")
async def root():
    return {
        "message": "사주 로또 추천 API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/api/v1/recommend", response_model=LottoResponse)
async def recommend_lotto(request: LottoRequest):
    """
    로또 번호 추천 API
    
    - birth_date: 생년월일 (YYYY-MM-DD)
    - target_date: 기준일 (YYYY-MM-DD, 기본값: 오늘)
    """
    try:
        # 기준일 설정
        target = request.target_date or date.today().isoformat()
        
        # 임시 통계 (DB 연결 후 변경)
        stats = {n: {"total_frequency": 200, "recent_5_frequency": 1} 
                for n in range(1, 46)}
        
        # 추천 생성
        result = generate_lotto_numbers(
            birth_date=request.birth_date,
            target_date=target,
            stats=stats,
            user_name=request.user_name or ""
        )
        
        return LottoResponse(
            numbers=result["numbers"],
            reason=result["reason"],
            user_saju={
                "year": result["saju"]["year_pillar"],
                "month": result["saju"]["month_pillar"],
                "day": result["saju"]["day_pillar"],
                "elements": result["saju"]["elements"],
                "lacking": result["saju"]["lacking"],
                "lacking_all": result["saju"]["lacking_all"],
            },
            today_energy={
                "stem": result["today"]["heavenly_stem"],
                "branch": result["today"]["earthly_branch"],
                "element": result["today"]["element"]
            }
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/saju/{birth_date}")
async def get_saju_info(birth_date: str):
    """
    사주 정보만 조회
    """
    try:
        saju = calculate_saju(birth_date)
        return {
            "year_pillar": saju["year_pillar"],
            "month_pillar": saju["month_pillar"],
            "day_pillar": saju["day_pillar"],
            "elements": saju["elements"],
            "lacking": saju["lacking"],
            "dominant": saju["dominant"]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)