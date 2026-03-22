import { AnimatePresence, motion } from "framer-motion";
import { useLottoDraw } from "./hooks/useLottoDraw";
import Background from "./components/Background";
import BirthDateInput from "./components/BirthDateInput";
import GachaMachine from "./components/GachaMachine";
import ResultDisplay from "./components/ResultDisplay";

function App() {
  const {
    phase, result, error,
    userName, setUserName,
    birthDate, setBirthDate,
    drawnInfo,
    draw, reset,
  } = useLottoDraw();

  const showResult = result && (phase === "revealing" || phase === "done");
  const canDraw = !!birthDate && !!userName.trim();

  return (
    <div className="relative min-h-screen flex flex-col items-center px-4 py-8 sm:py-10">
      <Background />

      <div className="relative z-10 w-full max-w-md mx-auto flex flex-col items-center">
        {/* Header */}
        <motion.header
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-6"
        >
          <h1 className="text-3xl sm:text-4xl font-bold mb-1"
            style={{ fontFamily: "var(--font-family-title)", color: "#2E8B57" }}>
            행운의 로또
          </h1>
          <p className="text-text-muted text-base">
            귀여운 냥이가 행운 번호를 뽑아줄게요 🐱
          </p>
        </motion.header>

        {/* Input - only on main page */}
        {!showResult && (
          <div className="mb-6 w-full">
            <BirthDateInput
              name={userName}
              onNameChange={setUserName}
              birthDate={birthDate}
              onBirthDateChange={setBirthDate}
              disabled={phase !== "idle" && phase !== "done"}
            />
          </div>
        )}

        {/* Error */}
        <AnimatePresence>
          {error && (
            <motion.div
              initial={{ opacity: 0, y: -10, scale: 0.95 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: -10, scale: 0.95 }}
              className="mb-4 px-4 py-3 rounded-2xl text-sm flex items-center gap-2"
              style={{ background: "#FFF0F0", border: "1.5px solid #FFD5D5", color: "#C62828" }}
            >
              😿 {error}
            </motion.div>
          )}
        </AnimatePresence>

        {/* Main */}
        <AnimatePresence mode="wait">
          {!showResult ? (
            <motion.div key="machine"
              initial={{ opacity: 0 }} animate={{ opacity: 1 }}
              exit={{ opacity: 0, scale: 0.95 }} transition={{ duration: 0.3 }}>
              <GachaMachine phase={phase} onDraw={draw} disabled={!canDraw} />
            </motion.div>
          ) : (
            <motion.div key="result"
              initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }} transition={{ duration: 0.4 }} className="w-full">
              <ResultDisplay result={result} revealed={phase === "done"} drawnInfo={drawnInfo!} onReset={reset} />
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      <footer className="relative z-10 mt-auto pt-10 pb-4 text-center">
        <p className="text-[11px] text-text-dim">
          본 서비스는 오락 목적이며 당첨을 보장하지 않습니다
        </p>
      </footer>
    </div>
  );
}

export default App;
