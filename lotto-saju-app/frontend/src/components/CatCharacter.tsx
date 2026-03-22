import { motion } from "framer-motion";

interface CatCharacterProps {
  phase: string;
  message?: string;
}

export default function CatCharacter({ phase, message }: CatCharacterProps) {
  const isIdle = phase === "idle" || phase === "done";
  const isShaking = phase === "shaking";
  const isDropping = phase === "dropping";
  const isRevealing = phase === "revealing";
  const isExcited = isShaking || isDropping || isRevealing;

  return (
    <div className="flex flex-col items-center">
      {/* Speech bubble - above cat */}
      {message && (
        <motion.div
          initial={{ opacity: 0, scale: 0.7, y: 10 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          key={message}
          className="mb-2 px-5 py-3 rounded-2xl text-base font-medium relative"
          style={{ background: "white", border: "2px solid #FFE8D6", color: "#3D2C2C" }}
        >
          {message}
          {/* Bubble tail pointing down */}
          <div className="absolute -bottom-2 left-1/2 -translate-x-1/2 w-0 h-0"
            style={{
              borderLeft: "8px solid transparent",
              borderRight: "8px solid transparent",
              borderTop: "8px solid #FFE8D6",
            }}
          />
          <div className="absolute -bottom-[6px] left-1/2 -translate-x-1/2 w-0 h-0"
            style={{
              borderLeft: "6px solid transparent",
              borderRight: "6px solid transparent",
              borderTop: "6px solid white",
            }}
          />
        </motion.div>
      )}

      {/* Cat */}
      <motion.div
        animate={
          isShaking
            ? { y: [0, -4, 0, -3, 0], rotate: [-2, 2, -1, 1, 0] }
            : isDropping || isRevealing
            ? { y: [0, -8, 0], scale: [1, 1.06, 1] }
            : { y: [0, -4, 0] }
        }
        transition={
          isShaking
            ? { duration: 0.4, repeat: Infinity }
            : isDropping || isRevealing
            ? { duration: 0.7, repeat: 2 }
            : { duration: 2.5, repeat: Infinity, ease: "easeInOut" }
        }
        className="relative"
        style={{ width: 150, height: 150 }}
      >
        <svg viewBox="0 0 200 200" width="150" height="150">
          {/* ===== Chibi kawaii cat ===== */}

          {/* Tail - attached to body */}
          <motion.path
            d="M152 135 Q172 118 168 100 Q165 90 172 82"
            stroke="#FFC94D"
            strokeWidth="12"
            fill="none"
            strokeLinecap="round"
            animate={
              isIdle
                ? {
                    d: [
                      "M152 135 Q172 118 168 100 Q165 90 172 82",
                      "M152 135 Q178 114 172 98 Q168 86 176 78",
                      "M152 135 Q172 118 168 100 Q165 90 172 82",
                    ],
                  }
                : {}
            }
            transition={{ duration: 2.5, repeat: Infinity, ease: "easeInOut" }}
          />
          {/* Tail tip stripe */}
          <motion.path
            d="M168 92 Q165 90 172 82"
            stroke="#E0A820"
            strokeWidth="12"
            fill="none"
            strokeLinecap="round"
            animate={
              isIdle
                ? {
                    d: [
                      "M168 92 Q165 90 172 82",
                      "M172 88 Q168 86 176 78",
                      "M168 92 Q165 90 172 82",
                    ],
                  }
                : {}
            }
            transition={{ duration: 2.5, repeat: Infinity, ease: "easeInOut" }}
          />

          {/* Body - big round blob */}
          <ellipse cx="100" cy="142" rx="55" ry="42" fill="#FFC94D" />

          {/* === BIG round head (chibi = big head!) === */}
          <circle cx="100" cy="88" r="56" fill="#FFC94D" />

          {/* Left ear (shorter) */}
          <path d="M58 52 Q46 30 50 24 Q54 18 58 26 L72 45 Z" fill="#FFC94D" />
          <path d="M61 48 Q52 33 54 28 Q57 24 60 30 L68 44 Z" fill="#FFB0C8" />

          {/* Right ear (shorter) */}
          <path d="M142 52 Q154 30 150 24 Q146 18 142 26 L128 45 Z" fill="#FFC94D" />
          <path d="M139 48 Q148 33 146 28 Q143 24 140 30 L132 44 Z" fill="#FFB0C8" />

          {/* Forehead stripes */}
          <path d="M88 52 L90 64" stroke="#E0A820" strokeWidth="2.5" strokeLinecap="round" />
          <path d="M100 48 L100 61" stroke="#E0A820" strokeWidth="2.5" strokeLinecap="round" />
          <path d="M112 52 L110 64" stroke="#E0A820" strokeWidth="2.5" strokeLinecap="round" />

          {/* Eyes */}
          {isIdle ? (
            <>
              {/* Super happy eyes ◠ ◠ */}
              <path d="M74 86 Q84 76 94 86" stroke="#5D4037" strokeWidth="3.5" fill="none" strokeLinecap="round" />
              <path d="M106 86 Q116 76 126 86" stroke="#5D4037" strokeWidth="3.5" fill="none" strokeLinecap="round" />
              {/* Tiny sparkle near eyes */}
              <circle cx="96" cy="78" r="2" fill="#FFD700" opacity="0.6" />
              <circle cx="128" cy="78" r="2" fill="#FFD700" opacity="0.6" />
            </>
          ) : (
            <>
              {/* Big sparkly excited eyes */}
              <ellipse cx="84" cy="84" rx="11" ry="12" fill="#5D4037" />
              <ellipse cx="116" cy="84" rx="11" ry="12" fill="#5D4037" />
              {/* Big highlight */}
              <circle cx="89" cy="79" r="4.5" fill="white" />
              <circle cx="121" cy="79" r="4.5" fill="white" />
              {/* Small highlight */}
              <circle cx="81" cy="86" r="2.5" fill="white" opacity="0.5" />
              <circle cx="113" cy="86" r="2.5" fill="white" opacity="0.5" />
              {/* Star sparkle in eyes */}
              <path d="M89 79 L90 77 L91 79 L93 78 L91 80 L90 82 L89 80 L87 78 Z" fill="white" opacity="0.7" />
              <path d="M121 79 L122 77 L123 79 L125 78 L123 80 L122 82 L121 80 L119 78 Z" fill="white" opacity="0.7" />
            </>
          )}

          {/* Blush - bigger and cuter */}
          <ellipse cx="66" cy="96" rx="11" ry="7" fill="#FFB0B0" opacity="0.45" />
          <ellipse cx="134" cy="96" rx="11" ry="7" fill="#FFB0B0" opacity="0.45" />

          {/* Nose - tiny heart shape */}
          <path d="M98 95 Q98 92 100 94 Q102 92 102 95 L100 98 Z" fill="#FF9CAD" />

          {/* Mouth - big smile */}
          <path d="M93 99 Q100 106 107 99" stroke="#5D4037" strokeWidth="2" fill="none" strokeLinecap="round" />

          {/* Whiskers - cute curves */}
          <path d="M52 88 Q62 86 72 90" stroke="#D4A060" strokeWidth="1.5" fill="none" strokeLinecap="round" />
          <path d="M50 96 Q62 94 72 96" stroke="#D4A060" strokeWidth="1.5" fill="none" strokeLinecap="round" />
          <path d="M128 90 Q138 86 148 88" stroke="#D4A060" strokeWidth="1.5" fill="none" strokeLinecap="round" />
          <path d="M128 96 Q138 94 150 96" stroke="#D4A060" strokeWidth="1.5" fill="none" strokeLinecap="round" />

          {/* Left paw */}
          <motion.g
            animate={
              isExcited
                ? { y: [0, 8, 0], rotate: [0, 10, 0] }
                : {}
            }
            transition={isExcited ? { duration: 0.45, repeat: Infinity } : {}}
          >
            <ellipse cx="58" cy="148" rx="18" ry="13" fill="#FFC94D" />
            {/* Paw pads */}
            <ellipse cx="53" cy="146" rx="3.5" ry="3" fill="#FFB0C8" opacity="0.7" />
            <ellipse cx="60" cy="143" rx="3.5" ry="3" fill="#FFB0C8" opacity="0.7" />
            <ellipse cx="66" cy="146" rx="3.5" ry="3" fill="#FFB0C8" opacity="0.7" />
            <ellipse cx="58" cy="151" rx="5" ry="4" fill="#FFB0C8" opacity="0.7" />
          </motion.g>

          {/* Right paw */}
          <motion.g
            animate={
              isExcited
                ? { y: [0, 6, 0], rotate: [0, -8, 0] }
                : {}
            }
            transition={isExcited ? { duration: 0.45, repeat: Infinity, delay: 0.06 } : {}}
          >
            <ellipse cx="142" cy="148" rx="18" ry="13" fill="#FFC94D" />
            <ellipse cx="137" cy="146" rx="3.5" ry="3" fill="#FFB0C8" opacity="0.7" />
            <ellipse cx="144" cy="143" rx="3.5" ry="3" fill="#FFB0C8" opacity="0.7" />
            <ellipse cx="151" cy="146" rx="3.5" ry="3" fill="#FFB0C8" opacity="0.7" />
            <ellipse cx="142" cy="151" rx="5" ry="4" fill="#FFB0C8" opacity="0.7" />
          </motion.g>

          {/* Belly patch */}
          <ellipse cx="100" cy="148" rx="25" ry="20" fill="#FFD980" opacity="0.5" />
        </svg>

        {/* Sparkles when excited */}
        {isExcited && (
          <>
            {[...Array(6)].map((_, i) => (
              <motion.div
                key={i}
                initial={{ scale: 0, opacity: 0 }}
                animate={{ scale: [0, 1.2, 0], opacity: [0, 1, 0] }}
                transition={{
                  duration: 0.6,
                  delay: i * 0.1,
                  repeat: Infinity,
                  repeatDelay: 0.5,
                }}
                className="absolute"
                style={{
                  top: `${5 + Math.sin(i * 1.2) * 20}%`,
                  left: `${5 + (i * 17)}%`,
                  fontSize: i % 2 === 0 ? 14 : 10,
                }}
              >
                {i % 3 === 0 ? "✨" : i % 3 === 1 ? "⭐" : "💛"}
              </motion.div>
            ))}
          </>
        )}
      </motion.div>
    </div>
  );
}
