import { useState, useCallback } from "react";
import type { LottoResponse } from "../types";

type DrawPhase = "idle" | "loading" | "shaking" | "dropping" | "revealing" | "done";

export interface DrawInfo {
  userName: string;
  birthDate: string;
}

export function useLottoDraw() {
  const [phase, setPhase] = useState<DrawPhase>("idle");
  const [result, setResult] = useState<LottoResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [userName, setUserName] = useState("");
  const [birthDate, setBirthDate] = useState("");
  const [drawnInfo, setDrawnInfo] = useState<DrawInfo | null>(null);

  const draw = useCallback(async () => {
    if (!birthDate) {
      setError("생년월일을 입력해주세요");
      return;
    }
    if (!userName.trim()) {
      setError("이름을 입력해주세요");
      return;
    }

    setError(null);
    setPhase("loading");

    try {
      const res = await fetch("/api/v1/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          birth_date: birthDate,
          user_name: userName.trim(),
        }),
      });

      if (!res.ok) {
        throw new Error("서버 오류가 발생했습니다");
      }

      const data: LottoResponse = await res.json();
      setResult(data);
      setDrawnInfo({ userName: userName.trim(), birthDate });

      // Animation sequence
      setPhase("shaking");
      await sleep(800);
      setPhase("dropping");
      await sleep(1200);
      setPhase("revealing");
      await sleep(600);
      setPhase("done");
    } catch (err) {
      setError(err instanceof Error ? err.message : "알 수 없는 오류");
      setPhase("idle");
    }
  }, [birthDate, userName]);

  const reset = useCallback(() => {
    setPhase("idle");
    setResult(null);
    setError(null);
    setDrawnInfo(null);
    setUserName("");
    setBirthDate("");
  }, []);

  return {
    phase,
    result,
    error,
    userName,
    setUserName,
    birthDate,
    setBirthDate,
    drawnInfo,
    draw,
    reset,
  };
}

function sleep(ms: number) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
