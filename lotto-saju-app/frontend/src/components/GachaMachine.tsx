import { motion, AnimatePresence } from "framer-motion";
import CatCharacter from "./CatCharacter";

interface GachaMachineProps {
  phase: string;
  onDraw: () => void;
  disabled: boolean;
}

const BALLS = [
  // Very bottom row (was label area)
  { x: 35,  y: 92, r: 14, color: "#FFD166" },
  { x: 68,  y: 95, r: 13, color: "#FF6B8A" },
  { x: 100, y: 93, r: 15, color: "#7BC67E" },
  { x: 135, y: 94, r: 14, color: "#6BB8E0" },
  { x: 168, y: 92, r: 13, color: "#C8A2E8" },
  { x: 200, y: 95, r: 14, color: "#FF8C42" },
  // Bottom row
  { x: 25,  y: 72, r: 15, color: "#FF7B7B" },
  { x: 58,  y: 75, r: 14, color: "#7BC67E" },
  { x: 90,  y: 73, r: 16, color: "#6BB8E0" },
  { x: 125, y: 74, r: 15, color: "#FFD166" },
  { x: 158, y: 72, r: 14, color: "#C8A2E8" },
  { x: 190, y: 75, r: 15, color: "#FF8C42" },
  { x: 220, y: 73, r: 14, color: "#FF6B8A" },
  // Middle row
  { x: 40,  y: 48, r: 14, color: "#A8B8C8" },
  { x: 72,  y: 50, r: 15, color: "#FF6B8A" },
  { x: 108, y: 47, r: 14, color: "#7BC67E" },
  { x: 142, y: 50, r: 15, color: "#FF7B7B" },
  { x: 175, y: 48, r: 14, color: "#6BB8E0" },
  { x: 205, y: 50, r: 13, color: "#E8C170" },
  // Top row
  { x: 60,  y: 27, r: 13, color: "#C8A2E8" },
  { x: 95,  y: 25, r: 14, color: "#FF8C42" },
  { x: 130, y: 27, r: 13, color: "#FFD166" },
  { x: 165, y: 25, r: 14, color: "#FF6B8A" },
  { x: 195, y: 28, r: 12, color: "#7BC67E" },
];

function LottoBallInBox({ x, y, r, color, shaking, index }: {
  x: number; y: number; r: number; color: string; shaking: boolean; index: number;
}) {
  return (
    <motion.g
      animate={
        shaking
          ? { x: [0, 4, -3, 3, -2, 0], y: [0, -3, 2, -2, 1, 0] }
          : { y: [0, -1.5, 0] }
      }
      transition={
        shaking
          ? { duration: 0.3, repeat: Infinity, delay: index * 0.015 }
          : { duration: 2 + index * 0.12, repeat: Infinity, ease: "easeInOut" }
      }
    >
      <circle cx={x} cy={y} r={r} fill={color} />
      <circle cx={x} cy={y} r={r} fill="none" stroke="white" strokeWidth="1.5" opacity="0.5" />
      {/* Highlight */}
      <circle cx={x - r * 0.25} cy={y - r * 0.25} r={r * 0.28} fill="white" opacity="0.35" />
    </motion.g>
  );
}

