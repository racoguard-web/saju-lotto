import { motion } from "framer-motion";

interface NumberBallProps {
  number: number;
  index: number;
  revealed: boolean;
}

function getBallStyle(n: number) {
  if (n <= 10) return { bg: "linear-gradient(135deg, #FFE082, #FFB300)", border: "#FF9F00" };
  if (n <= 20) return { bg: "linear-gradient(135deg, #81D4FA, #29B6F6)", border: "#0288D1" };
  if (n <= 30) return { bg: "linear-gradient(135deg, #EF9A9A, #EF5350)", border: "#D32F2F" };
  if (n <= 40) return { bg: "linear-gradient(135deg, #B0BEC5, #78909C)", border: "#546E7A" };
  return { bg: "linear-gradient(135deg, #CE93D8, #AB47BC)", border: "#8E24AA" };
}

export default function NumberBall({ number, index, revealed }: NumberBallProps) {
  const { bg, border } = getBallStyle(number);

  if (!revealed) {
    return (
      <div
        className="w-12 h-12 sm:w-14 sm:h-14 rounded-full flex items-center justify-center"
        style={{
          background: "#FFF0E0",
          border: "2.5px dashed #FFD6B0",
        }}
      >
        <motion.span
          animate={{ opacity: [0.3, 0.6, 0.3], scale: [0.9, 1.1, 0.9] }}
          transition={{ duration: 1.5, repeat: Infinity }}
          className="text-xl"
        >
          🐾
        </motion.span>
      </div>
    );
  }

  return (
    <motion.div
      initial={{ scale: 0, rotate: -180, y: -20 }}
      animate={{ scale: 1, rotate: 0, y: 0 }}
      transition={{
        type: "spring",
        stiffness: 300,
        damping: 16,
        delay: index * 0.15,
      }}
      className="lotto-ball w-12 h-12 sm:w-14 sm:h-14 rounded-full flex items-center justify-center"
      style={{
        background: bg,
        border: `2.5px solid ${border}`,
        boxShadow: `0 3px 10px ${border}40`,
      }}
    >
      <span
        className="text-xl sm:text-2xl font-extrabold text-white relative z-10"
        style={{ textShadow: "0 1px 2px rgba(0,0,0,0.2)" }}
      >
        {number}
      </span>
    </motion.div>
  );
}
