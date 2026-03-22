"""
Vercel Serverless Function - 로또 번호 추천 API
POST /api/recommend
"""
import json
import sys
import os
from http.server import BaseHTTPRequestHandler
from datetime import date

# backend/modules를 import할 수 있도록 경로 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from modules.recommender import generate_lotto_numbers
from modules.saju import calculate_saju, get_today_energy
from modules.stats_loader import load_stats_from_supabase


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            data = json.loads(body)

            birth_date = data.get("birth_date", "")
            target_date = data.get("target_date") or date.today().isoformat()
            user_name = data.get("user_name", "")

            if not birth_date:
                self._send_json(400, {"error": "birth_date is required"})
                return

            # Supabase에서 실제 통계 로드 (실패 시 더미 폴백)
            stats = load_stats_from_supabase()

            result = generate_lotto_numbers(
                birth_date=birth_date,
                target_date=target_date,
                stats=stats,
                user_name=user_name,
            )

            response = {
                "numbers": result["numbers"],
                "reason": result["reason"],
                "user_saju": {
                    "year": result["saju"]["year_pillar"],
                    "month": result["saju"]["month_pillar"],
                    "day": result["saju"]["day_pillar"],
                    "elements": result["saju"]["elements"],
                    "lacking": result["saju"]["lacking"],
                    "lacking_all": result["saju"]["lacking_all"],
                },
                "today_energy": {
                    "stem": result["today"]["heavenly_stem"],
                    "branch": result["today"]["earthly_branch"],
                    "element": result["today"]["element"],
                },
            }

            self._send_json(200, response)

        except Exception as e:
            self._send_json(500, {"error": str(e)})

    def do_OPTIONS(self):
        self.send_response(200)
        self._set_cors_headers()
        self.end_headers()

    def _send_json(self, status_code, data):
        self.send_response(status_code)
        self._set_cors_headers()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

    def _set_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