export default function GachaMachine({ phase, onDraw, disabled }: GachaMachineProps) {
  const isShaking = phase === "shaking";
  const isDropping = phase === "dropping";
  const isActive = phase !== "idle" && phase !== "done";

  return (
    <div className="flex flex-col items-center">
      {/* Cat with speech bubble */}
      <CatCharacter
        phase={phase}
        message={
          isActive
            ? "냥냥~ 행운의 번호를 찾고 있어요...! 🐾"
            : "오늘의 행운 번호를 뽑아줄게요! 🍀"
        }
      />

      {/* Lucky Box */}
      <motion.div
        animate={isShaking ? { rotate: [-1.5, 1.5, -1, 1, 0] } : {}}
        transition={isShaking ? { duration: 0.3, repeat: Infinity } : {}}
        className="relative -mt-4"
      >
        <svg viewBox="0 0 245 120" width="340" height="167">
          {/* Box shadow */}
          <ellipse cx="122" cy="115" rx="105" ry="6" fill="rgba(0,0,0,0.04)" />

          {/* Box body */}
          <rect x="8" y="10" width="230" height="100" rx="24" ry="24"
            fill="#FFF5E8" stroke="#FFD6B0" strokeWidth="2.5" />

          {/* Inner glow */}
          <rect x="14" y="16" width="218" height="88" rx="20" ry="20"
            fill="none" stroke="white" strokeWidth="1.5" opacity="0.5" />

          {/* Cute decorations on box */}
          <text x="20" y="32" fontSize="13" opacity="0.2">⭐</text>
          <text x="215" y="32" fontSize="13" opacity="0.2">⭐</text>
          <text x="118" y="25" fontSize="11" opacity="0.15">⭐</text>
          <text x="16" y="78" fontSize="11" opacity="0.15">🍀</text>
          <text x="220" y="78" fontSize="11" opacity="0.15">🍀</text>
          <text x="65" y="22" fontSize="9" opacity="0.15">🍀</text>
          <text x="170" y="22" fontSize="9" opacity="0.15">🍀</text>
          <text x="28" y="55" fontSize="9" opacity="0.13">♥</text>
          <text x="210" y="55" fontSize="9" opacity="0.13">♥</text>
          <text x="40" y="90" fontSize="8" opacity="0.12">✦</text>
          <text x="195" y="90" fontSize="8" opacity="0.12">✦</text>

          {/* Balls */}
          {BALLS.map((ball, i) => (
            <LottoBallInBox key={i} {...ball} shaking={isShaking} index={i} />
          ))}


        </svg>

        {/* Popping ball - sparkly ball instead of "!" */}
        <AnimatePresence>
          {isDropping && (
            <motion.div
              initial={{ y: 10, opacity: 0, scale: 0.3 }}
              animate={{ y: -50, opacity: 1, scale: 1 }}
              exit={{ y: -70, opacity: 0, scale: 0.6 }}
              transition={{ type: "spring", stiffness: 200, damping: 14 }}
              className="absolute left-1/2 -translate-x-1/2 top-2"
            >
              <div className="relative">
                <div
                  className="w-14 h-14 rounded-full flex items-center justify-center"
                  style={{
                    background: "linear-gradient(135deg, #FFD166, #FF8C42)",
                    border: "3px solid white",
                    boxShadow: "0 0 20px rgba(255,209,102,0.5), 0 4px 12px rgba(0,0,0,0.1)",
                  }}
                >
                  <span className="text-2xl">🍀</span>
                </div>
                {/* Sparkle lines around ball */}
                {[0, 45, 90, 135, 180, 225, 270, 315].map((deg) => (
                  <motion.div
                    key={deg}
                    initial={{ scale: 0 }}
                    animate={{ scale: [0, 1, 0] }}
                    transition={{ duration: 0.6, repeat: Infinity, delay: deg / 500 }}
                    className="absolute w-1.5 h-1.5 rounded-full"
                    style={{
                      background: "#FFD166",
                      top: "50%",
                      left: "50%",
                      transform: `rotate(${deg}deg) translateY(-22px)`,
                    }}
                  />
                ))}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </motion.div>

      {/* Draw Button */}
      <motion.button
        whileHover={disabled || isActive ? {} : { scale: 1.04 }}
        whileTap={disabled || isActive ? {} : { scale: 0.96 }}
        onClick={onDraw}
        disabled={disabled || isActive}
        className="cta-btn px-10 py-4 text-lg cursor-pointer flex items-center gap-2"
      >
        {isActive ? (
          <>
            <motion.span animate={{ rotate: 360 }}
              transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
              className="inline-block">🐾</motion.span>
            뽑는 중...
          </>
        ) : (
          <>🎰 번호 뽑기</>
        )}
      </motion.button>
    </div>
  );
}
