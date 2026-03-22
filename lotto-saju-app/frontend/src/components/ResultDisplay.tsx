import { motion } from "framer-motion";
import { useState } from "react";
import type { LottoResponse } from "../types";
import type { DrawInfo } from "../hooks/useLottoDraw";
import NumberBall from "./NumberBall";
import FortuneCard from "./FortuneCard";
import CatCharacter from "./CatCharacter";

interface ResultDisplayProps {
  result: LottoResponse;
  revealed: boolean;
  drawnInfo: DrawInfo;
  onReset: () => void;
}

export default function ResultDisplay({ result, revealed, drawnInfo, onReset }: ResultDisplayProps) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    const text = `🎰 행운의 로또 - ${drawnInfo.userName}님의 오늘의 번호\n${result.numbers.join(" ")}`;
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const formattedDate = (() => {
    const [y, m, d] = drawnInfo.birthDate.split("-");
    return `${y}년 ${parseInt(m)}월 ${parseInt(d)}일`;
  })();

  return (
    <div className="w-full max-w-md mx-auto space-y-4">
      {/* Cat celebrating */}
      <motion.div
        initial={{ opacity: 0, scale: 0.8 }}
        animate={{ opacity: 1, scale: 1 }}
        className="flex justify-center"
      >
        <CatCharacter phase={revealed ? "done" : "revealing"} />
      </motion.div>

      {/* User info card */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="card px-5 py-3 flex items-center justify-center gap-4 text-sm"
      >
        <span className="flex items-center gap-1.5">
          🐱 <span className="font-bold">{drawnInfo.userName}</span>
        </span>
        <span className="text-text-dim">|</span>
        <span className="flex items-center gap-1.5 text-text-muted">
          🎂 {formattedDate}
        </span>
      </motion.div>

      {/* Numbers Card */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="card p-6 sm:p-8"
      >
        <h3 className="text-xl font-bold mb-5 text-center flex items-center gap-2 justify-center">
          🍀 오늘의 행운 번호
        </h3>
        <div className="flex justify-center gap-2 sm:gap-3 flex-nowrap">
          {result.numbers.map((num, i) => (
            <NumberBall key={num} number={num} index={i} revealed={revealed} />
          ))}
        </div>
      </motion.div>

      {/* Reason */}
      {revealed && (
        <motion.div initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1.0 }} className="card p-5">
          <h3 className="text-lg font-bold mb-2 flex items-center gap-2">
            💡 추천 이유
          </h3>
          <p className="text-base text-text-muted leading-relaxed">{result.reason}</p>
        </motion.div>
      )}

      {/* Fortune Card */}
      {revealed && (
        <motion.div initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1.3 }}>
          <FortuneCard saju={result.user_saju} todayEnergy={result.today_energy} />
        </motion.div>
      )}

      {/* Buttons */}
      {revealed && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}
          transition={{ delay: 1.5 }} className="flex gap-3 justify-center pt-2 pb-4">
          <button onClick={onReset}
            className="flex items-center gap-2 px-5 py-3 rounded-full text-sm font-bold cursor-pointer transition-all"
            style={{ background: "white", border: "2px solid #FFE8D6", color: "#3D2C2C" }}>
            <i className="ri-refresh-line" /> 다시 뽑기
          </button>
          <button onClick={handleCopy}
            className="flex items-center gap-2 px-5 py-3 rounded-full text-sm font-bold text-white cursor-pointer transition-all"
            style={{
              background: copied
                ? "linear-gradient(135deg, #7BC67E, #4CAF50)"
                : "linear-gradient(135deg, #FF8C42, #FF6B8A)",
              boxShadow: "0 3px 12px rgba(255,107,138,0.25)",
            }}>
            {copied ? <>✅ 복사됨!</> : <>📋 번호 복사</>}
          </button>
        </motion.div>
      )}
    </div>
  );
}
